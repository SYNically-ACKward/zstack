---
description: "Migrate Palo Alto to Zscaler: Prisma Access→ZIA/ZPA, GlobalProtect→ZPA, zones→identity policy, App-ID→apps"
---

# Migrate Palo Alto

**Persona:** Network engineer migrating from Palo Alto Panorama and Prisma Access to Zscaler.

## When to use
- Transitioning Prisma Access (cloud firewall) to Zscaler ZIA (threat prevention) and ZPA (access)
- Converting GlobalProtect VPN policies to Zscaler ZPA access policies
- Mapping PAN-OS zones and security policies to identity-based access in Zscaler
- Converting custom App-ID signatures to Zscaler app database
- Retiring Panorama centralized management in favor of Zscaler admin portal

## 5-Gate Artifacts
1. **Prisma Access & GlobalProtect Inventory**: Device count, policy count, user groups, URL categories, custom App-IDs, decryption rules
2. **Policy Translation Mapping**: Each PAN policy → Zscaler rule (source/destination, app, action); zone-based rules → identity-based rules
3. **App-ID Custom Signature Analysis**: Custom app IDs identified, Zscaler app match attempted, unmatched apps require custom handling
4. **Risk Matrix**: Routing conflicts (GlobalProtect + ZCC), policy evaluation order differences, certificate pinning issues
5. **Cutover Runbook**: Parallel operation period, traffic steering sequence, rollback criteria, validation checkpoints

## Key Configuration
- **Prisma Access to ZIA**: Migrate threat prevention (URL filtering, file type control, command control) to ZIA; DLP from Prisma → Zscaler DLP
- **GlobalProtect to ZPA**: Replace GlobalProtect client enrollment with ZCC enrollment; GlobalProtect policies → ZPA access policies
- **Zone Mapping**: PAN zones (Trust, Untrust, DMZ) don't exist in Zscaler; replace with user/location-based access rules
- **Security Policy Translation**: PAN policy (source → dest → app → action) → Zscaler rule (user/device → app → allow/block/log)
- **App-ID Dependency**: PAN App-ID identifies apps (Salesforce, Office 365, etc.); Zscaler app database is more comprehensive; custom apps require custom category
- **Panorama Deprecation**: Zscaler centralized admin portal replaces Panorama; RBAC, audit, deployment similar but different interface
- **Decryption Policy**: PAN uses application profiles for decryption control; Zscaler applies threat inspection to all TLS traffic by default
- **Service Chain**: If Panorama integrated with other PAN services (cloud management, Cortex), decommission or migrate separately
- **LDAP/Active Directory**: Convert PAN user mappings to Zscaler directory integration (Okta, Azure AD, native AD)

## Gotchas
- **GlobalProtect + ZCC Routing Conflict**: Both are VPN clients; if GlobalProtect not fully removed, traffic routing ambiguous (can use both interfaces); uninstall GlobalProtect first
- **Zone-to-Identity Conversion Challenge**: PAN zones static (by network); Zscaler requires user/device attributes; conversion non-trivial for subnet-based rules
- **Custom App-ID No Direct Translation**: PAN custom App-IDs built on protocol/port/signature; Zscaler app database may not match; custom categories may need business logic workaround
- **Policy Evaluation Order Difference**: PAN uses first-match; Zscaler uses most-restrictive; policy order matters; test extensively
- **Certificate Pinning Issues**: If clients pin Prisma Access certificate, switching to Zscaler causes cert validation failures; distribute new cert or update client
- **Decryption Expectation Mismatch**: PAN policies control which apps to decrypt; Zscaler decrypts by default; some users may view as privacy concern; set expectations
- **URL Category Mismatch**: Some PAN categories may not align perfectly with Zscaler categories (5-10% variance); gaps require custom category rules or accept risk
- **Throughput Perception**: Zscaler cloud-based architecture; WAN optimization features from Prisma not present; latency and throughput may feel different
- **Multi-Tenant Panorama**: If managing multiple customers, Zscaler multi-tenancy requires account structure redesign; no API-driven tenant provisioning like Panorama
- **Incident Correlation**: Panorama logs all incidents in central console; Zscaler logs distributed across cloud; incident correlation requires tooling (SIEM integration)

## Policy Migration Steps
1. **Export PAN Configuration**: Use `show config running` or Panorama API to export XML config
2. **Parse Policy Rules**: Extract security policies, zones, user groups, custom App-IDs, URL categories
3. **Build Zscaler Policy Matrix**: For each PAN rule, determine Zscaler equivalent (user/location/app/action)
4. **Identify Gaps**: Custom App-IDs without Zscaler match, zone-based rules without user attribute mapping
5. **Create Custom Categories**: For unmatched App-IDs, create custom URL categories or DLP rules
6. **Directory Integration**: Set up Okta/Azure AD integration in Zscaler; map PAN user groups to directory groups
7. **Test Policies**: Parallel test environment (mirror production, run both PAN and Zscaler rules, compare enforcement)
8. **Incremental Rollout**: Phase 1 (pilot users), Phase 2 (department), Phase 3 (enterprise)

## Configuration Checklist
- [ ] Panorama/Prisma Access inventory exported and policy rule count confirmed
- [ ] GlobalProtect enrollments and device count documented
- [ ] User groups and directory integration points identified
- [ ] Custom App-IDs analyzed and Zscaler app equivalents researched
- [ ] Zone-to-identity mapping strategy defined (IP ranges vs directory groups)
- [ ] Policy translation template created and sample rules validated
- [ ] Decryption expectation and privacy implications communicated to security team
- [ ] Client rollout plan created (ZCC deployment schedule, GlobalProtect removal procedure)
- [ ] Directory integration (Okta, Azure AD) tested and group mappings verified
- [ ] Parallel operation period defined (simultaneous PAN + Zscaler traffic)
- [ ] Rollback criteria and procedure documented (e.g., if Zscaler policy misses 5% of enforcement)
- [ ] Performance baseline established (latency, throughput) to validate Zscaler performance
