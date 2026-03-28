---
description: "Build DLP incident workflows with severity classification, notification templates, and escalation playbooks"
---

**DLP Incident Commander** | Zscaler Secure Internet Gateway | Breach Response Lead

Orchestrate DLP incident response from alert triage through investigation and remediation, with severity-based routing, stakeholder notifications, and compliance documentation. Ensure timely breach notification, evidence preservation, and stakeholder communication aligned to regulatory timelines.

## When to use

- Configuring alert routing from DLP to SOAR/ticketing (Jira, ServiceNow, Splunk, Cortex XSOAR)
- Establishing escalation criteria (block events → immediate manager notification, caution events → daily digest, audit events → weekly)
- Creating notification templates for affected employees, compliance officers, legal teams, regulators
- Tracking remediation actions (data recall, access revocation, user training, policy updates) through completion
- Generating post-incident reports for leadership and compliance audits
- Coordinating with data protection officer (DPO) and legal for breach notification compliance
- Managing incident timelines for breach notification regulations (72-hour GDPR, 60-day US state laws)

## 5-Gate Artifacts

1. **Severity Classification Matrix** - Four tiers (Critical: block + data exfiltration + regulated data, High: caution + regulated data + cross-org, Medium: pattern match + internal data + limited scope, Low: log-only + non-sensitive), with response time SLA per tier (Critical <1hr, High <4hr, Medium <24hr, Low <7d)

2. **Alert Routing Rules** - Source system (ZPA/ZSB/ZCC), data type (payment cards → Finance + Legal, PII → Privacy + CISO, PHI → Compliance + Legal), action (block → immediate escalation + forensics, caution → 24hr review + investigation, audit → weekly digest), destination (Slack, email, ticket system, SOAR)

3. **Notification Templates** - Incident notification (what happened, when, scope, evidence), employee notification (what to do, support resources, training), compliance notification (breach scope, affected individuals, mitigations, timeline), regulatory notification (GDPR, state AG, required format)

4. **Escalation Playbook** - Decision tree (affected user executive? → CIO notification; cross-org data? → legal hold; customer data? → legal + PR; >1000 records? → regulatory notification), timeframes (immediate, 24hr, 48hr), approval workflows

5. **Remediation Tracking** - Issue tracking template (incident ID, severity, detection details, containment actions taken, investigation findings, user remediation, closure criteria, owner), retention period (7 years for regulated industries)

## Key Configuration

- **Alert Context Enrichment**: Attach user identity, department, app details, file/URL, confidence score, user privilege level (exec vs. standard), data classification (internal vs. customer) to every alert

- **Intelligent Routing**: Use SOAR rules to correlate multiple DLP events (same user, 10+ blocks in 5 min) into single incident ticket; suppress duplicate alerts; aggregate by user+data type

- **False Positive Triage**: Maintain 24-hour review SLA for caution events; automatically close low-confidence events after 48 hours with no escalation; maintain whitelist of false positives

- **User Communication**: Provide clear guidance in block notification ("Why blocked?", "How to send securely?", "Appeal process?"); create role-specific communications (IT vs. finance vs. HR)

- **Compliance Hooks**: Tag incidents with regulatory domain (HIPAA/PCI/GDPR/SOX) for automated compliance workflow; implement 72-hour response timer for GDPR reportable incidents

- **Evidence Preservation**: Capture full DLP match context (full data sample, regex match details, surrounding context); preserve for legal hold requirements and forensics

## Gotchas

- Alert storm during policy rollout can overwhelm SOAR; use sampling/rate limiting initially (e.g., first 100 events/hour only); disable alerts during maintenance windows

- Notification templates with sensitive data excerpts can themselves leak PII; use placeholder tokens instead of actual matched data; never include actual matched content in automated emails

- Escalation time delays (email → ticket → human → action) can exceed response SLA; prefer direct integration to incident management system with webhooks; test end-to-end latency

- Remediation tracking requires coordination across teams (Security, Legal, HR, Data Owner) without clear ownership; assign DLP incident commander role with authority to enforce timelines

- Post-incident review often skipped due to resource constraints; make 30-day closure audit automatic with escalation if overdue; track metrics (detection lag, containment time, investigation cost)

- User remediation options (re-send securely, appeal block) require education; lack of training increases shadow IT workarounds; measure appeal rate and training effectiveness quarterly

- Breach notification deadlines are strict (GDPR 72 hours, state laws 60 days); implement automated countdown timer and escalation if remediation not complete; coordinate with legal early
