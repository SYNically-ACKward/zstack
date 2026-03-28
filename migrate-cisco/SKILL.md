---
description: "Migrate Cisco to Zscaler: Umbrella→ZIA, AnyConnect→ZPA. CRITICAL: Umbrella+ZPA documented incompatibility; remove first"
---

# Migrate Cisco

**Persona:** Network engineer migrating from Cisco Umbrella and AnyConnect VPN to Zscaler.

## When to use
- Replacing Cisco Umbrella DNS-layer security with Zscaler ZIA cloud security
- Converting AnyConnect VPN client to Zscaler ZPA for remote access
- Integrating Cisco ISE (Identity Services Engine) user context with Zscaler
- Handling documented Umbrella + ZPA incompatibility (critical blocker)
- Decommissioning ASA firewall appliances in favor of Zscaler cloud FW

## 5-Gate Artifacts
1. **Cisco Security Stack Inventory**: Umbrella deployment (DNS proxy, roaming client version), AnyConnect user count, ISE integration, ASA appliance locations
2. **Umbrella Policy Migration Map**: URL categories, threat policies, proxy enforcement mode → Zscaler equivalents; DNS-layer policies → cloud proxy policies
3. **Roaming Client Conflict Analysis**: Umbrella roaming client must be completely removed before ZPA/ZCC enrollment; removal sequence and validation
4. **AnyConnect Policy Conversion**: Access profiles, group-based policies, authentication backend → Zscaler ZPA access policies
5. **ISE to Directory Integration**: Cisco ISE user groups/attributes → Okta/Azure AD/native AD; Zscaler directory binding

## Key Configuration
- **Umbrella to ZIA**: Umbrella DNS-layer security (malware/phishing/BPaaS filtering) → Zscaler ZIA full proxy (URL, threat, DLP, file inspection)
- **Roaming Client**: Umbrella roaming client provides DNS interception in office and remote; ZCC provides cloud connector + ZPA tunnel; cannot coexist
- **AnyConnect to ZPA**: AnyConnect VPN profiles/policies → Zscaler ZPA access policies; different authentication flow (certificate vs API token)
- **Policy Enforcement Mode**: Umbrella transparent proxy (DNS redirect) vs ZIA explicit proxy; client configuration differs
- **ISE Integration**: If using ISE for device posture, AD group mapping; Zscaler uses directory groups (Okta, Azure AD); requires attribute mapping
- **ASA Firewall**: Cisco ASA (network firewall, VPN termination) can be replaced with Zscaler cloud firewall or retained for on-premises filtering
- **URL Categories**: Umbrella URL categories → Zscaler equivalent; category differences (5-10% variance); custom categories for gaps
- **TrustSec**: Cisco TrustSec (software-defined networking) tags not directly supported in Zscaler; workload identity tagging workaround
- **Compliance Reporting**: Umbrella compliance reports (DNS query logs) → Zscaler reporting via admin portal or SIEM
- **Threat Intelligence**: Both consume threat feeds; Zscaler threat engine may differ; performance/detection variance possible

## Critical Gotcha: Umbrella + ZPA Incompatibility
**Documented Issue**: Cisco Umbrella roaming client and Zscaler ZPA/ZCC cannot run simultaneously. Symptoms:
- DNS queries fail (both clients trying to intercept)
- VPN tunnel drops intermittently
- Routing conflicts (both trying to set default gateway)
- SSL inspection interference

**Resolution**: Completely remove Umbrella roaming client BEFORE ZPA/ZCC enrollment. Test removal thoroughly.

## Client Removal Procedure
1. **Identify Umbrella Client Version**: Check if roaming client, proxy, or DNS interceptor
2. **Backup Config**: Export Umbrella policies and settings before removal
3. **MDM Push Uninstall**: If managed via MDM, push uninstall to all devices; do not proceed until confirmed removal
4. **Manual Verification**: Test 50-100 devices post-removal; confirm DNS resolution works without Umbrella
5. **Wait Period**: Allow 1-2 days for cache clearing and system stabilization
6. **ZCC/ZPA Deployment**: Only then enroll devices in ZPA and deploy ZCC

## Policy Migration Procedure
1. **Export Umbrella Config**: Extract policy rules, user groups, URL categories, threat settings
2. **Classify Umbrella Policies**: Security policies (threat), access policies (bypass rules), reporting rules
3. **Map to Zscaler**: Threat policies → ZIA rules, access policies → ZPA policies, reporting → dashboard config
4. **Convert URL Categories**: Umbrella built-in categories → Zscaler equivalents; document unmapped categories
5. **Test Sample Traffic**: Mirror production traffic; apply Zscaler policies; compare blocking decisions to Umbrella
6. **Pilot with Subset**: Enroll 5-10% of users; monitor for policy gaps before full rollout

## Configuration Checklist
- [ ] Umbrella roaming client version identified and removal procedure validated
- [ ] MDM deployment tested for Umbrella uninstall in non-prod environment
- [ ] Umbrella policy rules exported and categorized (security vs access vs reporting)
- [ ] AnyConnect profiles and access policies documented
- [ ] ISE user groups and attributes mapped to Zscaler directory (Okta/Azure AD)
- [ ] Zscaler ZIA URL categories matched to Umbrella categories; gaps identified
- [ ] ZPA access policies drafted based on AnyConnect policies
- [ ] DNS behavior change communicated (no longer transparent DNS interception)
- [ ] ASA firewall decommissioning or retention plan decided
- [ ] TrustSec tag workaround (if used) designed for Zscaler workload identity
- [ ] Parallel operation plan defined (Umbrella removal → ZCC deployment → ZPA enrollment)
- [ ] Umbrella client removal validation checklist created (50-100 device sample)
- [ ] Rollback procedure documented (how to re-enroll Umbrella if Zscaler issues)
- [ ] Training prepared for users on new security model (cloud proxy vs DNS interception)
