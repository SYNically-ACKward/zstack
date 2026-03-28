---
description: "Develop risk scoring models that prioritize vulnerability remediation using CVSS, exploitability, and business context"
---

**Risk Analyst** | Zscaler Zero Trust Exchange | Vulnerability Triage Lead

Create vulnerability risk scoring models that combine CVSS metrics, exploit availability, asset criticality, and business context to guide remediation prioritization.

## When to use

- Prioritizing remediation of thousands of vulnerabilities across large environments
- Reducing alert fatigue by surfacing highest-risk issues to remediation teams
- Justifying resource allocation (patching budget, team headcount) to business stakeholders
- Tracking metrics (mean time to remediation per criticality tier) and SLAs
- Correlating vulnerabilities with active exploits and threat intelligence

## 5-Gate Artifacts

1. **Risk Scoring Formula** - Base CVSS + asset criticality weight + exploitability factor + age (older unpatched = higher risk), normalized to 0-100 scale, with tier definitions (90-100 = critical, 70-89 = high, etc.)
2. **Exploitability Enrichment** - Integrate exploit availability (Exploit-DB, Shodan), active exploitation in wild (threat intel), weaponized status (Metasploit modules available), 0-day vs. patched exploit
3. **Asset Context Scoring** - Criticality tiers (production database = 10, test machine = 1), business impact (customer-facing = higher weight), data sensitivity (PII access = multiplier)
4. **Age & Patch Availability** - Days since vulnerability discovery (older = higher risk), patch availability status (patch ready vs. awaiting vendor), SLA countdown (critical unpatched >7 days = max risk)
5. **SLA Tier Definition** - Critical (CVSS 9-10 + exploited) = 24-hour SLA, High (CVSS 7-8 + exploitable) = 7-day SLA, Medium = 30-day SLA, Low = 90-day SLA

## Key Configuration

- **CVSS Enrichment**: Use CVSS 3.1 base scores from NVD; apply temporal metrics (patch available reduces score by 20%), environmental metrics (network scope affects scoring)
- **Exploitability Data Sources**: Combine commercial feeds (Recorded Future, Tenable), public sources (Exploit-DB, GitHub), threat intelligence feeds; weight by recency and accuracy
- **Asset Scoring Database**: Maintain in asset management system (ServiceNow, Qualys Asset View); update criticality tiers quarterly based on business changes
- **Automated Triage**: Rules (CVE in active exploit list → critical, unpatched >90 days → escalate, already patched in latest build → suppress)
- **Reporting by Tier**: Executive dashboard (vulnerability count by tier, SLA compliance), remediation team (sorted by risk score, with patch guidance)

## Gotchas

- CVSS inflation: many medium/low CVEs scored high; implement local calibration (is this really critical in our environment?); track override frequency and refine scoring rules

- Exploitability data lag: public exploit available but not yet in commercial feeds; use GitHub trending, Shodan queries for early detection; implement fast-track scoring for trending exploits

- Asset criticality creep: teams inflate importance of their systems to get faster patching; implement objective scoring (customer impact, regulatory requirement); audit criticality ratings quarterly

- Patch availability gaps: vendor delay in releasing patches; track time to patch and apply higher risk weight during gap period; implement compensating control tracking to lower risk

- Risk score churn: if asset changes criticality or exploit released, score spikes; avoid volatile scoring by applying change thresholds (>20 point change requires review); version scoring methodology

- SLA accountability unclear: remediation team disputes SLA if context missing (patch not available, system requires downtime coordination); include context in SLA calculation; communicate SLA expectations upfront

- Risk score gaming: teams contest scores to get easier SLAs; implement peer review of high-criticality assets and executive sign-off for exceptions; track score appeals and document rationale
