---
id: P-023
title: Sier Sport Arena
tagline: "Multi-venue sports facility booking platform for PT SIER"
tier: featured
year: 2022
domain: E-commerce
roles: [Dev Lead, Fullstack Developer]
client: "PT SIER"
stack: [Laravel, Inertia.js, Vue.js, Flutter]
architecture: "Laravel + Inertia web app with a companion Flutter mobile app"
cover: ./images/sier-sport-arena-booking-app/cover.png
screenshots:
  - src: ./images/sier-sport-arena-booking-app/shot-1.png
    caption: "Venue booking flow on the Sier Sport Arena web app"
featured: true
draft: false
order: 23
---

## Context
PT SIER (Surabaya Industrial Estate Rungkut) operates sports facilities as
part of its industrial-estate amenities. Before this system, venue booking
ran through manual coordination — phone calls and a shared schedule someone
had to keep updating by hand. As the estate's tenant base grew, that
process stopped scaling: double-bookings and scheduling conflicts were
becoming routine.

## Technical challenge
The core difficulty wasn't any single feature — it was keeping a single
source of truth for venue availability consistent across two clients at
once: the Laravel + Inertia web app for staff/admin use, and a separate
Flutter mobile app for end users booking on the go. Both needed to see the
same real-time slot state, and a chatroom feature meant the system also had
to handle lower-latency, session-based communication alongside the
request/response booking flow.

## Architecture & decisions
Laravel served as the single backend for both clients, with Inertia
powering the admin-facing web app directly against Laravel views/controllers
and a versioned API layer serving the Flutter app. Centralizing booking-slot
logic in one backend — rather than letting either client own its own
availability rules — was the deliberate trade-off: it added integration
work up front but removed an entire class of double-booking bugs that a
split-logic approach would have invited.

## Contribution
Led the project as Dev Lead and built across the stack: the venue and
schedule management backend, the booking flow, and the chatroom feature
connecting facility staff and renters.

## Result
Facility booking moved from manual, phone-based coordination to a
self-service flow across web and mobile, with schedule and booking
management consolidated into one system for PT SIER's operations staff.

## Lesson
Building two clients against one backend from day one is more work up
front than letting each client evolve its own shortcuts — but for anything
involving shared, mutable state like booking slots, that discipline is what
actually prevents the conflicts the system was built to solve.
