---
description: "Migrate Netskope to Zscaler: SWG→ZIA, CASB→CASB, NPA→ZPA, DLP→DLP. Gotchas: 3000+ rules, client conflict, console separation"
---

# Migrate Netskope

**Persona:** Security architect transitioning from Netskope unified platform to Zscaler modular architecture.

## When to use
- Replacing Netskope SWG (Secure Web Gateway) with Zscaler ZIA
- Migrating Netskope CASB capabilities to Zscaler CASB module
- Converting Netskope NPA (Network Path Access / Zero Trust Network) to Zscaler ZPA
- Handling Netskope DLP rule migration (3,000+ rules, identifier mapping)
- Unifying fragmented Zscaler portals (separate ZIA, ZPA, CASB consoles vs single Netskope console)

## 5-Gate Artifacts
1. **Netskope Appliance/Agent Inventory**: On-premises appliance count, roaming client deployment, cloud security module (CSM) servers, policy count
2. **DLP Rule Migration Analysis**: Netskope identifier list (3,000+ rules) mapped to Zscaler DLP dictionaries; unmatched identifiers documented
3. **Policy Consolidation Map**: SWG policies → ZIA rules, NPA policies → ZPA access policies, CASB rules → Zscaler CASB policies
4. **Client Software Transition Plan**: Netskope client removal schedule, ZCC deployment timing, coexistence risks identified
5. **Multi-Console Operational Model**: Transition from single Netskope console to Zscaler ZIA/ZPA/CASB three-portal model; training and SOPs

## Key Configuration
- **SWG to ZIA**: Netskope Secure Web Gateway (URL filtering, threat prevention, file inspection) → Zscaler ZIA cloud proxy
- **NPA to ZPA**: Netskope NPA (zero-trust network access, micro VPN) → Zscaler ZPA (application access control)
- **CASB to CASB**: Both vendors offer CASB; Zscaler CASB detects/blocks unauthorized cloud apps, enforces DLP; Netskope CASB similar; migrate cloud app policies
- **DLP Rule Complexity**: Netskope includes 3,000+ built-in DLP identifiers (PII, PCI, HIPAA, etc.); Zscaler DLP uses dictionary-based approach; 1:1 mapping impossible; consolidation needed
- **Client Architecture**: Netskope uses unified roaming client; Zscaler has separate ZCC (cloud connector) for ZPA; cleanup and clean install required
- **Management Portals**: Netskope single console; Zscaler has ZIA admin portal, ZPA admin portal, CASB portal; separate logins and UIs; training needed
- **Identity Integration**: Both support Okta/Azure AD; Zscaler implementation identical; user group mapping carries over
- **Threat Intelligence**: Both consume threat feeds; Zscaler threat engines may differ; performance/detection variance possible
- **Logging and Analytics**: Netskope unified logging; Zscaler logs distributed; SIEM integration required for unified view
- **API Automation**: Netskope API vs Zscaler API; automation scripts require refactoring

## Gotchas
- **3,000+ DLP Rule Remapping**: Netskope includes comprehensive DLP library; Zscaler DLP focuses on common use cases; 30-40% rules require custom mapping or acceptance of gaps
- **Client Conflict**: Netskope and Zscaler clients cannot run simultaneously; if not cleanly removed, routing and SSL inspection conflicts; careful MDM orchestration required
- **Unified Console Loss**: Users accustomed to single pane of glass in Netskope; three Zscaler portals perceived as fragmented; requires documentation and training
- **URL Category Variance**: Netskope URL categories may not 100% align with Zscaler; gaps in category classification (5-15% variance); custom categories mitigate
- **CASB Confidence Score Difference**: Netskope CASB uses different risk scoring than Zscaler CASB; policies using score thresholds need adjustment
- **Policy Evaluation Order**: Both use similar rule evaluation; less risky than PAN-Check Point migration, but subtle differences possible
- **Threat Intelligence Feed Timing**: Zscaler threat feed updates may lag Netskope in edge cases; performance during fast-moving threat may differ
- **NPA to ZPA Mindset Shift**: Netskope NPA is VPN replacement (all traffic through tunnel); ZPA is application-centric (traffic routed based on app access policy); significant architecture rethink
- **Client Removal Timing**: Removing Netskope before ZPA fully deployed leaves gap period with no client protection; coordination critical
- **Legacy Appliance**: If on-prem Netskope appliance decommissioned, ensure all policies migrated; appliance shutdown before migration completion causes disruption

## DLP Rule Migration Strategy
1. **Export Netskope DLP Rules**: Extract all custom DLP rules, identifiers, and exceptions
2. **Classify by Impact**: Critical (finance, health, legal), High (customer data), Medium (internal confidential), Low (nice-to-have)
3. **Map to Zscaler DLP**: For each rule, identify Zscaler DLP dictionary match (90%+ exact match candidate)
4. **Document Gaps**: Remaining unmapped rules; assess if gap acceptable or custom rule required
5. **Custom Rule Development**: Build Zscaler custom DLP rules for critical unmapped rules (regex-based patterns)
6. **Test on Sample Data**: Apply Zscaler rules to historical data; compare detection accuracy to Netskope
7. **Accept Risk or Enhance**: If gap acceptable, document exceptions; if not, enhance custom rules

## Configuration Checklist
- [ ] Netskope appliance and roaming client count documented
- [ ] SWG policies exported and migrated to ZIA rules
- [ ] NPA policies documented and converted to ZPA access policies
- [ ] CASB cloud app policies migrated to Zscaler CASB
- [ ] DLP rule export completed; critical rules identified and mapped to Zscaler DLP
- [ ] Custom DLP rules created for unmapped critical identifiers
- [ ] Client removal schedule created and MDM deployment tested
- [ ] ZCC deployment validated in non-prod environment
- [ ] Identity integration (Okta/Azure AD) tested and group mappings verified
- [ ] Parallel operation period defined (simultaneous Netskope + Zscaler)
- [ ] Multi-portal training prepared for operations team
- [ ] SIEM integration configured for unified logging (Netskope + Zscaler)
- [ ] Rollback procedure documented (how to restore Netskope if Zscaler issues)
- [ ] DLP gap risk assessment approved by information security officer
