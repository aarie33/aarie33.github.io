---
id: P-024
title: RKL-RPL Waste Reporting App
tagline: "Environmental compliance reporting system for PT SIER's industrial tenants"
tier: featured
year: 2023
domain: Internal Tools
roles: [Dev Lead, Fullstack Developer]
client: "PT SIER"
stack: [Laravel, Inertia.js, Vue.js, Flutter]
architecture: "Laravel + Inertia web app with a companion Flutter mobile app"
cover: ./images/rkl-rpl-app-pelaporan-limbah/cover.png
screenshots:
  - src: ./images/rkl-rpl-app-pelaporan-limbah/shot-1.png
    caption: "Monthly waste-document reporting and validation view"
featured: true
draft: false
order: 24
---

## Context
RKL-RPL (Rencana Pengelolaan Lingkungan / Rencana Pemantauan Lingkungan) is
Indonesia's mandated environmental management and monitoring reporting
scheme. PT SIER's industrial tenants are required to submit and validate
waste-management documentation on a regular cycle — a compliance
requirement with real regulatory weight, previously handled through
manual document submission and review.

## Technical challenge
This wasn't a generic form-and-approval app: it needed a live consultation
channel between tenants and facility staff (realtime chat) running
alongside a document validation workflow with monthly reporting cycles,
built for the same dual web/mobile audience as PT SIER's other systems on
this stack.

## Architecture & decisions
Reused the Laravel + Inertia + Flutter split established on the Sier Sport
Arena project — a deliberate choice to keep PT SIER's systems on a
consistent stack rather than introducing a new one per project, which paid
off directly in shared patterns for the web/mobile split and realtime
messaging.

## Contribution
Led the build as Dev Lead: the realtime chatroom for consultations, and the
monthly waste-document reporting and validation workflow.

## Result
Gave PT SIER's environmental compliance team a structured, auditable
digital trail for waste-report submissions and tenant consultations, in
place of ad hoc document handling.

## Lesson
Standardizing on one stack across multiple projects for the same client
compounds — the realtime messaging groundwork from the sports-arena project
carried over almost directly here, at a fraction of the original cost.
