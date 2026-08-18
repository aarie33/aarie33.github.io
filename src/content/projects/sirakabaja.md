---
id: P-008
title: SirakaBaja
tagline: "Companion module extending the Siraka campus system"
tier: compact
year: 2021
domain: Education
roles: [Backend Developer]
client: "Politeknik Negeri Jember"
stack: [CodeIgniter, HMVC]
architecture: "Modular monolith (HMVC)"
cover: ./images/sirakabaja/cover.png
featured: false
draft: false
order: 8
---

## Context
SirakaBaja extends the Siraka campus information system for Politeknik
Negeri Jember with an additional module built on a modular CodeIgniter
architecture.

## Technical challenge
Keeping a second HMVC module cleanly decoupled from the base Siraka
codebase while sharing its data model.
