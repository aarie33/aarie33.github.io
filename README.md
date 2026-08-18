# Portfolio — Ahmad Syamsul Arifin

Static portfolio site built with Astro, replacing `My-Portfolio.pptx` as the
primary artifact for job applications and client pitches. See `PRD.md` for
the full spec this was built against.

## Structure

```
My-Portfolio.pptx          Source deck — read-only, extracted once
scripts/extract_pptx.py    Extraction pipeline (see below)
src/content/projects/      One markdown file per project (35), the real
                            source of truth after extraction
src/content.config.ts      Zod schema for project frontmatter
src/layouts/project/       Featured / Standard / Compact detail templates
src/components/            IndexTable, FilterBar, BrowserFrame, etc.
src/styles/                tokens.css, base.css, motion.css
```

## Commands

| Command           | Action                                      |
| ------------------ | -------------------------------------------- |
| `npm install`       | Install dependencies                         |
| `npm run dev`       | Local dev server at `localhost:4321`         |
| `npm run build`     | Production build to `./dist/`                |
| `npm run preview`   | Preview the production build locally         |

## Re-running the extraction pipeline

Only needed if `My-Portfolio.pptx` changes. Project files that have already
been hand-edited (i.e. no longer have `_generated: true` in frontmatter) are
never overwritten.

```bash
pip install -r scripts/requirements.txt
python scripts/extract_pptx.py                  # generate/update everything
python scripts/extract_pptx.py --dry-run         # preview only
python scripts/extract_pptx.py --slide 12        # regenerate one slide
python scripts/extract_pptx.py --force           # overwrite edited files
```

Check `.extraction-report.md` after running — it lists slides that need a
manual look (ambiguous titles, multiple images, unmapped stack tokens).

## Adding a project by hand

Create `src/content/projects/{slug}.md` following the schema in
`src/content.config.ts`. No `_generated` field means the extractor will
leave it alone on future runs.

## Deploying

Push to `main` — `.github/workflows/deploy.yml` builds and deploys to
GitHub Pages automatically. Repository Settings → Pages → Source must be set
to **GitHub Actions** once, the first time.

Site is configured for `aarie33.github.io` (`astro.config.mjs`: `site` +
`base: '/'`). If the repo is renamed to something else, `base` needs to
change to match, and `import.meta.env.BASE_URL` should be used for any
manually-written links.
