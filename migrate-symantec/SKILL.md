---
description: "Migrate Symantec to Zscaler: WSS/ProxySG→ZIA, CloudSOC→CASB, Vontu→DLP. Gotchas: CPL policy language, URL variance, PAC rewrite"
---

# Migrate Symantec

**Persona:** Network architect transitioning from Symantec ProxySG, Blue Coat, and Vontu DLP to Zscaler.

## When to use
- Replacing Symantec ProxySG (Blue Coat) SWG with Zscaler ZIA
- Migrating Symantec CloudSOC CASB to Zscaler CASB
- Converting Vontu DLP rules and data loss prevention policies to Zscaler DLP
- Translating CPL (Catalyst Policy Language) security policies to Zscaler rule language
- Updating PAC (Proxy Auto-Configuration) files to point to Zscaler instead of ProxySG

## 5-Gate Artifacts
1. **ProxySG/Blue Coat Policy Export**: CPL policy rules, policy objects (networks, users, services), URL categories, ICAP integration points
2. **Vontu DLP Rule Migration**: Vontu fingerprints, identifiers, and custom patterns extracted; Zscaler DLP mapping with identified gaps
3. **PAC File Rewrite**: Legacy PAC files proxying to ProxySG updated to route to Zscaler cloud proxy or ZCC
4. **Policy Translation Matrix**: CPL rules → Zscaler ZIA rules; classification by complexity and risk
5. **CloudSOC/CASB Policies**: Symantec CloudSOC app control and CASB policies migrated to Zscaler CASB equivalents

## Key Configuration
- **ProxySG to ZIA**: Symantec ProxySG (URL filtering, threat prevention, SSL inspection) → Zscaler ZIA; similar functionality, different policy language
- **CPL Policy Language**: Symantec CPL uses condition-based logic (if-then-else, nested conditions); Zscaler uses simpler condition+action model; complex policies simplify
- **URL Categories**: ProxySG maintains extensive URL database; Zscaler app/URL database similar but categories differ; 5-10% variance expected
- **Vontu DLP Integration**: Symantec Vontu DLP (content filtering) → Zscaler DLP; rule translation requires pattern extraction and re-engineering
- **CloudSOC to CASB**: Symantec CloudSOC monitors SaaS apps and enforces policies; Zscaler CASB similar; app definitions and risk scores differ
- **ICAP Integration**: ProxySG uses ICAP for external policy (scanning, custom actions); Zscaler DLP is integrated; ICAP calls removed, DLP rules migrated
- **PAC File Update**: Legacy PAC files route traffic to ProxySG:8080; update to route to Zscaler cloud proxy (https://pceproxy.zscaler.net or regional proxy)
- **SSL Inspection Certificates**: ProxySG uses self-signed certificate for SSL interception; Zscaler cloud uses Zscaler CA certificate; client trust store update needed
- **Proxy Port Configuration**: ProxySG commonly port 8080; Zscaler uses port 80 (HTTP) or 443 (HTTPS); PAC and client configuration updated
- **Authentication Backend**: If ProxySG integrated with LDAP/Kerberos; Zscaler uses directory (Okta, Azure AD); reauthentication architecture differs

## Gotchas
- **CPL Language Complexity**: ProxySG policies leverage CPL nested conditions and variables; 1:1 translation impossible; policy consolidation and simplification required
- **URL Category Mismatch**: ProxySG categories may not perfectly align with Zscaler; custom categories needed for 5-10% mismatches; business impact depends on policies
- **Vontu Fingerprint Conversion**: Vontu uses cryptographic fingerprints for data identification (PII, PCI); Zscaler DLP uses regex/dictionary patterns; fingerprint rules become custom patterns
- **ICAP Chain Removal**: If ProxySG chains multiple ICAP servers (scan + custom action); Zscaler DLP integrated; cascade logic must be rebuilt in Zscaler rules
- **PAC File Deployment Challenge**: If thousands of devices have hardcoded PAC files; centralized DHCP or DNS WPAD required for Zscaler PAC distribution
- **Legacy Proxy Configuration**: Old clients may hardcode ProxySG IP:port; PAC file changes alone may not reach all clients; MDM or Group Policy update needed
- **Performance Perception**: ProxySG on-premises; Zscaler cloud adds latency; users may perceive slower internet; especially noticeable for high-throughput users
- **Policy Audit Trail**: ProxySG audit logs detailed CPL evaluation; Zscaler logs show final action but not policy evaluation; audit log format change
- **Backward Compatibility**: If ProxySG policies reference custom objects or functions; Zscaler equivalent may not exist; manual rule redesign required
- **Proxy Port Expectation**: Some clients hardcoded to port 8080 (ProxySG); Zscaler uses different ports; client reconfiguration needed

## Policy Migration Steps
1. **Export ProxySG CPL Policies**: Use ProxySG UI or API to export policy rules and policy objects (networks, users, services)
2. **Parse CPL Syntax**: Identify condition blocks, actions, nested logic; document policy intent (not just syntax)
3. **Simplify Complex Rules**: CPL nested conditions → Zscaler rules (consolidate multiple ProxySG rules into single Zscaler rule where possible)
4. **Map Policy Objects**: ProxySG network objects, user groups, services → Zscaler equivalents (locations, user groups, applications)
5. **Vontu Rule Extraction**: Export Vontu fingerprints and patterns; identify Zscaler DLP dictionary matches; design custom patterns for unmatched rules
6. **PAC File Generation**: Create Zscaler PAC files (provide templates) and distribution plan (DHCP WPAD, central repository, MDM)
7. **Test Policy Equivalence**: Apply both ProxySG and Zscaler policies to sample traffic; measure enforcement accuracy
8. **Pilot Rollout**: 5-10% of users on Zscaler; monitor policy hits and false positives

## Configuration Checklist
- [ ] ProxySG policy export completed; CPL rule count and complexity assessed
- [ ] Vontu DLP rule export done; fingerprint-to-pattern conversion documented
- [ ] Policy object mapping (networks, users, services) to Zscaler locations/groups completed
- [ ] URL category comparison completed; custom categories created for mismatches
- [ ] PAC file generated and tested in non-prod environment
- [ ] Client proxy configuration strategy defined (DHCP WPAD, Group Policy, MDM, manual)
- [ ] SSL inspection certificate (Zscaler CA) prepared for client distribution
- [ ] CloudSOC policies migrated to Zscaler CASB (if used)
- [ ] ICAP integration removed; policies converted to Zscaler DLP rules
- [ ] Performance baseline established (ProxySG latency vs Zscaler cloud latency)
- [ ] Parallel operation plan created (ProxySG + Zscaler traffic sampling)
- [ ] User communication prepared (new proxy configuration, potential latency change)
- [ ] Rollback procedure documented (revert to ProxySG if issues)
