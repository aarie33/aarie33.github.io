---
id: P-026
title: Project Management App
tagline: "Internal project tracking system for a construction company"
tier: standard
year: 2024
domain: ERP
roles: [Dev Lead]
client: "Jember Futura"
stack: [Laravel, Inertia.js, Vue.js]
cover: ./images/project-management-app/cover.png
screenshots:
  - src: ./images/project-management-app/shot-1.png
    caption: "Project and material tracking dashboard for Jember Futura"
featured: false
draft: false
order: 26
---

## Context
Built for Jember Futura to manage internal projects — tracking materials
and quality control alongside project timelines, replacing spreadsheet-based
tracking.

## Technical challenge
Modeling project → material → quality-control as related, queryable data
rather than the flat spreadsheet rows it was replacing.

## Key features
- Project management
- Material tracking per project
- Quality control per project
