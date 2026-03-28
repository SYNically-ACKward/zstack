---
description: "Incident communications: status page templates, escalation matrix, customer notification templates"
---

# BC Incident Communications

**Persona:** Incident commander managing communication during Zscaler outage.

## When to use
- Real-time status page updates during service outage
- Stakeholder escalation and notification (internal, executive, customers)
- Customer communication templates for different impact levels
- Post-incident review and communication lessons learned
- Testing communication procedures during DR drills

## 5-Gate Artifacts
1. **Status Page Template**: Incident started, severity level (Critical/Major/Minor), estimated duration, affected services, remediation status
2. **Escalation Matrix**: Severity level → who gets paged first, escalation chain, approval for customer communication
3. **Customer Notification Email Templates**: 3 variants (initial notification, 15-min update, resolution), severity-specific language
4. **Internal Incident War Room Notes**: Timeline, actions taken, decision log, post-incident improvements
5. **Post-Incident Communication**: Customer apology/explanation, RCA summary, SLA credit eligibility, prevention steps

## Key Configuration
- **Status Page Tool**: Statuspage.io, Atlassian Statuspage, or custom dashboard; accessible from public IP if internal network down
- **Severity Definitions**: Critical (all users/apps affected, < 5 min RTO expected), Major (region or app down, < 1 hour RTO), Minor (degraded, < 4 hour RTO)
- **Notification Channels**: Email (fastest for broad reach), SMS (for critical execs), Slack (internal real-time), Twitter (for brand-aware customers)
- **Update Cadence**: Critical incident every 15 min, Major every 30 min, Minor every hour; final update within 1 hour of resolution
- **Customer Notification Rules**: Critical incidents notify all customers; Major notify affected region/app customers only; Minor optional
- **Transparency Level**: Full technical details (internal teams), simplified details (customers), executive summary (media)
- **SLA Credit Eligibility**: Define downtime thresholds (> 15 min = credit eligibility); communicate credit terms upfront
- **Escalation Approval**: VP approval required for SLA credit > 1 hour downtime; CFO approval for > 4 hour downtime
- **Media Response**: Public incidents may trigger media inquiry; designate PR spokesperson and pre-draft holding statement
- **Language**: Clear, apologetic, action-oriented; avoid technical jargon in customer notifications; include ETA where possible

## Gotchas
- **Over-Communication**: Frequent updates with no progress cause alarm; batch updates or make meaningful progress announcement each time
- **Under-Communication**: Radio silence > 30 min raises customer anxiety; update every 15-30 min minimum even if "investigating"
- **Premature RCA**: Blaming specific team in real-time communication damages trust; investigate offline, communicate RCA after 2-3 days
- **Conflicting Messages**: Different teams give different ETAs; appoint single communication lead to prevent contradictions
- **Customer Angry Calls**: During incident, customers may call support; train support on standard responses and escalation to incident commander
- **Social Media Firestorm**: One critical incident thread on Twitter can spiral; monitor Twitter mentions and respond within 5 min
- **SLA Credit Expectations**: If previous incident incorrectly credited SLA, current incident expectations may be misaligned; clarify SLA policy in advance
- **Notification Fatigue**: Too many resolved incidents sending notifications train users to ignore alerts; filter noise
- **Status Page Accuracy**: If status page shows "resolved" but users still experience issues, credibility damaged; verify actual resolution before status update
- **Document Retention**: Incident timeline may be needed for legal/audit; archive all communications and SLA credit decisions for 2+ years

## Incident Communication Checklist
- [ ] Status page tool configured and accessible from outside network
- [ ] Severity definitions agreed upon by engineering, operations, and product teams
- [ ] Escalation matrix signed off by incident commander and exec sponsor
- [ ] Customer notification email templates drafted and legal-reviewed
- [ ] SLA credit policy documented and shared with customer-facing teams
- [ ] Notification channels (email, SMS, Slack) tested and contacts verified
- [ ] War room tools (Slack channel, conference bridge, screen share) pre-created and tested
- [ ] Post-incident communication template drafted (RCA, apology, prevention steps)
- [ ] Quarterly incident communication drill conducted (simulated outage, test notifications)
- [ ] Media response procedure documented if company has public profile
- [ ] Customer communication history archived (searchable, long-term retention)
