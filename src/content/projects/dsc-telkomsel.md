---
id: P-033
title: Digital Smart Care (DSC)
tagline: "Enterprise agent-assist platform for Telkomsel's GraPARI customer service"
tier: featured
year: 2025
domain: Internal Tools
roles: [Fullstack Developer]
client: "Telkomsel"
stack: [React, TypeScript, Node.js, NestJS, AWS]
architecture: "Serverless report generation (AWS Lambda + S3) behind Node.js/NestJS APIs, React + TypeScript frontend"
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
customer interactions across Telkomsel's retail network. Built as a Senior
Full Stack Developer at PT. Dans Multi Pro, engaged directly within
Telkomsel's ecosystem, with a focus on the cashier and financial reporting
side agents rely on daily: transaction reports, cashier reports, and
daily/monthly financial reports used by thousands of internal agents.

## Technical challenge
Financial reporting for an operation this size can't just be accurate —
it has to stay fast and searchable for thousands of agents pulling reports
every day, and exportable to Excel/PDF without that generation work
blocking the web servers serving everyone else.

## Architecture & decisions
Reporting APIs run on Node.js (Express) and NestJS, with a React and
TypeScript frontend providing searchable data tables so agents can find
the right report without digging through menus. Report generation itself —
Excel exports and PDF processing — runs on AWS Lambda instead of the main
API servers, with Amazon S3 used to temporarily hold generated PDFs before
download. Moving generation off the request path was the deliberate call:
it kept heavy report jobs from ever competing with agents' regular
day-to-day API traffic.

## Contribution
Enhanced the reporting interfaces (React/TypeScript, searchable tables),
built and maintained the reporting APIs (Node.js/Express and NestJS), and
implemented the serverless report-generation pipeline on AWS Lambda and S3.
Also monitored and troubleshot production issues across the stack — from
the React frontend through backend services to AWS — to keep reporting
reliable for agents.

## Result
The reporting stack stayed reliable and accurate for thousands of daily
users. More broadly, the DSC platform it's part of reduced agent
info-seeking steps by 50% and contributed to Telkomsel achieving an 89.25%
Net Promoter Score at GraPARI outlets.

## Lesson
Pulling report generation out of the request/response path and onto Lambda
was a small architectural decision that paid for itself immediately —
agents never felt report load, no matter how many were being generated at
once.
