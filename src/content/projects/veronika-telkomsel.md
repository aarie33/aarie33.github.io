---
id: P-035
title: Veronika
tagline: "Omnichannel AI chatbot serving millions of Telkomsel customers"
tier: featured
year: 2025
domain: Internal Tools
roles: [Backend Developer]
client: "Telkomsel"
stack: [Java, Node.js, Go, AWS, Kafka]
architecture: "Event-driven microservices"
cover: ./images/veronika-telkomsel/cover.png
featured: true
draft: false
order: 35
---

## Context
Veronika is an enterprise-grade AI chatbot serving millions of users across
Telkomsel's digital touchpoints — WhatsApp, Telegram, Instagram, Facebook
Messenger, the MyTelkomsel app, and a standalone web chat — automating
customer queries that would otherwise queue for a human agent.

## Technical challenge
Millions of users across six different channels means message volume and
variety that a request/response backend can't absorb cleanly — the system
needed to orchestrate messages from heterogeneous channels into one AI
engine and back, without any single channel's traffic spike degrading the
others.

## Architecture & decisions
Event-driven microservices built on Java, Node.js, and Go, using Kafka for
message orchestration across channels, deployed on AWS. Decoupling channel
ingestion from AI processing via Kafka — rather than each channel
integration calling the AI engine directly — was the key architectural
choice: it isolated channel-specific traffic patterns from the shared AI
backend and let channels be added without touching core orchestration logic.

## Contribution
Built and optimized backend integration services handling high-throughput
API communication between the social/messaging channels and Telkomsel's
core internal infrastructure.

## Result
Automated customer query handling at a scale — millions of users, six
channels — that would be impractical to staff with human agents alone,
while keeping response orchestration consistent regardless of which channel
a customer used.

## Lesson
Putting an event broker between channel ingestion and AI processing early
meant channel growth (six and counting) never became an architectural
problem, only a configuration one.
