---
id: P-034
title: AntreAja
tagline: "Nationwide digital queue management system for Telkomsel GraPARI outlets"
tier: featured
year: 2025
domain: Internal Tools
roles: [Backend Developer]
client: "Telkomsel"
stack: [React, Node.js, Go, AWS]
architecture: "Microservices on AWS"
cover: ./images/antreaja-telkomsel/cover.png
featured: true
draft: false
order: 34
---

## Context
AntreAja is a nationwide digital queue management system operating under
the DSC ecosystem, built to replace physical queue-taking at Telkomsel's
GraPARI outlets with remote, trackable virtual queues.

## Technical challenge
Queue state needed to stay accurate and real-time across a nationwide
network of outlets simultaneously — customers checking queue status
remotely needed to see the same state staff saw on-site, with no lag that
would send someone to a outlet just to find the queue had moved on.

## Architecture & decisions
A Go and Node.js backend on AWS handling real-time queue state, with
ReactJS on the frontend for both the customer-facing queue view and
outlet-locator flow. Building this as a nationwide service from the start —
rather than a per-outlet queue tool — was the deliberate scope decision,
since Telkomsel's outlet network made a fragmented per-location system a
non-starter operationally.

## Contribution
Backend development on the real-time queue engine and its integration into
the wider DSC platform.

## Result
Let customers locate the nearest outlet, book a queue number in advance,
and monitor service availability remotely — removing the need to
physically queue to know where they stood.

## Lesson
Real-time queue state is a distributed-systems problem disguised as a
simple feature; treating it as one paid off once outlet volume scaled
nationwide.
