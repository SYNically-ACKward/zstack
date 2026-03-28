---
description: "Vendor assessment: product mapping matrix, risk scoring, gap analysis, discovery checklist for Palo Alto, Check Point, Netskope, Cisco, Symantec, Forcepoint"
---

# Migration Assessment

**Persona:** Network architect evaluating migration from legacy security vendor to Zscaler.

## When to use
- Assessing feasibility of migrating from Palo Alto, Check Point, Netskope, Cisco, Symantec, or Forcepoint
- Identifying feature gaps and compatibility risks before migration
- Creating product mapping matrix to track policy translation requirements
- Quantifying effort and timeline for enterprise-scale migration
- Identifying go/no-go criteria and blockers

## 5-Gate Artifacts
1. **Product Feature Mapping Matrix**: Legacy vendor features → Zscaler equivalent, gap severity (critical/major/minor/non-applicable)
2. **Current State Inventory**: Policy count, user/device count, integration points, customizations, automation dependencies
3. **Gap Analysis Report**: Feature gaps (mitigated vs unmitigated), custom code (3rd-party integration scripts), training needs
4. **Risk Assessment**: Migration risk score (critical/high/medium/low), mitigation strategies, fallback plan
5. **Migration Roadmap**: Phased approach, timeline, resource requirements, success criteria, RTO/RPO targets

## Vendor-Specific Mapping

**Palo Alto Networks (PAN)**
- Prisma Access → ZIA + ZPA
- GlobalProtect VPN → ZPA
- PAN-OS zones → identity-based location/user groups
- App-ID → Zscaler app database
- Threat Prevention (URL, file, command control) → ZIA threat engines
- User-ID → integration with Okta/Azure AD

**Check Point (CP)**
- NGFW/SandBlast → ZIA (URL, threat prevention)
- SmartConsole → Zscaler admin portal
- VPN blades → ZPA
- Gateways → cloud-native gateway replacement
- First-match policy → Zscaler evaluation order (most restrictive first)
- Network objects → user/group objects + location

**Netskope**
- SWG (Secure Web Gateway) → ZIA
- CASB → Zscaler CASB
- NPA (Network Path Access) → ZPA
- DLP engine → Zscaler DLP (3,000+ DLP rules may need remapping)
- Client software → ZCC (remove Netskope client first to avoid conflict)

**Cisco**
- Umbrella SWG → ZIA (roaming client removes before ZPA enrollment)
- AnyConnect VPN → ZPA
- ASA firewall → Zscaler cloud FW
- Umbrella categories → Zscaler URL categories
- TrustSec → workload identity tagging

**Symantec**
- Blue Coat ProxySG / WSS → ZIA
- CloudSOC → Zscaler CASB
- Vontu DLP → Zscaler DLP
- URL categories → Zscaler categories (5-10% mismatch expected)
- Client software → ZCC

**Forcepoint**
- Web Secure Cloud (WSC) → ZIA
- NGFW → cloud-native firewall
- DLP fingerprinting → Zscaler IDM (identity + data)
- UEBA → Zscaler behavioral analytics
- Hybrid agents → cloud-native agent (ZCC)

## Key Configuration
- **Mapping Methodology**: 1) List all legacy policies, 2) Classify by function (URL filtering, threat, DLP, etc.), 3) Map to Zscaler feature, 4) Assess gap
- **Risk Scoring**: Criticality (high if production, low if test) × complexity (1-5) × gap severity (1-5) = risk score
- **Feature Gap Closure**: Unmitigated gaps require mitigation strategy (custom API, workaround, accept risk, or third-party integration)
- **Testing Strategy**: Non-prod validation (mirror policies to lab), production pilot (subset of users/locations), full rollout
- **Rollback Criteria**: Define go/no-go decision points (blockers discovered, RTO > target, critical feature gaps); prepare rollback to legacy
- **User Communication**: Prepare communication plan for users, IT teams, and business stakeholders

## Gotchas
- **Automatic Feature Parity Assumption**: Legacy vendor features may not have direct Zscaler equivalent; custom scripting required
- **Automation Dependency**: If legacy infrastructure relies on vendor APIs (e.g., auto-scaling triggers), Zscaler equivalent may require different architecture
- **Custom URL Categories**: Manually created categories in legacy systems don't auto-migrate; manual review and rebuild required
- **DLP Identifier Complexity**: Some vendors (Netskope, Symantec) use 3,000+ DLP rules; 1:1 migration impossible; consolidation and adjustment needed
- **Policy Language Differences**: Each vendor has different policy evaluation order (first-match vs most-restrictive); policies may behave unexpectedly
- **Client Conflict**: If multiple clients (legacy + Zscaler) run simultaneously, routing and SSL inspection conflicts occur; clean removal essential
- **Documentation Gaps**: Legacy vendor policies may lack documentation; reverse-engineering from live config time-consuming
- **Licensing Assumptions**: Legacy licenses may cover features not explicitly listed; Zscaler licensing structure differs; true cost comparison difficult
- **Operational Skill Transfer**: Teams trained on legacy vendor tools; Zscaler requires new skill development (can't use vendor certifications)

## Discovery Checklist
- [ ] Current vendor identified and version documented
- [ ] Policy count and complexity assessed (simple rules vs complex nested policies)
- [ ] User and device count baseline established
- [ ] Integrations with third-party systems catalogued (AD, SIEM, SOAR, ticketing)
- [ ] Custom code and automations identified and documented
- [ ] URL and DLP custom categories exported and analyzed
- [ ] SSL inspection certificate deployment method understood
- [ ] Performance baselines captured (throughput, latency, policy evaluation time)
- [ ] High-risk policies and exceptions documented
- [ ] Rollback requirement and procedure defined
- [ ] Compliance and audit dependencies on legacy vendor identified
- [ ] Support and escalation contacts obtained

## Configuration Checklist
- [ ] Product mapping matrix completed for all legacy features
- [ ] Gap analysis severity assigned (critical/major/minor) and mitigation planned
- [ ] Risk score calculated for each major policy category
- [ ] Phased migration timeline created (Phase 1-3 with go/no-go gates)
- [ ] Testing environment set up with representative legacy policies
- [ ] Rollback procedure tested and validated
- [ ] Communication plan drafted for users and IT teams
- [ ] Success criteria and measurement approach defined (policy accuracy, RTO, user satisfaction)
