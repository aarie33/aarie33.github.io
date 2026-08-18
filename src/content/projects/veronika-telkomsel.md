---
id: P-035
title: Veronika
tagline: "Omnichannel AI chatbot serving millions of Telkomsel customers"
tier: featured
year: 2026
domain: Internal Tools
roles: [Fullstack Developer]
client: "Telkomsel"
stack: [Java, Spring Boot, Python, Kubernetes, AWS, Kafka, Redis, gRPC, React, TypeScript]
architecture: "Event-driven microservices (Spring Boot + Python) on Kubernetes/AWS EKS, orchestrated via Kafka with gRPC and SSE for real-time"
cover: ./images/veronika-telkomsel/cover.png
metrics:
  - label: Digital channels unified
    value: "6"
  - label: Chatbot sessions handled
    value: "1,000s/hour"
featured: true
draft: false
order: 35
---

## Context
Veronika is Telkomsel's enterprise-grade omnichannel AI chatbot, serving
millions of users across six digital touchpoints — WhatsApp, Instagram,
Facebook, Telegram, a standalone web chat, and the MyTelkomsel app —
automating customer queries that would otherwise queue for a human agent.
It's the most recent and largest-scale system built as a Senior Full Stack
Developer at PT. Dans Multi Pro, within Telkomsel's ecosystem.

## Technical challenge
Millions of users across six heterogeneous channels means message volume
and variety a plain request/response backend can't absorb cleanly — the
system needed to orchestrate messages from all six into one shared AI
engine and back, sustaining thousands of chatbot sessions per hour without
any single channel's traffic spike degrading the others.

## Architecture & decisions
Backend integration services and microservices run on Spring Boot, JPA,
and Python, deployed on Kubernetes via AWS EKS. Kafka handles event-driven
processing and service-to-service communication, Redis provides caching,
and gRPC and SSE (Server-Sent Events) cover synchronous service calls and
real-time web interactions respectively. Decoupling channel ingestion from
AI processing through Kafka — rather than each channel integration calling
the AI engine directly — isolated channel-specific traffic patterns from
the shared AI backend and let channels be added without touching core
orchestration logic.

## Contribution
Architected the backend integration services and microservices unifying
all six channels into the platform, and implemented the Kafka/Redis/gRPC/SSE
layer that lets it sustain thousands of chatbot sessions per hour.
Integrated AI-driven services in collaboration with the dedicated AI team,
connecting AI models to backend services and automating data flows across
all six channels. Also built the React and TypeScript frontend components
providing consistent chatbot interactions across channels.

## Result
Automated customer query handling at a scale — millions of users across six
channels, thousands of concurrent sessions per hour — that would be
impractical to staff with human agents alone, with consistent response
orchestration regardless of which channel a customer used.

## Lesson
Putting Kafka between channel ingestion and AI processing early meant
channel growth — six and counting — never became an architectural problem,
only a configuration one.
