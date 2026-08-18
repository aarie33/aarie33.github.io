#!/usr/bin/env python3
"""Generate src/content/projects/*.md + images from My-Portfolio.pptx.

Usage:
    python scripts/extract_pptx.py                  # generate everything
    python scripts/extract_pptx.py --dry-run         # preview, write nothing
    python scripts/extract_pptx.py --slide 12        # regenerate one slide
    python scripts/extract_pptx.py --force           # overwrite edited files
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Emu
from slugify import slugify

ROOT = Path(__file__).resolve().parent.parent
PPTX_PATH = ROOT / "My-Portfolio.pptx"
CONTENT_DIR = ROOT / "src/content/projects"
CONTACT_PATH = ROOT / "src/data/contact.json"
CACHE_DIR = ROOT / ".extraction-cache"
REPORT_PATH = ROOT / ".extraction-report.md"
DICTIONARY_PATH = Path(__file__).parent / "stack_dictionary.json"

PICTURE = 13
DECORATIVE_AREA_THRESHOLD = 0.05

ROLE_PATTERNS = [
    (re.compile(r"\bdev\s*lead\b|\bteam\s*lead\b", re.I), "Dev Lead"),
    (re.compile(r"\bfull[\s-]?stack\b", re.I), "Fullstack Developer"),
    (re.compile(r"\bback[\s-]?end\b", re.I), "Backend Developer"),
    (re.compile(r"\bfront[\s-]?end\b", re.I), "Frontend Developer"),
    (re.compile(r"\bmobile\b", re.I), "Mobile Developer"),
    (re.compile(r"\bsystem\s*analyst\b", re.I), "System Analyst"),
]

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{7,}\d")
LINKEDIN_RE = re.compile(r"linkedin\.com/\S+", re.I)
GITHUB_RE = re.compile(r"github\.com/\S+", re.I)
YEAR_RE = re.compile(r"\b(20\d{2})\b")
PAREN_RE = re.compile(r"\(([^)]+)\)")
TECHSTACK_RE = re.compile(r"tech\s*stack\s*:\s*([^\n]+)", re.I)
TEAMSIZE_RE = re.compile(r"(\d+)\s*(orang|people|dev|member)", re.I)
FEATURES_HEADER_RE = re.compile(r"^\s*features?\s*:?\s*$", re.I)

with open(DICTIONARY_PATH) as f:
    STACK_DICT: dict[str, list[str]] = json.load(f)


def normalize_stack_token(raw: str) -> list[str]:
    key = raw.strip().lower()
    key = re.sub(r"\s+", " ", key)
    if key in STACK_DICT:
        return STACK_DICT[key]
    if not key:
        return []
    return [" ".join(w.capitalize() for w in key.split())]


def split_stack_phrase(phrase: str) -> list[str]:
    parts = re.split(r"[,/&+]", phrase)
    out: list[str] = []
    for p in parts:
        for tok in normalize_stack_token(p):
            if tok not in out:
                out.append(tok)
    return out


@dataclass
class SlideInfo:
    index: int
    kind: str = "skip"
    title: str | None = None
    tagline: str | None = None
    roles: list[str] = field(default_factory=list)
    stack: list[str] = field(default_factory=list)
    client: str | None = None
    confidential: bool = False
    year: int | None = None
    team_size: int | None = None
    features: list[str] = field(default_factory=list)
    unmapped_stack: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    cover_path: Path | None = None
    shot_paths: list[Path] = field(default_factory=list)
    thumb_path: Path | None = None


@dataclass
class SlideBoxes:
    title: str | None
    subtitle: str | None
    other: list[str]


def collect_boxes(slide) -> SlideBoxes:
    """Layout in this deck is consistent: TITLE placeholder carries the
    project name, SUBTITLE placeholder carries role + stack, and any extra
    text boxes carry client name and/or a 'Features:' block — in shape
    order. Falls back gracefully if a slide doesn't use placeholders."""
    title = None
    subtitle = None
    other: list[str] = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        text = shape.text_frame.text.strip()
        if not text:
            continue
        if shape.is_placeholder:
            try:
                ph_type = shape.placeholder_format.type
            except Exception:
                ph_type = None
            ph_name = str(ph_type) if ph_type is not None else ""
            if "TITLE" in ph_name and "SUBTITLE" not in ph_name and title is None:
                title = text
                continue
            if "SUBTITLE" in ph_name or "BODY" in ph_name:
                subtitle = text
                continue
        other.append(text)
    return SlideBoxes(title=title, subtitle=subtitle, other=other)


