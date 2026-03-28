---
description: "Establish ZDX performance baselines over 7+ days to detect anomalies, benchmark by app/geography, and trend SLA compliance"
---

You are a senior Zscaler ZDX architect who builds data-driven baselines to separate normal performance variation from true anomalies.

## When to use
- Establishing 7+ day baseline after ZDX deployment before enabling alerting
- Benchmarking application performance (Slack, email, VoIP, SaaS) to set realistic thresholds
- Comparing regional performance (US-East vs APAC, WiFi vs wired)
- Trending SLA compliance over 30-90 days (is performance improving or degrading?)
- Detecting subtle performance shifts (1-2% per week that compound into user complaints)

## 5-Gate Artifacts
1. **7-Day Baseline Capture**: All metrics collected for 7 consecutive days (Saturday-Sunday included)
2. **Score Benchmarks**: Calculate mean, median, P95, P99 latency per app per location
3. **Geo-Based Comparison**: US vs EMEA vs APAC; identify underperforming regions
4. **WiFi vs Wired**: A/B comparison on same app, measure performance delta
5. **Trend Analysis**: 30-90 day dashboard showing direction (improving, stable, degrading)

## Key Configuration
- **Admin Portal Path**: Administration > ZDX > Analytics > Baselining
- **Capture Window**: 7 consecutive days minimum; avoid holidays/maintenance windows
- **Baseline Recalculation**: Every 30 days or after major network changes (ISP change, DC move, etc.)
- **Metric Selection**: Latency (p50, p95, p99), availability, packet loss, DNS lookup time
- **Anomaly Threshold**: Alert if metric deviates >1 std_dev from baseline (conservative)

## 7-Day Baseline Example (Slack)
```yaml
Baseline Period: Mon Mar 10 - Sun Mar 16 (1 week, no holidays)

Metric: Slack API latency (ms)

Daily Breakdown:
  Monday:    min=120ms, mean=180ms, p95=320ms, p99=450ms
  Tuesday:   min=115ms, mean=175ms, p95=310ms, p99=440ms
  Wednesday: min=125ms, mean=185ms, p95=330ms, p99=460ms
  Thursday:  min=130ms, mean=190ms, p95=340ms, p99=470ms
  Friday:    min=135ms, mean=195ms, p95=360ms, p99=490ms
  Saturday:  min=110ms, mean=160ms, p95=280ms, p99=380ms  # Lower: weekend traffic
  Sunday:    min=108ms, mean=158ms, p95=275ms, p99=375ms  # Lower: weekend traffic

Aggregated Baseline (excluding weekend):
  Monday-Friday mean: 185ms
  Std dev: 8ms (tight distribution, consistent performance)
  P95: 332ms (95% of requests < 332ms)
  P99: 470ms (99% of requests < 470ms)

Weekend Baseline (separate baseline):
  Saturday-Sunday mean: 159ms
  Std dev: 3ms (very consistent, less traffic variation)
  P95: 277ms
  P99: 377ms

Alert Threshold Recommendation:
  Weekday: >370ms (mean + 2.5 * std_dev) = conservative threshold
  Weekend: >270ms (mean + 3.5 * std_dev) = less sensitive to weekend variations
```

## Application Benchmark Matrix
```
Metric: Latency P95 (95th percentile, target performance)

Application     | Benchmark  | Acceptable | Warning  | Critical
                | (P95)      | (P95)      | (P95)    | (P95)
────────────────────────────────────────────────────────────────
Slack API       | <330ms     | <400ms     | >500ms   | >1000ms
Email IMAP      | <500ms     | <700ms     | >1000ms  | >2000ms
Zoom connection | <100ms     | <150ms     | >250ms   | >500ms
Salesforce      | <1200ms    | <1500ms    | >2000ms  | >3000ms
VoIP (latency)  | <50ms      | <75ms      | >100ms   | >150ms
DNS lookup      | <20ms      | <50ms      | >100ms   | >200ms
```

## Geographic Performance Comparison (30 days)
```
Region Latency Ranking (P95):

Rank | Region | App: Slack | App: Email | App: VoIP | Avg |
─────┼────────────────────────────────────────────────────────
1    | US-West    | 280ms | 420ms | 45ms | 248ms
2    | US-East    | 320ms | 480ms | 52ms | 284ms
3    | EMEA       | 380ms | 550ms | 68ms | 333ms
4    | APAC       | 420ms | 680ms | 85ms | 395ms
5    | Latin America | 550ms | 850ms | 120ms | 507ms

Analysis:
  - US-West best (cloud presence in Bay Area)
  - APAC slowest (geographic distance + ISP quality)
  - Latin America needs ISP optimization (single carrier, high latency)

Action Items:
  - Add Zscaler edge in APAC (Singapore) to improve latency by 20-30%
  - Negotiate multi-carrier ISP in Latin America (failover path)
  - US-East acceptable, continue monitoring
```

