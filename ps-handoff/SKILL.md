---
description: "Operational handoff: runbooks, training plan, day-2 operations guide, support transition"
---

# PS Handoff

You are transferring the keys. Handoff is when the customer becomes independent—they can operate without you. Nail this, and you build loyalty. Botch it, and you own every problem forever.

## When to use

**DO** use PS Handoff when:
- You're in final gate of implementation (Gate 5)
- Go-live is 2–3 weeks away
- You're building training materials & runbooks

**DON'T** use when:
- You're still in design phase
- The system isn't stable enough to document

## The Handoff Triangle

```
        Training
          /  \
         /    \
    Knowledge  Runbooks
       /          \
      /            \
   Confidence     Procedures
```

**You win handoff when:**
1. Customer team has documented procedures (runbooks)
2. Customer team is trained & certified
3. Customer team has been tested under fire (cutover dress rehearsal)

## Training Tier (By Role)

| Role | Training | Duration | Certification |
|------|----------|----------|----------------|
| **Primary Admin** | Architecture + console deep-dive + policies + troubleshooting | 3 days | Written exam (80%+ pass) |
| **Secondary Admin** | Console navigation, policy basics, incident handling | 2 days | Hands-on lab assessment |
| **Network Ops** | Monitoring & alerts, common issues, escalation path | 1 day | Observed cutover support |
| **Help Desk** | User troubleshooting, password resets, device enrollment | 4 hours | Q&A only (no cert) |
| **Executives** | Dashboard reading, SLA metrics, cost visibility | 1 hour | Attendance = completion |

## Runbook Types & Templates

**Daily Operations:**
```markdown
# Daily: Check System Health

Every morning at 9 AM:
1. Log into Zscaler Admin Portal
2. Review Incidents dashboard: any critical alerts? [Y/N]
   - If yes: open ticket, escalate to [phone/email]
3. Check VRI (Visibility, Realizability, Integrity) metrics:
   - User adoption % (target: 95%+)
   - Policy blocks trending (normal range: X–Y)
   - Certificate errors (target: <0.5%)
4. Review overnight logs for anomalies
5. Send status email to [steering group] by 9:30 AM
   - Format: [metric A] | [metric B] | [issues/none]
```

**Weekly Operations:**
```markdown
# Weekly: Policy Review & Optimization

Every Monday, 10 AM:
1. Review blocked traffic report (Insights → Block Events)
   - Any unusual categories? Document for follow-up
   - Are any business-critical apps blocked? Open change request
2. Check DLP incident log: any attempts to exfil sensitive data?
3. Review admin audit log: any unauthorized changes?
4. Test failover: is backup appliance / secondary ZPA gateway healthy?
5. Send weekly digest to [CISO/CTO] by EOD Monday
   - Threats caught, policy changes made, pending escalations
```

**Quarterly:**
```markdown
# Quarterly: Licensing & Capacity Review

Every [month]:
1. Verify user count vs. license allocation
   - Expected growth? Plan ahead.
2. Review bandwidth utilization trends (capacity planning)
3. Audit user roles & permissions (principle of least privilege)
4. Test disaster recovery procedures
5. Schedule 30/60/90-day review with Zscaler PS
```

## Support Transition SLA

**Post-Go-Live (Weeks 1–2):**
```
Zscaler will provide 3 days of on-site/remote engineering support:
  • Critical issues (system down): 1-hour response, 24/7 on-call
  • High (user impact): 4-hour response, business hours
  • Medium (cosmetic): best-effort, 24-hour response
  • Handoff call: 1 hour with customer team to review escalation contacts
```

**After Handoff (Ongoing):**
```
Zscaler support transitions to standard support plan:
  • Customer opens tickets via Zscaler support portal
  • PS is available for architecture questions (not helpdesk-level)
  • Monthly health check calls (optional, fee-based)
```

## Handoff Checklist (Gate 5)

**Documentation:**
- [ ] Architecture diagram (network, policy layers, integration points)
- [ ] Policy matrix (all live policies, change log, approval sign-offs)
- [ ] Admin runbooks (daily, weekly, monthly, quarterly tasks)
- [ ] Troubleshooting guide (common issues, diagnostic steps, escalation)
- [ ] Integration documentation (AD sync, Okta, SIEM, etc.)
- [ ] Disaster recovery procedures (failover, restore, validation)

**Training & Certification:**
- [ ] Primary admin certified (passed exam, score ≥80%)
- [ ] Secondary admin certified (passed lab assessment)
- [ ] Help desk trained (Q&A assessment passed)
- [ ] Steering committee briefed (1-hour readiness review)
- [ ] Training materials delivered (slides, lab guides, reference sheets)

**Cutover Validation:**
- [ ] Cutover dry-run completed (full production-like simulation)
- [ ] Cutover runbook finalized (step-by-step go-live procedures)
- [ ] Rollback procedures tested & documented
- [ ] Incident command structure established (war room, escalation)
- [ ] Customer sign-off: "Ready to go live" (documented email/signature)

**Support & Escalation:**
- [ ] Zscaler PS contact list distributed (architect, engineer, PM, escalation path)
- [ ] Customer escalation matrix documented (who calls whom, when)
- [ ] Support portal access verified (customer can open tickets)
- [ ] SLA terms confirmed (response times, availability, handoff cutoff date)

## Gotchas

1. **Overly detailed runbooks:** If it takes 30 minutes to do a daily task, the customer will skip it. Keep runbooks to 10 minutes max.
2. **Training without testing:** Slide decks don't stick. Hands-on labs are mandatory. 70% of learning = doing.
3. **Disappearing after Day 1:** You promised 3 days of support—be there for all of it. Ghosting kills references.
4. **No escalation path:** If the customer's primary admin quits on Day 5, who do they call? Define it.
5. **Documentation debt:** If the runbooks are vague or outdated in Week 2, the customer will blame you for their problems. Keep them current.

---

**Pro tip:** The best handoff feels invisible to the customer. They don't notice you leaving because they're confident and independent. That's the goal—make yourself unnecessary.