def full_text(slide) -> str:
    chunks = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            t = shape.text_frame.text.strip()
            if t:
                chunks.append(t)
    return "\n".join(chunks)


def classify(slide, pics: list) -> str:
    text = full_text(slide)
    if EMAIL_RE.search(text) and (PHONE_RE.search(text) or LINKEDIN_RE.search(text)):
        if len(pics) == 0:
            return "contact"
    n_shapes = len(slide.shapes)
    if not pics and n_shapes < 3:
        return "skip"
    if not pics:
        return "skip"
    if not text.strip():
        return "skip"
    return "project"


def extract_roles(text: str) -> list[str]:
    found: list[str] = []
    for pattern, canonical in ROLE_PATTERNS:
        if pattern.search(text) and canonical not in found:
            found.append(canonical)
    return found


def extract_stack(text: str) -> tuple[list[str], list[str]]:
    stack: list[str] = []
    for m in PAREN_RE.finditer(text):
        for tok in split_stack_phrase(m.group(1)):
            if tok not in stack:
                stack.append(tok)
    ts_match = TECHSTACK_RE.search(text)
    if ts_match:
        for tok in split_stack_phrase(ts_match.group(1)):
            if tok not in stack:
                stack.append(tok)
    known_lower = {v.lower() for vals in STACK_DICT.values() for v in vals}
    unmapped = [s for s in stack if s.lower() not in known_lower and s.lower() not in STACK_DICT]
    return stack, unmapped


def extract_features(text: str) -> list[str]:
    lines = text.split("\n")
    out: list[str] = []
    capturing = False
    for line in lines:
        stripped = line.strip()
        if FEATURES_HEADER_RE.match(stripped) or stripped.lower().startswith("features"):
            capturing = True
            after = re.sub(r"(?i)^features?\s*:?\s*", "", stripped)
            if after:
                out.append(after)
            continue
        if capturing:
            if not stripped or stripped.lower() == "etc":
                continue
            out.append(stripped)
    return out


def extract_name_and_client(title: str | None, other_boxes: list[str]) -> tuple[str | None, str | None, bool]:
    """Returns (project_name, client, confidential). Prefers a dedicated
    client text box over splitting the title, since some titles contain a
    ' - ' that is part of the name itself (e.g. 'Rkl rpl (app ...)')."""
    name = title
    client = None
    confidential = False
    for box in other_boxes:
        if FEATURES_HEADER_RE.match(box.split("\n")[0].strip()) or box.lower().startswith("features"):
            continue
        if "confidential" in box.lower():
            confidential = True
            continue
        first_line = box.split("\n")[0].strip()
        first_line = re.sub(r"\s*\((hongkong|hong kong)\)\s*", "", first_line, flags=re.I).strip()
        if first_line and client is None:
            client = first_line
    if client is None and name and " - " in name:
        n, c = name.split(" - ", 1)
        name, client = n.strip(), c.strip()
    return name, client, confidential


def pick_images(slide, out_dir: Path, base_name: str, dry_run: bool) -> tuple[Path | None, list[Path], Path | None]:
    slide_w, slide_h = slide.part.package.presentation_part.presentation.slide_width, None
    prs = slide.part.package.presentation_part.presentation
    slide_area = prs.slide_width * prs.slide_height

    pics = [s for s in slide.shapes if s.shape_type == PICTURE]
    pics = [p for p in pics if (p.width * p.height) / slide_area > DECORATIVE_AREA_THRESHOLD]
    pics.sort(key=lambda p: p.width * p.height, reverse=True)

    if not pics:
        return None, [], None

    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    cover_path = None
    shot_paths: list[Path] = []
    thumb_path = None

    for i, pic in enumerate(pics):
        try:
            blob = pic.image.blob
        except Exception:
            continue
        img = Image.open(io.BytesIO(blob))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        if img.width > 1600:
            img = img.resize((1600, int(img.height * 1600 / img.width)), Image.LANCZOS)

        if i == 0:
            cover_path = out_dir / "cover.png"
            if not dry_run:
                img.save(cover_path, "PNG", optimize=True)
            thumb = img.copy()
            thumb.thumbnail((480, 480), Image.LANCZOS)
            thumb_path = out_dir / "thumb.webp"
            if not dry_run:
                thumb.save(thumb_path, "WEBP", quality=78)
        else:
            shot_path = out_dir / f"shot-{i}.png"
            if not dry_run:
                img.save(shot_path, "PNG", optimize=True)
            shot_paths.append(shot_path)

    return cover_path, shot_paths, thumb_path


