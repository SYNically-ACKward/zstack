# ZStack

**91 Zscaler Professional Services skills for Claude Code and Claude Desktop.**

Built by PS engineers, for PS engineers. ZStack turns Claude into a senior Zscaler architect that knows every configuration knob, every migration gotcha, and every best practice — and produces customer-ready artifacts in the official Zscaler format.

## What it does

ZStack gives Claude specialized knowledge across the full Zscaler portfolio. Instead of generic answers, you get deployment-ready configurations, customer-facing documents, and migration plans grounded in real field experience.

Ask Claude naturally:

```
> Scope a ZIA+ZPA deal for Acme Corp, $2M ARR, 8K seats across NA and EMEA
> Migrate from Palo Alto Prisma Access to Zscaler for a healthcare org
> What does Zscaler recommend for ZPA connector HA in AWS?
> Generate a SOW for a 12-week ZDX + DLP deployment
```

Claude chains the right skills automatically — scoping flows into proposals, migration assessments flow into vendor-specific plans, best practice lookups validate designs.

## Install

**Claude Code (terminal):**

```bash
git clone https://github.com/pganti/zstack.git ~/.claude/skills/zstack
```

**Claude Desktop (Cowork):**

```bash
git clone https://github.com/pganti/zstack.git ~/.claude/skills/zstack
```

Then restart Claude. ZStack skills appear automatically.

## The 5-Gate Lifecycle

Every engagement follows five gates. Each gate produces three artifacts: a config artifact, a client document, and a PS checklist.

**DISCOVER** → **DESIGN** → **IMPLEMENT** → **VALIDATE** → **HANDOFF**

## Skills (91 across 16 categories)

### PS Engagement (6)

| Command | What it does |
|---------|-------------|
| `/ps-scoping` | Map entitlements to service tiers, ARR-based resourcing, SOW-ready scope |
| `/isp` | Implementation Success Plan — 5-gate blueprint with VRI dashboard |
| `/ps-proposal` | Customer-facing proposal with exec summary, approach, timeline |
| `/ps-sow` | **Official ZS-format SOW** from bundled template — fills placeholders, preserves legal boilerplate |
| `/ps-kickoff` | Kickoff meeting agenda, RACI matrix, project charter |
| `/ps-handoff` | Operational handoff package — runbooks, training plan, support transition |

### ZIA — Internet & SaaS Security (6)

| Command | What it does |
|---------|-------------|
| `/zia-policy` | URL filtering, cloud firewall, app control policy design |
| `/zia-ssl` | SSL/TLS inspection — CA management, bypass strategies, compliance |
| `/zia-dlp-inline` | Inline DLP for web traffic — detection rules, incident workflow |
| `/zia-firewall` | Cloud firewall L3/L4 + L7 rules, geo-blocking, IPS |
| `/zia-bandwidth` | Bandwidth control policies — QoS, throttling, app prioritization |
| `/zia-sandbox` | Cloud sandbox / Advanced Threat Protection configuration |

### ZPA — Private Access (6)

| Command | What it does |
|---------|-------------|
| `/zpa-connectors` | App Connector deployment — sizing, HA, network placement |
| `/zpa-segments` | App Segment design — FQDN/IP mapping, wildcard domains |
| `/zpa-policy` | Access policy design — IdP groups, posture checks, segmentation |
| `/zpa-browser` | Browser Access for clientless private app access |
| `/vpn-migration` | Phased VPN→ZPA migration with parallel run + rollback |
| `/zpa-troubleshoot` | ZPA connectivity troubleshooting — connector health, path analysis |

### ZDX — Digital Experience (5)

| Command | What it does |
|---------|-------------|
| `/zdx-deployment` | Probe configuration, alerting, ITSM integration |
| `/zdx-alerting` | Alert thresholds, escalation rules, NOC dashboard setup |
| `/zdx-cloudpath` | CloudPath hop-by-hop analysis for network troubleshooting |
| `/zdx-integration` | ServiceNow, PagerDuty, Slack alerting integration |
| `/zdx-baselining` | 7-day baseline capture, score benchmarking, trend analysis |

### ZCC — Client Connector (4)

| Command | What it does |
|---------|-------------|
| `/zcc-deployment` | ZCC deployment — MDM/GPO, app profiles, forwarding config |
| `/zcc-posture` | Posture profiles — device trust checks, OS compliance |
| `/zcc-troubleshoot` | ZCC troubleshooting — tunnel status, PAC issues, split tunnel |
| `/zcc-update` | ZCC update strategy — rings, rollback, version management |

### Data Protection (7)

| Command | What it does |
|---------|-------------|
| `/dlp-design` | DLP policy design — data classification, EDM/IDM, detection rules |
| `/dlp-edm` | Exact Data Match — index setup, hash management, refresh cadence |
| `/dlp-incident` | DLP incident management workflow — triage, escalation, remediation |
| `/casb-inline` | Inline CASB — real-time SaaS controls, tenant restrictions |
| `/casb-api` | API CASB — out-of-band scanning for M365, Google, Salesforce |
| `/dspm` | Data Security Posture Management — cloud data discovery |
| `/ai-guard` | AI/ML security — prompt inspection, shadow AI discovery, GenAI policy |

### SecOps (5)

| Command | What it does |
|---------|-------------|
| `/secops-log-streaming` | Nanolog Streaming Service — SIEM integration, log formats |
| `/secops-threat-intel` | Threat intelligence feeds, custom block lists, IoC management |
| `/secops-incident-response` | IR playbook for Zscaler-detected threats |
| `/secops-siem-tuning` | SIEM correlation rules, alert tuning, dashboard design |
| `/secops-deception` | Integration between Zscaler Deception alerts and SOC workflow |

### UVM — Vulnerability Management (4)

