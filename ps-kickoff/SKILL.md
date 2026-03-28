---
description: "Kickoff meeting: agenda template, RACI matrix, project charter, stakeholder mapping"
---

# PS Kickoff

You are starting the execution clock. The kickoff meeting sets tone, cadence, and alignment. A tight kickoff saves you 3 weeks of confusion later.

## When to use

**DO** use PS Kickoff when:
- You've signed the SOW and are ready to start
- You're meeting the customer team for the first time (post-contract)
- You need to align roles, expectations, and schedule

**DON'T** use when:
- You're still in proposal stage
- The deal isn't closed yet

## Kickoff Agenda (4 Hours)

| Time | Topic | Owner | Output |
|------|-------|-------|--------|
| 0:00–0:15 | Introductions & goals | You | Rapport established |
| 0:15–0:45 | Project scope review (SOW walkthrough) | You | Scope confirmed |
| 0:45–1:15 | Architecture overview (high-level) | You | Technical alignment |
| 1:15–1:45 | RACI matrix & roles | You | Accountability clear |
| 1:45–2:15 | Success criteria & risks | You | Shared metrics |
| 2:15–2:45 | Communication cadence & escalation | You | Weekly sync structure |
| 2:45–3:00 | Next steps & action items | You | Sprint ready |
| 3:00–4:00 | Optional deep-dive on any topic | Either | Questions answered |

## Project Charter Template

**Project Name:** [Customer] – Zscaler ZIA/ZPA Implementation

**Project Sponsor:** [Customer CEO / CTO / CISO]

**Project Manager:** [Your name / Customer name]

**Start Date:** [Date]
**Target Go-Live:** [Date]

**Business Objectives:**
```
1. Reduce WAN traffic by 40% through local breakout
2. Eliminate legacy VPN; adopt zero-trust access model
3. Improve security posture: reduce lateral movement risk
4. Support 10,000+ remote workers
```

**Scope Summary:**
```
✓ ZIA deployment (cloud firewall, URL filtering, DLP)
✓ Identity integration (AD/Okta sync)
✓ Admin training & runbooks
✓ 3 days post-go-live support

✗ Integration with Splunk SIEM (recommend separate project)
✗ Custom mobile app testing beyond 50 approved apps
```

**Success Criteria:**
```
• 95%+ of users successfully provisioned by Day 30
• 100% of production policies live & tested by cutover
• 0 production incidents on Day 1 go-live
• 100% admin team trained & certified
```

**Key Assumptions:**
```
• Customer provides user list by Week 1
• Customer grants AD/Okta admin access to Zscaler team
• Change control approvals documented in writing
• Customer CISO approves all security policies
```

## RACI Matrix Template

| Task | Responsible | Accountable | Consulted | Informed |
|------|-------------|-------------|-----------|----------|
| Architecture design | PS Architect | Customer CISO | Your CTO | Project sponsor |
| Policy development | PS Engineer | Customer SecOps | Your architect | Compliance officer |
| User provisioning | Customer IT | You (PM) | Okta admin | HR |
| UAT execution | Customer QA | You (PM) | PS engineer | Business owner |
| Cutover runbook | You (PS) | Customer CISO | Your architect | Incident command |
| Admin training | You (PS) | Customer training lead | Your architect | IT staff |
| Escalation path | Your PS director | Customer CIO | Your PS director | Account executive |

**Golden rule:** Every row has ONE accountable. If two people are accountable, no one is.

## Stakeholder Map

```
Steering Committee (Monthly reviews):
  – CEO (project sponsor; budget authority)
  – CISO (security sign-off; policy approval)
  – CTO (architecture decisions)

Working Group (Weekly sync):
  – Your PS project manager (delivery lead)
  – Customer project manager (sponsor representative)
  – Customer network architect (technical counterpart)
  – PS engineer (hands-on deployment lead)

Technical Team (Daily standup):
  – PS engineer (deployment)
  – Customer IT ops (environment access, testing)
  – Customer network ops (cutover support)
```

## Kickoff Artifacts (Deliver in First Week)

1. **Signed Project Charter** (1 page)
2. **RACI Matrix** (table, 1 page)
3. **Stakeholder Contact Sheet** (names, titles, email, escalation)
4. **Gate Timeline** (Gantt chart, realistic dates)
5. **Risk Register** (initial 5–10 items, mitigation owners)
6. **Weekly Sync Cadence** (day, time, standing invite, agenda template)

## Cadence (Non-Negotiable)

```
Daily standup: 15 min, 9 AM customer time
  – What got done yesterday
  – What's blocked
  – Escalations needed

Weekly working group: 1 hour, same day/time
  – Gate progress
  – Risk register review
  – Change requests

Monthly steering committee: 30 min
  – Overall health (green/yellow/red)
  – Budget / timeline status
  – Executive blockers

Ad-hoc architect working sessions: As needed
  – Design refinement, policy deep-dives
```

## Gotchas

1. **No project sponsor:** If no one owns it, it fails. Escalate in kickoff. Get executive commitment before starting.
2. **RACI ambiguity:** "We'll figure it out" is a recipe for blame. Write RACI. Have them sign it.
3. **Vague success criteria:** "Go live" isn't a criterion. "95% of users active + 0 production incidents" is.
4. **Stakeholder surprise:** If you discover new decision-makers in Week 3, you'll rework everything. Surface them now.
5. **No escalation path:** When the CISO blocks a policy, who makes the trade-off call? Define it in the charter.

---

**Pro tip:** A well-run kickoff saves weeks of rework. Invest 4 hours upfront to align 20 people. You'll thank yourself when you're ahead of schedule instead of behind it.
