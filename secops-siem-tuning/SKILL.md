---
description: "Create SIEM correlation rules, dashboards, and alert configurations for Zscaler log analysis"
---

**SIEM Analyst** | Zscaler Zero Trust Exchange | Log Analysis Lead

Develop Splunk/ELK/ArcSight correlation rules that surface security-relevant events from Zscaler logs while reducing alert fatigue through intelligent filtering and enrichment.

## When to use

- Creating correlation rules that detect multi-step attack chains (reconnaissance + exploitation + exfiltration + c&c communication)
- Building dashboards for SOC monitoring (top users, threat categories, geographic anomalies, policy violations, block rates)
- Reducing alert fatigue by correlating related events into single incident; tuning thresholds for signal-to-noise optimization
- Enriching Zscaler logs with context (user department, asset criticality, threat intelligence, risk scores)
- Generating compliance reports from Zscaler logs (access logs, policy violations, audit trails, user behavior anomalies)
- Implementing threat hunting queries on historical Zscaler data to find breach indicators missed by automated alerts
- Supporting incident investigations with fast retroactive log analysis and timeline reconstruction

## 5-Gate Artifacts

1. **Correlation Rule Library** - Rules per attack vector (data exfiltration, C&C communication, lateral movement, privilege escalation), aggregate conditions (same user + multiple threat categories in 5 min window), suppression rules for known false positives, rule version control

2. **SIEM Data Model** - Fields mapping (Zscaler field → CIM field), enrichment (add user department, asset owner, risk score), categorization (access, malware, anomaly, policy violation), index structure for fast queries

3. **Alert Configuration & Tuning** - Alert thresholds (suppress if <5 occurrences/day), scheduling (real-time vs. hourly digest vs. weekly summary), routing rules (Slack for critical, daily email for medium, escalation for trending), deduplication windows

4. **Dashboard & Reporting Suite** - SOC dashboard (top users, threat categories, block rate per hour), executive dashboard (risk trend, policy violations, remediation status, compliance metrics), compliance reports (audit log inventory, retention evidence), threat hunting dashboard

5. **Baseline & Anomaly Tuning** - User behavior baseline (normal login times, typical file transfer volume, accessed applications), deviation thresholds (2+ std dev = alert, require validation), seasonal adjustments (holiday traffic patterns, maintenance windows)

## Key Configuration

- **Correlation Window**: Use 300-second window for attack chain detection (same source, escalating activity); adjust per environment and attack type; document rationale for each rule window

- **Suppression & Deduplication**: Suppress repeated alerts from same source IP for 24 hours; correlate related events (same user, same app) to reduce ticket volume; implement smart suppression based on context

- **Enrichment Lookups**: Add user role, department, asset tier from HR/asset management systems; enrich IP addresses with threat intel, geolocation, ISP information; join with identity data for risk scoring

- **Alert Scheduling**: Real-time alerting for critical rules (malware, DLP block, lateral movement), hourly digest for medium (anomalies, policy violations), daily summary for low (audit events); implement priority queuing

- **Tuning Metrics**: Track alert accuracy (precision = TP/TP+FP, recall = TP/TP+FN); aim for >90% precision to reduce fatigue; measure alert resolution time and false positive investigation cost

- **Rule Testing**: Use historical data to test rule effectiveness before production deployment; measure expected TPR and FPR on test dataset; version control and document rule changes

## Gotchas

- Over-correlation rules create false positives; validate rules against historical data before enabling alerting; measure rule effectiveness on past 30 days of data

- Alert threshold tuning requires baseline collection; don't alert during first 2 weeks of data collection; use weekly stats collection to detect anomalies after baseline matures

- Time-based correlation (daily, hourly) misses off-hours attacks; use 24-hour rolling window for baseline anomaly detection; implement time-of-day normalization for shift-based work patterns

- Enrichment data staleness (user transferred to new department, IP reassigned) creates noise; maintain fresh lookups with daily refresh or real-time sync from authoritative sources

- SIEM parsing errors (malformed CEF, missing fields) break correlation; validate log format quality before enabling rules; monitor parsing error rate and alert on anomalies

- Alert routing decisions (SOC, incident team, business owner) not documented; create runbook for alert routing logic and update quarterly; measure alert routing accuracy

- Correlation rule complexity creep; overly complex rules become unmaintainable; periodically review and simplify rules to ensure team understanding and maintainability
