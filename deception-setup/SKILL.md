---
description: "Deploy Zscaler deception architecture with decoy connectors, alert pipelines, and SOC integration"
---

**Deception Architect** | Zscaler Deception Intelligence Platform | Deception Strategy Lead

Implement enterprise deception platform with decoy infrastructure, cloud integration, and automated alert routing to SIEM and SOC systems for threat detection.

## When to use

- Building initial deception program to detect insider threats and external attackers
- Creating detection infrastructure for lateral movement, credential theft, and data exfiltration
- Integrating deception alerts into existing SOC workflows and incident response processes
- Detecting attackers who evade traditional security controls
- Generating real attack data for threat intelligence and security training

## 5-Gate Artifacts

1. **Deception Architecture Design** - Decoy connector deployment (cloud vs. on-prem), network topology (isolated subnet, full network visibility), physical placement (near critical assets, along exfiltration paths)
2. **Zscaler Integration Plan** - Deception platform API connectivity, alert routing to Zscaler SIEM, correlation with threat intelligence and ZPA logs, credential integration for monitoring
3. **Alert Pipeline Configuration** - Decoy trigger → Zscaler cloud → SIEM (Splunk/ELK) → SOAR (if applicable) → incident ticket, with low-latency design (<5 second end-to-end)
4. **Decoy Placement Strategy** - High-value targets (executive systems, database servers), lateral movement paths (critical servers in network), common attacker objectives (admin credentials, customer data)
5. **Operational Playbook** - Alert triage process (distinguish real threat vs. legitimate access), response escalation (block user, forensic collection), feedback loop (deception coverage tuning)

## Key Configuration

- **Decoy Connector Deployment**: Deploy in DMZ, internal network, and cloud environments; ensure network visibility without detection evasion
- **Credential Management**: Decoy credentials stored in secure vault (AWS Secrets Manager, Azure Key Vault); rotated quarterly; access logged and audited
- **Alert Enrichment**: Decoy trigger includes actor details (IP, username, timing, accessed content), context (was user expecting to access this file?), confidence scoring
- **SIEM Integration**: Export decoy alerts with CEF format; use consistent field naming for correlation with other detection sources
- **False Positive Baseline**: Monitor for legitimate access (IT maintenance, backups); establish whitelist of known benign actors

## Gotchas

- Decoys too obvious (filename "passwords.txt", account "honeypot") avoids detection; use realistic naming that matches business context; test decoys for attacker recognition patterns

- Decoy network isolation too strict (no firewall rules to actual servers) breaks attack chain detection; maintain network paths that enable lateral movement detection; verify connectivity before deployment

- Alert delays (decoy trigger → SIEM lag >30 seconds) miss real-time response window; implement direct webhook integration for <5 second latency; measure end-to-end alerting latency monthly

- False positives from legitimate user confusion (IT browsing decoy file out of curiosity) create noise; require correlation with other risk signals before escalation; track false positive rate and adjust sensitivity

- Attacker awareness (shared reports of "honeypot" accounts circulate in underground forums) reduces effectiveness; refresh decoys quarterly and rotate detection methods; monitor underground chatter for deception platform mentions

- Overfitting deception to known attacks (placing decoys based on past breaches) misses new attack patterns; balance known threat TTPs with exploratory placement; use threat modeling to identify coverage gaps

- Deception platform exposure in incident response: detailed deception architecture disclosed during breach investigation; consider deception infrastructure a sensitive asset with access controls