def estimate_year(slide_index: int, first_project_slide: int, last_project_slide: int) -> int:
    """Slides are ordered oldest -> newest (per deck's own note). No explicit
    year exists on most slides, so interpolate across an assumed career span.
    Flagged as an estimate in the QA report — verify and correct manually."""
    span_start, span_end = 2018, 2025
    if last_project_slide == first_project_slide:
        return span_end
    ratio = (slide_index - first_project_slide) / (last_project_slide - first_project_slide)
    return round(span_start + ratio * (span_end - span_start))


def render_markdown(slide_id: str, order: int, info: SlideInfo, slug: str) -> str:
    screenshots_yaml = ""
    if info.shot_paths:
        lines = []
        for i, p in enumerate(info.shot_paths, 1):
            lines.append(f"  - src: ./images/{slug}/{p.name}")
            lines.append(f'    caption: "{{{{TODO}}}}"')
        screenshots_yaml = "screenshots:\n" + "\n".join(lines) + "\n"

    stack_yaml = "[" + ", ".join(info.stack) + "]" if info.stack else "[]"
    roles_yaml = "[" + ", ".join(info.roles) + "]" if info.roles else "[Backend Developer]"

    if info.confidential:
        client_line = 'client: "{{TODO — confidential, use a generic description}}"\n'
    elif info.client:
        client_line = f'client: "{info.client}"\n'
    else:
        client_line = ""
    team_line = f"teamSize: {info.team_size}\n" if info.team_size else ""

    body_lines = ["## Context", "{{TODO}}", "", "## Technical challenge", "{{TODO}}"]
    if info.features:
        body_lines += ["", "## Key features"]
        for feat in info.features:
            body_lines.append(f"- {feat}")

    body = "\n".join(body_lines)

    fm = f"""---
id: {slide_id}
title: {info.title or "{{TODO}}"}
tagline: "{info.tagline or "{{TODO}}"}"
tier: compact
year: {info.year}
domain: "{{{{TODO}}}}"
roles: {roles_yaml}
{team_line}{client_line}stack: {stack_yaml}
cover: ./images/{slug}/cover.png
{screenshots_yaml}featured: false
draft: false
order: {order}
_generated: true
_sourceSlide: {info.index}
_extractedAt: {date.today().isoformat()}
---

{body}
"""
    return fm


