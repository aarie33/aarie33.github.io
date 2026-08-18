---
id: P-031
title: A Drop of Life
tagline: "Fundraising and donation platform for a Hong Kong charity"
tier: featured
year: 2024
domain: Social Impact
roles: [Dev Lead]
client: "A Drop of Life (Hong Kong)"
stack: [Laravel, Inertia.js, Vue.js]
cover: ./images/fundraising/cover.png
screenshots:
  - src: ./images/fundraising/shot-1.png
    caption: "Campaign management view for A Drop of Life admins"
  - src: ./images/fundraising/shot-2.png
    caption: "Donation flow with PayPal and Stripe payment options"
featured: true
draft: false
order: 31
---

## Context
A Drop of Life is a Hong Kong-based charity running fundraising campaigns.
The platform needed to support both the internal admin side — creating and
managing campaigns — and the public-facing donation flow, with international
payment support since donors were not limited to one region.

## Technical challenge
Payment integration was the crux of it: supporting both PayPal and Stripe
meant handling two different payment provider APIs, webhook flows, and
failure states behind one consistent donation experience, rather than
exposing the provider split to the end user.

## Architecture & decisions
Built on Laravel + Inertia + Vue, with campaign and donation data modeled
independently of payment provider — donations recorded a provider-agnostic
transaction, with PayPal/Stripe-specific handling isolated behind that
boundary. That separation meant adding or changing a payment provider later
wouldn't touch campaign logic at all.

## Contribution
Led the build as Dev Lead: campaign management, the donation flow, and both
payment integrations.

## Result
Gave A Drop of Life a self-service platform for running fundraising
campaigns and accepting international donations directly, rather than
relying on manual or single-provider payment collection.

## Lesson
Isolating payment-provider logic behind a provider-agnostic transaction
model early made supporting two providers only marginally more work than
supporting one.

## Key features
- Admin: campaign management
- Admin: fundraising management
- User: make a donation
- User: payment with PayPal/Stripe