| Command | What it does |
|---------|-------------|
| `/uvm-setup` | UVM deployment — scanner integration, asset discovery |
| `/uvm-risk-scoring` | Risk scoring model — CVSS enrichment, business context |
| `/uvm-remediation` | Remediation workflows — SLA tracking, patching cadence |
| `/uvm-reporting` | Executive and operational vulnerability reporting |

### Deception (3)

| Command | What it does |
|---------|-------------|
| `/deception-setup` | Decoy Connectors, deployment architecture, alert pipeline |
| `/deception-network-decoys` | Network decoys — SSH, RDP, SMB, database, AD SPN honeypots |
| `/deception-endpoint-lures` | Endpoint lures via ZCC — breadcrumbs, fake credentials, canary files |

### Zero Trust Branch (5)

| Command | What it does |
|---------|-------------|
| `/ztb-design` | ZTB architecture — appliance sizing, topology, HA, VLAN strategy |
| `/ztb-deployment` | ZTP enrollment, cabling, SVI migration, traffic cutover |
| `/ztb-traffic-policy` | Branch traffic policies — DIA, backhaul, app-based routing |
| `/ztb-device-segmentation` | IoT/OT device segmentation at the branch |
| `/ztb-troubleshoot` | ZTB troubleshooting — tunnel health, failover, performance |

### Business Continuity & Regional (5)

| Command | What it does |
|---------|-------------|
| `/bc-design` | BC architecture — customer-hosted PCC or Zscaler-managed DR |
| `/bc-failover-testing` | DR drill planning — quarterly testing, RTO/RPO validation |
| `/bc-config-backup` | Configuration backup strategy — export, version control, restore |
| `/bc-incident-comms` | BC incident communication templates and escalation matrix |
| `/china-premium` | China Premium setup — zscalerone.net, ICP filing, GFW bypass |

### Cloud + Sovereign + Segmentation (4)

| Command | What it does |
|---------|-------------|
| `/zt-cloud-egress` | Cloud workload egress security via ZIA — AWS, Azure, GCP |
| `/zt-cloud-east-west` | East-west traffic inspection in cloud environments |
| `/sovereign-cloud` | Sovereign cloud deployment — data residency, regional compliance |
| `/microsegmentation` | Microsegmentation — east-west policy, workload isolation |

### ITDR + Posture (4)

| Command | What it does |
|---------|-------------|
| `/itdr-setup` | ITDR deployment — AD monitoring, identity risk scoring |
| `/itdr-response` | Identity threat response — compromised credential containment |
| `/posture-control` | Cloud security posture management — misconfig detection |
| `/posture-compliance` | Compliance mapping — CIS, NIST, SOC2, PCI-DSS frameworks |

### Competitive Migration (8)

| Command | What it does |
|---------|-------------|
| `/migration-assessment` | Vendor assessment — product mapping, risk score, discovery checklist |
| `/migrate-palo-alto` | PAN-OS, Prisma Access, GlobalProtect → Zscaler |
| `/migrate-checkpoint` | Check Point NGFW, SmartConsole, VPN blades → Zscaler |
| `/migrate-netskope` | Netskope SWG, CASB, NPA, DLP → Zscaler |
| `/migrate-cisco` | Cisco Umbrella, AnyConnect, ASA/Firepower → Zscaler |
| `/migrate-symantec` | Symantec WSS, ProxySG, Blue Coat, Vontu DLP → Zscaler |
| `/migrate-forcepoint` | Forcepoint WSC, NGFW, DLP, FlexEdge → Zscaler |
| `/migration-cutover` | Cutover runbook — hour-by-hour schedule, rollback, war room |

### Knowledge Base (1)

| Command | What it does |
|---------|-------------|
| `/best-practices-qa` | Query curated Zscaler best practices from ChromaDB vector KB on HuggingFace |

## Skill chaining

Claude chains skills automatically based on context:

- **New engagement** → `ps-scoping` → product skills → `isp` + `ps-proposal`
- **Migration deal** → `migration-assessment` → vendor-specific → `ps-scoping` → `ps-proposal`
- **ZPA deployment** → `zpa-connectors` → `vpn-migration` → `zdx-deployment`
- **Best practices** → `best-practices-qa` before or after any design skill

## Adding a new skill

```bash
mkdir my-new-skill
```

Create `my-new-skill/SKILL.md`:

```yaml
---
description: "One-line description of what the skill does and when to trigger it"
---

You are a senior Zscaler PS architect...
```

Claude discovers it automatically on next session.

## Structure

```
zstack/
├── CLAUDE.md              ← Master registry (Claude reads this first)
├── README.md              ← This file
├── ps-scoping/SKILL.md    ← Each skill is a directory with a SKILL.md
├── ps-sow/
│   ├── SKILL.md
│   └── templates/         ← Some skills bundle templates or scripts
│       └── sow-template.docx
├── best-practices-qa/
│   ├── SKILL.md
│   └── scripts/
│       └── query_kb.py
├── migrate-palo-alto/SKILL.md
├── ... (73 skill directories)
```

## Best Practices QA

ZStack includes a live connection to a curated Zscaler knowledge base hosted at [pganti/zscaler-best-practices-qa](https://huggingface.co/spaces/pganti/zscaler-best-practices-qa). The `best-practices-qa` skill queries ChromaDB vector embeddings of official Zscaler documentation to ground recommendations in authoritative guidance.

## SOW Template

The `ps-sow` skill bundles the official Zscaler PS Statement of Work template. When you ask for a SOW, Claude starts from the real template and fills in the placeholders — preserving the exact section order, legal boilerplate, Zscaler branding, headers, footers, and formatting that Legal has approved.

## License

MIT

## Author

Built by [Paddy Ganti](https://github.com/pganti) — Zscaler Professional Services Engineering.
