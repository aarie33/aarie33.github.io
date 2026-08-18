---
id: P-033
title: Digital Smart Care (DSC)
tagline: "Enterprise agent-assist platform for Telkomsel's GraPARI customer service"
tier: featured
year: 2025
domain: Internal Tools
roles: [Backend Developer]
client: "Telkomsel"
stack: [React, Node.js, Go, AWS]
architecture: "Microservices on AWS"
cover: ./images/dsc-telkomsel/cover.png
metrics:
  - label: Agent info-seeking steps reduced
    value: "50%"
  - label: NPS at GraPARI
    value: "89.25%"
featured: true
draft: false
order: 33
---

## Context
Digital Smart Care (DSC) is an enterprise-grade platform for Telkomsel's
GraPARI customer service agents — the staff handling in-person and digital
customer interactions across Telkomsel's retail network. Agents previously
had to search across multiple disconnected systems to answer customer
questions, which slowed down every interaction and made service quality
inconsistent across outlets.

## Technical challenge
The system needed to unify knowledge lookup, queue management (via the
AntreAja integration), and transaction tooling into one interface agents
could use without context-switching — at Telkomsel's scale, where
inconsistent tooling multiplies into real customer-facing delay across
hundreds of outlets.

## Architecture & decisions
Built as part of the DSC ecosystem on AWS, with a ReactJS frontend and a
Node.js backend for agent-facing services, integrating an AI-powered
Knowledge Management System (KMS) so agents get relevant answers surfaced
to them instead of having to search for them. Centralizing agent tooling
into one platform — rather than layering yet another point tool onto
agents' existing workflow — was the core bet, and it's what the outcome
metrics below reflect.

## Contribution
Backend development on the agent-assist services powering DSC's core
tooling and its integration with the AI-driven knowledge system.

## Result
Reduced the number of steps agents needed to find customer information by
50%, and DSC contributed to Telkomsel achieving an 89.25% Net Promoter
Score at GraPARI outlets.

## Lesson
Unifying disconnected agent tools into a single interface produced a bigger
service-quality gain than any individual feature within it — the
consolidation itself was the win.
