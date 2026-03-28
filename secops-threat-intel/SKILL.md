---
description: "Integrate threat intelligence feeds, custom blocklists, and IoC management for real-time threat blocking"
---

**Threat Intelligence Lead** | Zscaler Zero Trust Exchange | TI Ops Engineer

Curate custom threat blocklists, import Indicators of Compromise (IoCs) from STIX/TAXII feeds, and tune detection rules to prevent false positives while blocking advanced threats.

## When to use

- Importing indicators from commercial threat feeds (Recorded Future, CrowdStrike, Mandiant, AlienVault OTX)
- Creating custom blocklists (competitor domains, new malware C&C, phishing campaigns, attack infrastructure)
- Reducing false positives from over-broad threat intel (block tech support scam domains, not all .tk domains)
- Sharing internal threat indicators (compromised accounts, known attack infrastructure) across teams
- Compliance threat blocking (OFAC sanctions lists, known malware families per regulation)
- Maintaining historical threat context for incident investigations and breach analysis
- Implementing feed voting (block if 3+ feeds agree) to balance coverage vs. false positives

## 5-Gate Artifacts

1. **Threat Feed Inventory & SLA** - Feed source (Recorded Future IP reputation, AlienVault OTX malware hashes, Shodan, Team Cymru), update frequency (hourly, daily, weekly), confidence threshold per source, TTL, cost/licensing, SLA for feed availability

2. **IoC Import Workflow** - STIX/TAXII ingestion pipeline with format validation, duplicate deduplication across feeds, confidence scoring (1-10 scale), integration with Zscaler blocklists, version control and rollback capability

3. **Custom Blocklist Criteria & Process** - Internal processes (incident findings, threat research, customer context), approval workflow (threat team, legal for OFAC), monitoring for legitimacy (false positive rate <0.1%), sunset policy (re-evaluate quarterly), documentation of rationale

4. **False Positive Reduction Framework** - Whitelist known false positives (legitimate domain sharing infrastructure, CDNs, webhooks, ISP infrastructure), adjust confidence thresholds per industry/region, monitor override requests for patterns, quarterly review of whitelist entries

5. **Operational Metrics & Reporting** - Blocks per threat category (malware, phishing, C&C, ransom), false positive rate trend, time to block new threat (TTB), feed coverage gaps, ROI per feed, block distribution by threat type and geography

## Key Configuration

- **Feed Prioritization**: Combine multiple feeds with weighted voting; commercial feeds (Recorded Future 0.9) higher confidence than community feeds (OTX 0.6); implement voting rule (block if 3+ feeds agree or confidence >0.8)

- **IoC Type Handling**: IP blocklists for direct blocking with GeoIP context, domain blocklists with wildcard support (e.g., *.malicious.com for subdomain variants), URL patterns for phishing, hash-based detection for malware (MD5, SHA1, SHA256)

- **Confidence Scoring**: 1-10 scale; use <5 for early detection with careful monitoring, 7+ for enforcement, 9-10 for manual review before blocking; track score calibration accuracy quarterly

- **Geo-Specific Filtering**: Allow region-relevant threat intel (sanctions list for US business only), disable noisy feeds in non-applicable regions (APT targeting specific countries), implement geo-based tuning

- **Integration with Threat Categories**: Align IoCs with Zscaler threat categories (Advanced Malware, Botnet, Phishing, C&C); enable automated blocking per category; map to MITRE ATT&CK framework for intelligence sharing

- **Feed Rotation & Decommissioning**: Plan feed sunset (notify 30 days before removal), keep IoCs in "monitor" mode before removal to detect operational impact, archive feed for historical threat hunting

## Gotchas

- Over-aggressive threat intel blocks legitimate traffic; manage false positive rate closely (aim for <0.05% of legitimate requests); measure actual impact on business traffic before enforcement

- Threat feed update delays cause gaps in coverage (new malware C&C discovered but feed not updated for 24 hours); cross-reference multiple feeds to reduce single-source risk; implement fast-moving feed tier

- Custom blocklists created reactively during incidents often contain overly broad indicators (entire domain instead of specific subdomain); enforce narrow scoping rules and require incident lead approval

- Geographic IoCs (block all traffic from country X) create compliance and geopolitical liability; consult legal before implementing country-level blocks; implement export control verification for ITAR/EAR

- Threat intel feeds may contain indicators flagged for legitimate services (e.g., Cloudflare IP ranges marked as proxy/VPN, AWS IP ranges as botnet); monitor blocks for false positives and adjust confidence thresholds

- Feed rotation and decommissioning require planning; keep old IoCs in "monitor" mode before removal to detect operational impact; archive feed for 2+ years for historical threat hunting and incident investigation

- Feed credentials (API keys for threat feed access) can be compromised; rotate quarterly, monitor for abuse, restrict IP access to trusted networks
