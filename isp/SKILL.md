---
description: "Implementation Success Plan — 5-gate blueprint, VRI dashboard, milestones, deliverables per gate"
---

# Implementation Success Plan (ISP)

You are the orchestrator. The ISP is your blueprint—it tells everyone (customer, your team, leadership) exactly what happens when, who owns it, and how we measure success.

## When to use

**DO** use ISP when:
- You're building the project charter
- Customer needs a roadmap they can show their steering committee
- You want to reduce scope churn by creating a defined structure
- You're running a multi-gate project (most enterprise deals)

**DON'T** use when:
- The customer wants a 2-week quick-start (use a simple 1-gate kickoff instead)
- You haven't scoped the work yet

## The 5-Gate Blueprint

| Gate | Timeline | Customer Deliverable | Acceptance Criteria |
|------|----------|----------------------|-------------------|
| **1. Prep** | Week 1–2 | Project charter, RACI, stakeholder list | Signed approval |
| **2. Design** | Week 3–4 | Architecture diagram, policy framework, risk register | Customer arch signoff |
| **3. Build** | Week 5–8 | Configured system, test cases, user guides | UAT environment ready |
| **4. Test** | Week 9–10 | UAT results, remediation log, cutover plan | Go-live decision made |
| **5. Handoff** | Week 11–12 | Runbooks, training certs, support handoff | Customer independence verified |

## Key Metrics

Track these in your VRI (Visibility, Realizability, Integrity) dashboard:

```
Visibility:
  - Days on-time to each gate
  - Change requests vs. committed scope
  - Risk items trending (open → closed)

Realizability:
  - Engineering hours vs. estimate
  - Rework rate (% of work redone)
  - Customer blocking issues count

Integrity:
  - Acceptance criteria met per gate
  - UAT pass rate
  - Production incidents post-go-live (target: 0)
```

## 5-Gate Deliverables

**Gate 1 (Prep):**
- Project charter (1–2 pages)
- RACI matrix (responsible, accountable, consulted, informed)
- Stakeholder contact sheet (names, titles, escalation paths)
- Project timeline (Gantt or narrative)

**Gate 2 (Design):**
- Architecture diagram (network, policy layers, integration points)
- Policy framework document (URL filtering, firewall, DLP rules)
- Risk & mitigation register
- Testing approach (unit, integration, UAT)

**Gate 3 (Build):**
- Deployed system with production-like config
- User acceptance testing plan & test cases
- Admin & end-user training materials
- Support transition plan

**Gate 4 (Test):**
- UAT results summary (pass/fail by test case)
- Remediation log (open issues + resolution)
- Cutover runbook (pre-flight, go-live steps, rollback)

**Gate 5 (Handoff):**
- Operational runbooks (daily, weekly, monthly tasks)
- Training completion certificate list
- Support ticket templates
- 30/60/90-day review agenda

## Gotchas

1. **Gate creep:** Don't let customers add new gates. The 5-gate model is proven. Variations cause delays.
2. **Skipping risk register:** Make it real from Day 1. Update it weekly. It's your safety net.
3. **"UAT is optional":** It's not. UAT catches 80% of problems before production. Budget for it.
4. **No owner per deliverable:** Assign a single owner (customer or you) for each gate artifact. Ambiguity kills schedules.
5. **Cutover surprises:** Test the cutover plan in a lab. Never do it cold.

---

**Pro tip:** An ISP isn't for you—it's for the customer's steering committee. Make it accessible, use simple language, and update it weekly. A project with a visible, credible roadmap stays on track.
