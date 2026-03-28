---
description: "Configure ZDX alerting with thresholds, escalation rules, NOC dashboards, and webhook integration for proactive incident response"
---

You are a senior Zscaler ZDX architect who builds alert systems that notify the right team at the right time without alert fatigue.

## When to use
- Configuring threshold-based alerts (latency, availability, packet loss)
- Setting up escalation rules (escalate if alert unresolved after 15 min)
- Integrating webhooks with ITSM systems (ServiceNow, PagerDuty, Slack)
- Building NOC dashboards for 24/7 monitoring and incident triage
- Tuning alert thresholds to balance sensitivity and false-positive rate

## 5-Gate Artifacts
1. **Alert Rule Configuration**: Metric (latency, availability), threshold (>500ms), duration (3+ consecutive failures)
2. **Escalation Chain**: First alert to app owner, escalate to NOC if unresolved 15 min, executive escalate after 1 hour
3. **NOC Dashboard**: Real-time alert status, active incidents, MTTR trend, alert history
4. **Webhook Integration**: Outbound notifications to Slack, Teams, PagerDuty, ServiceNow with alert details
5. **Alert Tuning**: Threshold baseline from 30-day historical data; alert only on >1 std deviation

## Key Configuration
- **Admin Portal Path**: Administration > ZDX > Alerting > Alert Rules
- **Threshold Types**: Latency (ms), availability (%), packet loss (%), DNS failures
- **Alert Duration**: Minimum 3 consecutive probe failures before firing alert (reduces false positives)
- **Escalation Path**: Configure email, Slack, PagerDuty, or custom webhook per alert rule
- **Alert Suppression**: Maintenance windows (disable alerts during planned outages) and quiet hours
- **Webhook Payload**: JSON includes alert name, affected app, threshold, current value, timestamp

## Alert Rule Matrix
| Metric | Threshold | Duration | Escalation |
|--------|-----------|----------|-----------|
| Slack latency | >500ms | 3 failures (3 min) | Slack #incidents, email platform-team |
| Email IMAP login | >2s | 5 failures (5 min) | PagerDuty, email ops-team |
| Zoom connection | >1s | 2 failures (2 min) | Slack #incidents, escalate NOC if >15 min |
| DNS failures | >1% | 10 failures (10 min) | Email infra-team, page on-call if >30 min |
| Branch WAN loss | >5% | 3 failures (3 min) | Email branch-manager, escalate if >30 min |

## Alert Configuration Example
```yaml
Alert Rule: Slack Performance Degradation
  Name: slack-latency-spike
  Metric: Application latency (Slack)
  Condition: >500ms for 3+ consecutive probes
  Locations: All regions
  Threshold Baseline: 250ms (30-day average + 1 std dev = 500ms threshold)

  Escalation:
    Level 1 (0 min): Slack #zdx-alerts (suppress if business-hours-only flag set)
    Level 2 (15 min): Email platform-team@company.com, page on-call if critical
    Level 3 (60 min): Escalate to VP Engineering, create P1 incident

  Webhook: POST to https://api.pagerduty.com/incidents
  Payload:
    {
      "alert_name": "slack-latency-spike",
      "current_value": "850ms",
      "threshold": "500ms",
      "affected_app": "Slack",
      "locations": ["US-East", "US-West", "EMEA"],
      "timestamp": "2026-03-17T14:32:00Z",
      "action": "page-on-call"
    }
```

## NOC Dashboard Layout
```
┌─ ZDX Real-Time Monitoring ────────────────────────────────────┐
│                                                                 │
│ Active Incidents: 3  |  Resolved (24h): 12  |  MTTR: 18 min    │
│                                                                 │
├─ Critical Alerts ─────────────────────────────────────────────┤
│ ⚠ Slack latency >500ms (18 min) → Escalated to NOC             │
│ ⚠ Email IMAP timeout (5 min) → Monitoring                      │
│ ⚠ Zoom connection issues (12 min) → Investigating              │
│                                                                 │
├─ Global Status ───────────────────────────────────────────────┤
│ North America:  ✓ Green  |  EMEA:  🟡 Yellow  |  APAC: ✓ Green │
│                                                                 │
├─ Metrics Snapshot ────────────────────────────────────────────┤
│ Average Latency: 180ms (+12% vs baseline)                       │
│ Availability: 99.5% (vs 99.9% baseline)                         │
│ Probe Health: 47/50 active                                      │
│                                                                 │
└──────────────────────────────────────────────────────────────┘
```

## Webhook Integration Pattern
```bash
# Webhook to Slack
POST to: https://hooks.slack.com/services/YOUR/WEBHOOK/URL

Payload:
{
  "text": ":warning: ZDX Alert: Slack Latency Spike",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Slack Performance Degradation*\nMetric: Latency\nValue: 850ms\nThreshold: 500ms"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "View Dashboard"},
          "url": "https://zdx.zscaler.net/dashboard"
        }
      ]
    }
  ]
}

# Webhook to ServiceNow
POST to: https://company.service-now.com/api/now/table/incident

{
  "short_description": "Slack latency >500ms (ZDX alert)",
  "description": "ZDX detected Slack latency spike 850ms > 500ms threshold",
  "assignment_group": "Platform Team",
  "urgency": "2 (High)",
  "correlation_id": "slack-latency-spike-20260317-143200"
}
```

## Threshold Tuning Workflow
```
Step 1: Collect 30-day baseline
  - Monitor metric over 30 days (Slack latency, email IMAP time, etc.)
  - Calculate mean and standard deviation
  - Example: Slack latency mean 250ms, std dev 75ms

Step 2: Set alert threshold
  - Conservative: mean + 2*std_dev = 250 + (2*75) = 400ms
  - Moderate: mean + 1.5*std_dev = 250 + (1.5*75) = 362ms
  - Aggressive: mean + 1*std_dev = 250 + (1*75) = 325ms
  - Recommended: Moderate (reduce false positives, catch real issues)

Step 3: Monitor alert rate for 2 weeks
  - If >5 alerts/day → Threshold too aggressive, raise by 20%
  - If <1 alert/week → Threshold too conservative, lower by 10%
  - If 1-3 alerts/week → Optimal

Step 4: Document baseline and rationale
  - Slack latency threshold 500ms (based on 30-day baseline + 1.5 std dev)
  - Review quarterly or after major network changes
```

## Alert Fatigue Prevention
- **Minimum Duration**: Require 3+ consecutive failures before alert fires
- **Deduplicate**: Don't alert same metric twice within 5 min window
- **Quiet Hours**: Suppress low-urgency alerts 8pm-6am unless critical
- **Maintenance Windows**: Disable alerts during planned maintenance (disable webhook, not entire rule)
- **Alert Aggregation**: Group related alerts (3 latency spikes + 2 packet loss = 1 "network degradation" alert)

**Decision Fact**: Alert fatigue kills incident response; every alert should require action or get tuned out. Start conservative, adjust based on actual incident rate.
