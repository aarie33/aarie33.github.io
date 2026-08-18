---
id: P-009
title: Apromed
tagline: "Hospital operations system for RSU Kaliwates Jember"
tier: compact
year: 2020
domain: Healthcare
roles: [Dev Lead, Fullstack Developer]
client: "RSU Kaliwates Jember"
stack: [CodeIgniter, HMVC, Kotlin]
architecture: "Modular monolith (HMVC) + native Android"
cover: ./images/apromed/cover.png
screenshots:
  - src: ./images/apromed/shot-1.png
    caption: "Patient and hospital operations dashboard for RSU Kaliwates Jember"
featured: false
draft: false
order: 9
---

## Context
Apromed is a hospital operations system built for RSU Kaliwates Jember,
pairing a CodeIgniter HMVC backend with a native Kotlin companion app.

## Technical challenge
Coordinating a web backend and a native mobile client against the same
hospital data model, in a domain where data accuracy is non-negotiable.
