---
description: "Deploy and configure unified vulnerability management scanners (Qualys, Tenable, Rapid7) with asset discovery"
---

**Vulnerability Ops Engineer** | Zscaler Zero Trust Exchange | Asset Management Lead

Integrate vulnerability scanners (Qualys, Tenable Nessus, Rapid7 InsightVM) with Zscaler to discover assets and continuously scan for security gaps across cloud and on-premises infrastructure.

## When to use

- Deploying vulnerability scanners across cloud environments (AWS, Azure, GCP) and on-premises networks
- Discovering assets (hosts, services, applications) and mapping to business criticality and data sensitivity
- Choosing between agent-based (endpoint visibility, offline remediation tracking) vs. agentless (network scan, rapid deployment) approaches
- Integrating scanner output with Zscaler threat correlation and risk scoring for incident context
- Scaling scanning across multi-cloud, multi-region environments with centralized management
- Establishing baseline vulnerability metrics and tracking progress on remediation programs
- Meeting compliance requirements for vulnerability scanning (NIST 800-53 RA-3, PCI-DSS 11.2, HIPAA)

## 5-Gate Artifacts

1. **Scanner Deployment & Integration Plan** - Scanner platform (Qualys, Tenable, Rapid7) selected based on coverage (cloud/on-prem/web app/container), API integration method (direct Zscaler sync vs. SIEM intermediary), credentials/service account configuration, multi-tenant support

2. **Asset Discovery Strategy** - Cloud API integration (AWS/Azure/GCP tag-based discovery, auto-scaling support), network-based discovery (CIDR scans, IP range enumeration), agent-based discovery (EDR/Zscaler visibility, sensor network), import from CMDB and orchestration tools (Terraform state, CloudFormation)

3. **Scan Schedule & Scope** - Frequency (critical assets daily, standard assets weekly, low-risk monthly), parallelization (X concurrent scans to limit network impact), excluded networks (development, testing, guest WiFi), maintenance windows for production scanning

4. **Agent vs. Agentless Comparison** - Agent benefits (deep OS inspection, offline remediation tracking, priority scanning), agentless benefits (no deployment overhead, immediate cloud coverage, stateless); hybrid approach common (agents on critical, agentless on standard)

5. **Scanner Health & Reliability** - Credential rotation (90-day service account password changes, API key rotation), certificate management (renewal before expiry), scanner appliance updates (monthly patches), failover configuration (redundant appliances), monitoring and alerting on scanner failures

## Key Configuration

- **Asset Tagging**: Implement consistent asset tags (environment: prod/staging/dev, owner: team, criticality: P1/P2/P3, data sensitivity: public/internal/confidential) for segmented scanning and reporting; automate tag enforcement via cloud policies

- **Discovery Priority**: Automate cloud asset discovery (EC2 instances via ASG, Azure VMs via VMSS, GCP instances via instance groups); use network scans for air-gapped networks; reconciliation monthly to find shadow IT

- **Agentless Scanning**: Deploy scanner from DMZ or cloud VPC with network access to target subnets; use IP/FQDN ranges; monitor for network noise (port scans on customer infrastructure); implement rate limiting

- **Agent Deployment**: Distribute via endpoint management (ConfigMgr, Intune, Puppet) with auto-enrollment; ensure auto-updates enabled (schedule during maintenance window); monitor agent health/reporting (lag >24 hours = alert)

- **Credential Management**: Use service accounts with scan-only permissions; rotate credentials quarterly; implement MFA for scanner admin console access; store credentials in vault (AWS Secrets Manager, HashiCorp Vault)

- **Network Segmentation**: Deploy scanners in management network (separate from production); implement firewall rules for scanner-to-target communication; use encrypted API channels (TLS 1.2+)

## Gotchas

- Asset discovery gaps (new cloud accounts, shadow IT infrastructure) cause incomplete scanning; require monthly reconciliation and automated discovery; measure coverage against infrastructure-as-code sources

- Agent rollout slow on legacy endpoints; use hybrid approach (agents on >90%, agentless on <10%) initially; prioritize critical/production systems for agent coverage

- Scan impact on production (network congestion, CPU spike on scanned hosts) requires coordination; scan during maintenance windows or throttle bandwidth; monitor production metrics during scans (latency, throughput)

- Scanner credentials exposed if database compromised; implement least privilege (scan-only service accounts), credential vault integration, regular audit; rotate API keys monthly

- False positives from scanner (vulnerability dismissed as patch not applicable, OS version mismatch) require manual verification; maintain suppression list and suppress list governance (quarterly review)

- Scanner output delays (24-48 hours from scan to findings available) miss real-time threats; integrate with EDR/Zscaler for fast detection correlation; implement API-based real-time scanning for critical assets

- Scanner misconfiguration (scanning test environments same as production) skews metrics; implement environment-aware scanning with separate policies and dashboards