def run(dry_run: bool, only_slide: int | None, force: bool):
    prs = Presentation(PPTX_PATH)
    n_slides = len(prs.slides)
    CACHE_DIR.mkdir(exist_ok=True)

    project_slides: list[SlideInfo] = []
    contact_lines: list[str] = []
    skipped: list[tuple[int, str]] = []
    unmapped_all: dict[str, list[int]] = {}
    review_needed: list[tuple[int, str, str, str]] = []

    for idx, slide in enumerate(prs.slides, start=1):
        pics = [s for s in slide.shapes if s.shape_type == PICTURE]
        kind = classify(slide, pics)
        text = full_text(slide)

        if kind == "contact":
            contact_lines.append(text)
            continue
        if kind == "skip":
            skipped.append((idx, (text[:40] + "...") if text else "(no text)"))
            continue

        info = SlideInfo(index=idx, kind="project")
        boxes = collect_boxes(slide)
        raw_title = boxes.title.split("\n")[0].strip() if boxes.title else None
        name, client, confidential = extract_name_and_client(raw_title, boxes.other)
        info.title = name.strip() if name else None
        info.client = client
        info.confidential = confidential

        role_stack_text = boxes.subtitle or text
        info.roles = extract_roles(role_stack_text)
        stack, unmapped = extract_stack(role_stack_text)
        info.stack = stack
        info.unmapped_stack = unmapped
        for u in unmapped:
            unmapped_all.setdefault(u, []).append(idx)

        info.features = extract_features("\n".join(boxes.other))

        ym = YEAR_RE.search(text)
        if ym:
            info.year = int(ym.group(1))

        tm = TEAMSIZE_RE.search(text)
        if tm:
            info.team_size = int(tm.group(1))

        if boxes.subtitle and not PAREN_RE.search(boxes.subtitle) and len(boxes.subtitle) > 60:
            first_sentence = re.split(r"(?<=[.!?])\s", boxes.subtitle.strip())[0]
            info.tagline = first_sentence[:90]

        if not info.title:
            review_needed.append((idx, "{{TODO}}", "?", "Title not detected"))
        if info.confidential:
            review_needed.append((idx, "?", info.title or "?", "Marked confidential in source — client anonymized, verify wording"))
        project_slides.append(info)

    if not project_slides:
        print("No project slides found.")
        return

    first_idx = project_slides[0].index
    last_idx = project_slides[-1].index
    for info in project_slides:
        if info.year is None:
            info.year = estimate_year(info.index, first_idx, last_idx)

    manifest_path = CACHE_DIR / "manifest.json"
    manifest: dict[str, dict] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())

    written, skipped_edited, regenerated = 0, 0, 0

    for order, info in enumerate(project_slides, start=1):
        if only_slide is not None and info.index != only_slide:
            continue

        slide_id = f"P-{order:03d}"
        base_slug = slugify(info.title or f"project-{order}")
        slug = base_slug
        suffix = 2
        used_slugs = {v["slug"] for v in manifest.values()}
        while slug in used_slugs and manifest.get(slide_id, {}).get("slug") != slug:
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        md_path = CONTENT_DIR / f"{slug}.md"
        img_dir = CONTENT_DIR / "images" / slug

        if md_path.exists() and not force:
            existing = md_path.read_text()
            if "_generated: true" not in existing:
                skipped_edited += 1
                continue

        cover, shots, thumb = pick_images(prs.slides[info.index - 1], img_dir, slug, dry_run)
        info.cover_path = cover
        info.shot_paths = shots
        info.thumb_path = thumb

        if cover is None:
            review_needed.append((info.index, slide_id, info.title or "?", "No usable image found"))

        if len(shots) + (1 if cover else 0) > 1:
            review_needed.append((info.index, slide_id, info.title or "?", f"{len(shots)+1} images — verify cover is correct"))

        if not dry_run:
            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_text(render_markdown(slide_id, order, info, slug))
            manifest[slide_id] = {"slide": info.index, "slug": slug}

        written += 1
        if md_path.exists() and force:
            regenerated += 1

    if not dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2))

        contact = {}
        for line in contact_lines:
            email = EMAIL_RE.search(line)
            phone = PHONE_RE.search(line)
            linkedin = LINKEDIN_RE.search(line)
            github = GITHUB_RE.search(line)
            if email:
                contact["email"] = email.group(0)
            if phone:
                contact["phone"] = phone.group(0).strip()
            if linkedin:
                contact["linkedin"] = "https://" + linkedin.group(0)
            if github:
                contact["github"] = "https://" + github.group(0)
        if contact:
            CONTACT_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONTACT_PATH.write_text(json.dumps(contact, indent=2) + "\n")

    report = [
        f"# Extraction Report — {date.today():%d %b %Y}",
        f"Source: {PPTX_PATH.name} ({n_slides} slides)",
        "",
        "## Summary",
        f"- {len(project_slides)} slide(s) -> project",
        f"- {len(contact_lines)} slide(s) -> contact",
        f"- {len(skipped)} slide(s) -> skipped (cover, divider, thank-you)",
        f"- {skipped_edited} project file(s) left untouched (already hand-edited)",
        "",
        "## Needs manual review",
        "| Slide | ID | Project | Issue |",
        "|---|---|---|---|",
    ]
    for idx, sid, name, issue in review_needed:
        report.append(f"| {idx} | {sid} | {name} | {issue} |")

    report += ["", "## Unmapped stack tokens (add to stack_dictionary.json)"]
    if unmapped_all:
        for tok, slides in unmapped_all.items():
            report.append(f"- \"{tok}\" (slide {', '.join(str(s) for s in slides)})")
    else:
        report.append("- none")

    report += ["", "## Skipped slides"]
    for idx, snippet in skipped:
        report.append(f"- Slide {idx} — {snippet}")

    report += [
        "",
        "## Estimated years",
        "No slide carries an explicit year for most projects. Years were "
        "linearly interpolated across the deck assuming a 2018-2025 span "
        "(slides are already ordered oldest -> newest per the deck's own "
        "note on slide 2). **Verify and correct `year:` in each file.**",
    ]

    if not dry_run:
        REPORT_PATH.write_text("\n".join(report) + "\n")

    print(f"{'[dry-run] ' if dry_run else ''}{written} project file(s) processed, "
          f"{skipped_edited} skipped (hand-edited), {len(skipped)} slide(s) not a project.")
    if not dry_run:
        print(f"Report written to {REPORT_PATH}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--slide", type=int, default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if not PPTX_PATH.exists():
        print(f"Source not found: {PPTX_PATH}", file=sys.stderr)
        sys.exit(1)

    run(dry_run=args.dry_run, only_slide=args.slide, force=args.force)


if __name__ == "__main__":
    main()
