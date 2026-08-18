---
id: P-034
title: AntreAja
tagline: "Nationwide digital queue management system for Telkomsel GraPARI outlets"
tier: featured
year: 2025
domain: Internal Tools
roles: [Fullstack Developer]
client: "Telkomsel"
stack: [Go, MySQL, Redis, Kafka]
architecture: "Golang microservices, event-driven via Kafka"
cover: ./images/antreaja-telkomsel/cover.png
metrics:
  - label: GraPARI outlets served
    value: "500+"
  - label: Queue events processed
    value: "1,000s/day"
featured: true
draft: false
order: 34
---

## Context
AntreAja is a nationwide digital queue management system operating under
the DSC ecosystem, built to replace physical queue-taking at Telkomsel's
GraPARI outlets with remote, trackable virtual queues across 500+ outlets
nationwide. Built as a Senior Full Stack Developer at PT. Dans Multi Pro,
within Telkomsel's ecosystem.

## Technical challenge
Queue state needed to stay accurate and real-time across a nationwide
network of outlets simultaneously, processing thousands of queue events a
day — customers checking queue status remotely needed to see the same
state staff saw on-site, with no lag that would send someone to an outlet
just to find the queue had moved on.

## Architecture & decisions
Golang microservices handle the full digital queue flow — creation,
assignment, status updates — with Kafka providing event-driven
communication between services so status changes propagate reliably under
high volume. MySQL and Redis back persistent and fast-access queue state
respectively. Building this as a nationwide, event-driven service from the
start — rather than a per-outlet queue tool — was the deliberate scope
decision, since Telkomsel's outlet network made a fragmented per-location
system a non-starter operationally.

## Contribution
Maintained and extended the Golang-based microservices handling the
end-to-end queue flow, working across both backend and frontend to ship
features using Golang, REST APIs, MySQL, and Redis. Monitored and
troubleshot production services using Splunk logs to investigate issues
and keep daily operations reliable across 500+ outlets.

## Result
Customers can locate the nearest outlet, book a queue number in advance,
and monitor service availability remotely — removing the need to
physically queue to know where they stood — while the platform reliably
processes thousands of queue events every day across 500+ outlets
nationwide.

## Lesson
Real-time queue state is a distributed-systems problem disguised as a
simple feature; putting Kafka between services early meant status updates
stayed consistent even as event volume scaled nationwide.
