---
description: "Build incident response playbooks for Zscaler alerts with containment, forensics, and post-incident analysis"
---

**IR Playbook Author** | Zscaler Zero Trust Exchange | Incident Response Manager

Develop repeatable incident response workflows triggered by Zscaler alerts, with automated containment, forensic data collection, and post-incident review processes.

## When to use

- Responding to malware detection (block, quarantine, forensics, user notification, remediation)
- Investigating suspicious user activity (impossible travel, bulk downloads, privilege escalation, lateral movement)
- Executing data exfiltration incident response (identify stolen data, notify customers, remediate access, legal hold)
- Coordinating incident handoff between SOC, threat intel, and business units (legal, PR, executive leadership)
- Conducting post-incident reviews and improving detection rules (gap analysis, root cause, prevention recommendations)
- Meeting regulatory breach notification timelines (GDPR 72 hours, state laws 60 days, industry-specific requirements)
- Managing incident communication with internal/external stakeholders during active response phase

## 5-Gate Artifacts

1. **Alert Triage Matrix** - Alert type (malware, DLP, anomalous login, threat intel block, lateral movement), severity (critical/high/medium/low) with response SLA, auto-actions (block + notify, quarantine, escalate to incident team), confidence scoring, analyst playbook per alert type

2. **Containment Playbook** - Automated blocks (re-block IP, disable user, revoke API token, kill process), manual investigation steps (gather logs, interview user, check related activities, hunt for similar patterns), escalation path (team lead, CISO, legal, executive), reversibility checks

3. **Forensic Data Collection** - Timeline (when user accessed what, command sequence, files touched), context (source IP, device posture, app used, URL visited with referrer), related events (similar activities by other users, same IP, same tools), preservation of evidence for legal hold

4. **Communication & Notification Plan** - Incident notification (user, manager, legal, executive leadership), customer notification (if customer data involved, regulatory timeline), regulatory reporting (GDPR/state law breach notification, audit documentation), media/public communication if applicable

5. **Post-Incident Review Template** - Incident summary (timeline, scope, impact), root cause analysis (technical, process, human factors), detection gap analysis (why missed, when should have detected), remediation actions with owner/due date, prevention recommendations, lessons learned, accountability assignment, metrics for effectiveness

## Key Configuration

- **Alert-to-Ticket Integration**: Zscaler → SOAR (Splunk SOAR, Palo Alto Cortex XSOAR) → ServiceNow ticket with auto-population of user, asset, threat context, confidence score, recommended actions

- **Automated Containment**: Script user disablement (AD, O365, Okta) with reversibility flag, credential revocation (API tokens, SSH keys, stored passwords), access revocation (file shares, cloud storage), EDR process termination (if applicable)

- **Forensic Data Retention**: Retain Zscaler logs for 365 days (7 years for regulated industries); enable cloud storage audit logging (Azure Audit, AWS CloudTrail, GCS audit logs) for forensics; implement immutable retention for legal hold

- **Escalation Rules**: Critical incidents → immediate paging (5 min SLA response), high → 1hr SLA, medium → 4hr SLA, low → business hours response; auto-escalate if SLA breached

- **Playbook Versioning**: Maintain playbook versions with change log and testing notes; update quarterly or after major incidents; track playbook execution metrics (time to contain, success rate of automated actions)

## Gotchas

- Alert storm during incident can overwhelm manual triage; implement alert aggregation (same user/IP, related threats) to reduce ticket count; use sampling for very high-volume scenarios

- Containment actions (user disablement) must be reversible; verify incident legitimacy before irreversible action (data deletion, permanent access revocation); implement approval workflow for drastic actions

- Forensic data collection delayed by storage/SIEM lag; ensure real-time log export and retain full packet capture for high-risk users; test data availability SLA before incidents

- User notification can complicate investigation (user aware of detection may destroy evidence); coordinate timing with legal/HR before notifying user; implement containment before notification when possible

- Post-incident review often incomplete; make 30-day review mandatory with executive sign-off; escalate overdue reviews to team lead; measure and track follow-up recommendations implementation rate

- Playbook drift (manual workarounds, unapproved changes) happens over time; audit playbook execution quarterly and update to reflect actual practices; measure playbook effectiveness via metrics

- Incident response metrics (MTTR, containment time, blast radius) not tracked; implement automated collection from ticketing system and SOAR; trend quarterly to identify improvement areas