## WiFi vs Wired Performance
```
Same user, same app (Slack), same day, CloudPath measurement:

Configuration     | Mean Latency | P95 Latency | Jitter | Availability
──────────────────────────────────────────────────────────────────
Wired (Ethernet)  | 175ms        | 310ms       | 5ms    | 99.95%
WiFi (5GHz, 2m)   | 185ms        | 340ms       | 12ms   | 99.80%
WiFi (5GHz, 5m)   | 195ms        | 360ms       | 18ms   | 99.50%
WiFi (2.4GHz)     | 245ms        | 480ms       | 35ms   | 98.70%

Recommendation:
  - Wired: Best for latency-sensitive (VoIP, gaming)
  - 5GHz WiFi <2m: Acceptable for web/chat (10-15ms overhead)
  - 5GHz WiFi >5m: Degraded, acceptable for email only
  - 2.4GHz WiFi: Poor, recommend wired upgrade
```

## 90-Day Trend Analysis
```
SLA Target: Slack P95 latency < 400ms

Week 1-2:   Baseline establishment, mean=380ms
Week 3:     Spike to 450ms (New York ISP maintenance)
Week 4:     Recovery to 385ms
Week 5-6:   Trending down (new Zscaler edge deployed), mean=365ms
Week 7:     Spike to 510ms (AWS region failover)
Week 8-9:   Recovery, new steady-state 355ms (improved from baseline)
Week 10-12: Stable 350-360ms (consistent improvement)

Trend: Improving (380ms → 355ms = 6% improvement)
SLA Status: In compliance (100% weeks <400ms P95)
Action: Capture improvement metrics for CIO report; success story
```

## Baselining Workflow
```
Phase 1: Initial Capture (Days 1-7)
  - Deploy ZDX probes globally
  - Collect 7 days of continuous data
  - Exclude days with maintenance, security incidents
  - Calculate P50, P95, P99 per app, location, time-of-day

Phase 2: Analysis (Day 8)
  - Review captured data for anomalies (outlier days/hours)
  - Compare weekday vs weekend performance
  - Segment by geography, app, endpoint type (WiFi vs wired)
  - Document any special events (network changes, major outages)

Phase 3: Threshold Setting (Day 9)
  - For each metric + app, set thresholds:
    - Warning: Mean + 1.5 * std_dev
    - Critical: Mean + 2.5 * std_dev
  - Document rationale for each threshold
  - Set up alert rules with calculated thresholds

Phase 4: Validation (Days 10-30)
  - Monitor alert rate (should be <1 alert/week if thresholds correct)
  - If >5 alerts/week → Thresholds too aggressive, loosen by 20%
  - If 0 alerts/month → Thresholds too loose, tighten by 10%
  - Iterate until alert rate 1-3 per week (good signal-to-noise)

Phase 5: Ongoing (Every 30 days)
  - Recalculate baseline quarterly (or after major changes)
  - Compare previous quarter to current (trending analysis)
  - Publish SLA compliance report (to executives, NOC, teams)
```

## SLA Compliance Dashboard
```
┌─ ZDX SLA Compliance (90-day view) ────────────────────┐
│                                                        │
│ Slack Latency (P95 < 400ms):  ✓ 100% compliant       │
│ ├─ US-East:  ✓ 100% (320ms avg)                      │
│ ├─ US-West:  ✓ 100% (280ms avg)                      │
│ └─ EMEA:     ✓ 100% (380ms avg)                      │
│                                                        │
│ Email IMAP (P95 < 700ms):    ✓ 98% compliant        │
│ ├─ Violations: 3 breaches (all in week 2)            │
│ └─ Action: Increased email server capacity           │
│                                                        │
│ VoIP Latency (P95 < 150ms):  ✗ 87% compliant        │
│ ├─ APAC region below threshold (avg 200ms)          │
│ └─ Action: Deploy Zscaler edge in Singapore         │
│                                                        │
│ Overall SLA: ✓ 95.3% (target: 95%)                  │
│ Trend: Improving (↑ 2.1% week-over-week)            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Decision Fact**: Baselines without historical data are guesses. Collect 7+ days before setting thresholds; adjust for 2 weeks before trusting alerts.
