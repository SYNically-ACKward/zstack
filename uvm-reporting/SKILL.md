---
description: "Create vulnerability dashboards and reports for executives, operations teams, and compliance auditors"
---

**Vulnerability Reporting Analyst** | Zscaler Zero Trust Exchange | Metrics & Analytics Lead

Build automated vulnerability reports and dashboards that serve different audiences: executive risk summaries, operational remediation tracking, and compliance evidence.

## When to use

- Creating executive dashboards showing vulnerability trend (improving vs. worsening), SLA performance, and business impact
- Generating compliance reports mapping remediation to NIST 800-53 controls, CIS benchmarks, or PCI-DSS requirements
- Tracking operational KPIs (MTTR by team, remediation rate, exception aging) for continuous improvement
- Trending analysis (quarter-over-quarter vulnerability count, age of unpatched systems) to support budget requests
- Providing evidence of vulnerability management program to auditors and regulators

## 5-Gate Artifacts

1. **Executive Dashboard** - Vulnerability count by criticality (pie chart), trend (30-day rolling), SLA compliance (% on-time remediation), top vulnerable assets, exception backlog
2. **Operational Report** - Remediation by team (assigned vs. completed), bottlenecks (top blockers for remediation), deployment status (staged, deployed, verified), aging analysis (oldest open vulnerabilities)
3. **Compliance Mapping Report** - NIST 800-53 RA-3 (vulnerability scanning) evidence, CIS benchmark assessment progress, PCI-DSS 11.2 (vuln scanning) compliance, control remediation status
4. **Trend Analysis Dashboard** - Vulnerability discovery rate (new CVEs per month), remediation velocity (resolved per week), age distribution (% >30 days old), SLA adherence trend
5. **Asset-Level Report** - Per-system vulnerability count, criticality breakdown, SLA status, patch currency, last scan date, remediation owner

## Key Configuration

- **Dashboard Frequency**: Executive review monthly, operational team daily, compliance quarterly; automated report delivery via email
- **Metric Definition**: Clarity on SLA start (CVE publication vs. vendor patch release vs. org discovery), exclusions (known false positive vulnerabilities), reset criteria (major scanning tool change)
- **Segmentation**: Trend by asset type (cloud vs. on-prem), business unit (engineering, finance, ops), environment (prod, staging, dev)
- **Visualization**: Use traffic light status (green <20 critical open, yellow 20-50, red >50), trend line showing improvement/degradation
- **Data Quality Checks**: Validate scanner data before reporting (duplicate findings, stale asset records); cross-check with other scanners for coverage gaps

## Gotchas

- Executive dashboard too detailed (all 5K vulnerabilities) defeats purpose; roll up to key metrics only (count by tier, SLA status, trend); measure what matters to business (customer impact, regulatory compliance)

- Compliance report static (manual generation) falls out of sync; automate data pull from vulnerability system quarterly; maintain version control and audit trail of report changes

- Vulnerability count inflation due to scanner tuning changes (new plugin, increased scanning scope) misrepresents trend; normalize by asset count or scope change; document all major changes with notes

- SLA compliance metric gamed: team marks item "remediated" before verification scan confirms patch effectiveness; audit 10% of closed items monthly; require scanner re-scan before closure

- Report latency (data collected Monday, report sent Friday) misses real-time status; use real-time dashboard for live data, reports for historical/audit/trend analysis

- Missing context in trend reports: vulnerability count up 30% but all new discoveries in dev environment, not risky; segment by environment to clarify; implement per-environment SLA tracking

- Compliance mapping errors: vulnerability mapped to wrong control (CVSS vs. business risk); require domain expert review of control mappings annually
