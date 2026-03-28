---
description: "Manage vulnerability remediation lifecycle with SLA tracking, patching cadence, and compensating controls"
---

**Remediation Manager** | Zscaler Zero Trust Exchange | Patch Management Lead

Execute vulnerability remediation programs with SLA enforcement, tracking patch status across systems, managing exceptions, and implementing compensating controls where patches unavailable.

## When to use

- Tracking patch deployment and verifying remediation completeness
- Managing remediation exceptions (system not yet patched due to compatibility, business justification)
- Implementing compensating controls (WAF rule, network segmentation) when patching delayed
- Reporting SLA compliance to compliance teams and business stakeholders
- Coordinating with infrastructure teams on patching schedules and maintenance windows

## 5-Gate Artifacts

1. **Remediation Tracking Workflow** - Vulnerability detected → assigned to team owner → patch identified → tested in staging → deployed → verified with re-scan; status workflow (Open → In Progress → Staged → Deployed → Verified)
2. **Exception Management Process** - Justification required (incompatible with production app, vendor hasn't released patch), approval (manager + security), compensating control (WAF rule, network block), re-evaluation date (quarterly)
3. **Patching Schedule & Cadence** - Monthly patch cycle (Tuesday after 2nd Monday), priority grouping (critical patches deployed within 24 hours, others batched), maintenance windows (weeknight 2am, low-traffic windows)
4. **Compensating Control Mapping** - Vulnerability → firewall rule (block inbound exploit), WAF signature (detect exploit attempt), network segmentation (isolate vulnerable service), monitoring rule (alert on exploitation)
5. **Remediation Metrics & Reporting** - SLA compliance by criticality, mean time to remediation (MTTR), exception aging (remediation >30 days justified), compensating control effectiveness (# exploits detected vs. blocked)

## Key Configuration

- **SLA Enforcement**: Critical = 24hr, High = 7d, Medium = 30d, Low = 90d; escalate overdue items to team lead, then management
- **Patch Testing**: Run patches in staging environment before production (system rebuild time <2 days); use automated testing (vulnerability re-scan, regression tests)
- **Re-scan Verification**: Run scanner 24-48 hours after patch to confirm remediation; track remediation confirmation rate
- **Exception Audit**: Monthly review of all open exceptions; require business justification; escalate >90-day old exceptions
- **Compensating Control SLA**: If patch delayed >7 days, implement compensating control within 24 hours; document control effectiveness

## Gotchas

- Patch conflicts (multiple patches require different reboot timings) cause deployment delays; coordinate with infrastructure teams and plan sequencing; pre-validate patch compatibility before deployment

- Remediation verification lag: scanner doesn't immediately confirm patch applied; use EDR agent reports for faster verification; implement post-patch validation testing before closure

- Exception drift: exceptions created with business justification but never re-evaluated; implement mandatory quarterly re-review with escalation; track exception aging and escalate >90 days old

- Compensating control false sense of security: WAF rule blocks obvious exploit but advanced attacker bypasses it; treat as temporary, not permanent solution; implement control effectiveness monitoring

- SLA creep: initial SLA (24 hours) too aggressive, teams request extensions; set realistic initial SLA based on deployment capacity; measure MTTR and adjust SLA annually based on historical data

- Legacy systems (unsupported OS, vendor out of business) have no patches; maintain inventory of unsupported systems and prioritize replacement over patching; track cost-benefit of continued operation

- Patch rollback failures: patch causes regression (app downtime, data corruption); implement easy rollback procedures; test in staging with production-equivalent data; track successful rollback rate
