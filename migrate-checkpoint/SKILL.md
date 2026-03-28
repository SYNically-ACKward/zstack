---
description: "Migrate Check Point to Zscaler: NGFW→ZIA, SmartConsole→portal, VPN→ZPA. Gotchas: first-match→eval order, network objects→groups"
---

# Migrate Check Point

**Persona:** Network engineer transitioning from Check Point firewalls and SmartConsole to Zscaler.

## When to use
- Replacing Check Point NGFW (Next Generation Firewall) with Zscaler cloud firewall
- Converting Check Point VPN blade policies to Zscaler ZPA access policies
- Migrating SmartConsole centralized management to Zscaler admin portal
- Translating network-based rules (objects/networks) to identity-based rules
- Managing policy conversion for Check Point Gateways in branch and data center

## 5-Gate Artifacts
1. **SmartConsole Policy Export**: Gateway configurations, rule base export (HTML or CSV), object definitions (networks, services, groups)
2. **Rule Translation Map**: CP rule (source/dest/service/action) → Zscaler rule (user/location/app/action); first-match behavior vs eval-order
3. **Network Object Inventory**: IP networks, user groups, services (ports/protocols); mapped to Zscaler locations, user groups, applications
4. **Custom Services Analysis**: Non-standard ports and protocols in CP; Zscaler app database match or custom app creation
5. **VPN Blade to ZPA Migration**: Remote user VPNs, site-to-site tunnels; converted to ZPA connectors and access policies

## Key Configuration
- **NGFW Migration**: Check Point Gateways (NGFW) handle threat prevention, firewalling, VPN; replace with Zscaler ZIA (threat) + ZPA (access)
- **SmartConsole Replacement**: Central management in SmartConsole → Zscaler admin portal (single pane, multi-tenant optional)
- **Rule Base Conversion**: CP rule base uses first-match rule evaluation; Zscaler uses most-restrictive-match; policy order implications differ
- **Network Objects Translation**: CP uses named objects (networks, service groups); Zscaler uses locations (branches), user groups (Okta/AD), applications
- **Access Control Lists (ACLs)**: CP ACLs (src → dst → service → action) → Zscaler policies (user → app → allow/block)
- **VPN Blade**: Check Point VPN handles remote access, site-to-site, IPSec; replace remote access with ZPA, site-to-site with ZPA connectors
- **Threat Prevention**: NGFW threat blade (IPS, URI filtering, file-based AV) → ZIA threat engines (URL, file, C&C detection)
- **High Availability**: CP active-active/active-passive architecture → Zscaler inherent redundancy (cloud-native, no HA config needed)
- **Management API**: SmartConsole API for automation → Zscaler API for policy management (structure and capabilities differ)
- **Logging & Auditing**: SmartConsole logs aggregated in Check Point; Zscaler logs in cloud dashboard; SIEM integration for historical queries

## Gotchas
- **First-Match vs Most-Restrictive Evaluation**: CP evaluates rules top-to-bottom, first match wins; Zscaler applies most-restrictive rule regardless of order; policy rework needed
- **Network Object Mapping Incomplete**: CP network objects (10.1.0.0/16, marketing-servers) don't directly map to Zscaler; must use user groups (if identity-based) or create manual location mapping
- **Service Port Range Expansion**: CP uses service groups (e.g., web-services: 80, 443, 8080); Zscaler app database may include different ports; custom app needed for non-standard
- **Policy Rule Explosion**: CP policies often use overlapping rules (one rule per src-dst-service); Zscaler policies more consolidated; 1000+ CP rules → 200-400 Zscaler rules (lower density)
- **VLAN and Interface Binding**: CP policies often tied to interface/VLAN; Zscaler location-based (no interface binding); architecture change
- **Logging Verbosity Loss**: CP SmartConsole logs very detailed (connection state, policy evaluation); Zscaler logs more summarized; custom DLP/threat rules needed for details
- **High Availability Implications**: CP active-active setup (both gateways processing traffic); Zscaler cloud HA transparent; if traffic steering depended on active/active, rethink architecture
- **Custom Endpoint Protection**: Check Point Smart Defense (mobile device management) may be separate; Zscaler has ZCC (light client) but different feature set; gaps possible
- **LDAP Integration**: CP SmartConsole integrates with LDAP for user management; Zscaler requires Okta/Azure AD/native AD; migration may need consolidation
- **Rule Audit and Change Management**: If SmartConsole audit logs critical for compliance, Zscaler audit format differs; custom SIEM parsing required

## Rule Migration Procedure
1. **Export SmartConsole Config**: Use SmartConsole export or manual rule documentation
2. **Parse Rule Base**: Extract each rule (source, destination, service, action) and gateway it applies to
3. **Consolidate Overlapping Rules**: Identify redundant or overlapping CP rules; simplify for Zscaler (fewer, more general rules)
4. **Map to Zscaler Structure**: Create lookup table (CP service → Zscaler app, CP network → Zscaler location/group)
5. **Build Zscaler Rules**: Translate each consolidated CP rule to Zscaler policy; test in non-prod
6. **Identify Gaps**: Services/objects without direct match; design custom rules or accept traffic pattern change
7. **Directory Integration**: Set up user/group mapping (LDAP → Okta/Azure AD → Zscaler)
8. **Parallel Operation**: Run CP and Zscaler rules simultaneously on pilot traffic; compare enforcement

## Configuration Checklist
- [ ] SmartConsole rule base exported and rule count verified
- [ ] Network objects (networks, service groups) documented and mapped to Zscaler locations/apps
- [ ] Gateway deployment (branch, data center) and policy distribution confirmed
- [ ] VPN blade users and site-to-site tunnels inventoried for ZPA migration
- [ ] First-match vs most-restrictive evaluation difference reviewed with security team
- [ ] Threat prevention policies (IPS, URI filtering) mapped to ZIA equivalent
- [ ] High availability configuration documented and redesigned for cloud-native
- [ ] Custom services (non-standard ports) identified; Zscaler app match or custom rule created
- [ ] LDAP/AD integration reviewed; Okta/Azure AD integration planned
- [ ] Policy translation template validated on sample 50-100 rules
- [ ] Parallel operation window (CP + Zscaler traffic) defined and resources allocated
- [ ] Rollback procedure documented (how to revert to CP if Zscaler issues occur)
