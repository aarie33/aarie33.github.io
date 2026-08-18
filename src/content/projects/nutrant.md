---
id: P-027
title: Nutrant
tagline: "Food nutrition tracking app with PDF/Excel export for clinical use"
tier: featured
year: 2024
domain: Healthcare
roles: [Dev Lead]
stack: [Laravel, Inertia.js, Vue.js]
cover: ./images/nutrant/cover.png
featured: true
draft: false
order: 27
---

## Context
Nutrant is a food-nutrition tracking application, the most clinically
oriented entry in a series of nutrition products built over several years —
built to let users and practitioners record eating history and see it
translated into structured nutrition data, not just a food diary.

## Technical challenge
Nutrition calculation is only useful if the numbers are trustworthy and the
output is usable outside the app itself — this meant getting food-to-nutrient
calculation logic right, and treating export as a first-class feature rather
than an afterthought, since clinical and institutional users needed to hand
reports off in PDF or Excel.

## Architecture & decisions
Built on the by-then-standard Laravel + Inertia + Vue stack, with the
eating-history and calculation logic centralized server-side so the exported
PDF/Excel reports and the in-app views were always generated from the same
source of truth, rather than duplicating calculation logic per output format.

## Contribution
Sole developer on the project: data model, nutrition-calculation logic, and
both export formats.

## Result
Gave users and practitioners a single tool to log eating history, see
calculated nutrition breakdowns, and produce shareable PDF/Excel reports —
consolidating what nutrition tracking, calculation, and reporting had been
doing as separate steps in earlier products in this line.

## Lesson
Centralizing calculation logic behind the export formats rather than inside
each one paid for itself the moment a second export format was added.

## Key features
- Record eating history
- Calculate food nutrition
- Report, export to PDF/Excel
