---
description: "Deploy inline CASB controls for real-time SaaS access enforcement, tenant restrictions, and user coaching"
---

**Cloud Access Security Broker** | Zscaler Zero Trust Exchange | SaaS Security Lead

Implement real-time Cloud Access Security Broker (CASB) policies that block risky SaaS usage, enforce tenant boundaries (M365/Google), and guide users toward compliant behavior. Prevent cloud service misuse while maintaining user productivity through contextual coaching and approved service alternatives.

## When to use

- Restricting access to unapproved SaaS instances (shadow IT elimination)
- Enforcing Microsoft 365 or Google Workspace tenant boundaries (block personal accounts and unauthorized domains)
- Preventing risky file operations (upload to personal cloud storage, sharing with external users, public link generation)
- Providing user education through inline coaching pages ("This app is not approved—use Slack instead")
- Protecting against token theft and insider threats in cloud apps
- Meeting compliance requirements (SOC2, HIPAA) for approved-app-only policies
- Scaling policy enforcement across geographically distributed workforces with consistent rules

## 5-Gate Artifacts

1. **SaaS Inventory & Risk Scorecard** - Catalog of apps (name, category, risk rating, compliance gaps, data sensitivity), approved/restricted/caution lists with business justification, business owner assignments, estimated user base per app

2. **Tenant Restriction Matrix** - M365 allowed tenants (Contoso.onmicrosoft.com only), Google allowed domains (corp.company.com, partner.com), conditional allow rules (HR to all domains, everyone else restricted), federated identity restrictions

3. **File Operation Policies** - Upload block to personal cloud storage, prevent sharing with external users, quarantine executable uploads, limit file size per upload (>1GB), log all file operations with user context, prevent public link sharing

4. **Coaching Page Templates** - Approved app messaging with use case ("Use Slack for work chat—instant messaging channel limits"), disapproved app messaging with alternatives ("Dropbox not approved—use OneDrive for file storage"), remediation steps with screenshots, appeal process

5. **Compliance Reporting** - Monthly SaaS usage inventory, policy violations by user/app/action, coaching interaction metrics (showed, clicked, bypassed), business justification tracking for "caution" apps, trend analysis quarter-over-quarter

## Key Configuration

- **Real-Time Inspection**: Deploy Zscaler CASB inline on ZPA App Connectors; monitor OAuth token issuing and API calls; inspect request/response for sensitive data

- **Tenant Enforcement**: Configure multiple M365 tenants in allow list (Contoso + Partner1 + Partner2); block all other Azure AD logins; implement conditional access for sensitive operations (e-discovery requires MFA)

- **File Operations Granularity**: Separate policies for upload vs. download, large file operations (>100MB flag for review), sharing permissions (public link block, internal share allowed), version history retention

- **Coaching Flow**: Redirect user to educational page with business case, pre-approved alternatives with links, appeal process with manager approval, track coaching effectiveness with click-through rates

- **API Discovery**: Enable CASB API logging to detect shadow API usage (Slack integrations, Zapier, make.com, webhook endpoints); correlate with DLP to detect data exfiltration via APIs

- **Session Hijacking Prevention**: Monitor for unusual OAuth token usage (different IP, device, time of day); revoke suspicious tokens; force re-authentication after policy block

## Gotchas

- Tenant restriction blocks legitimate business use (partner tenants, M&A acquisitions); maintain exception process with manager approval and 90-day review; escalate over-due exceptions

- Coaching pages can be bypassed with VPN or corporate proxy if CASB not positioned inline; verify enforcement point before rollout; implement enforcement on both inline and API CASB

- File upload blocks based on cloud provider create support burden (user doesn't understand why OneDrive upload blocked); include clear alternative workflow with links to IT support

- OAuth token revocation doesn't guarantee session termination; user may have cached access; implement token revalidation at API level; monitor for continued activity after revocation

- SaaS apps frequently change authentication flows; coaching pages and block rules require monthly review and updates; subscribe to app change logs and test new flows quarterly

- Real-time file inspection adds latency (50-500ms per operation); monitor user experience and adjust inspection rules to critical operations only; implement sampling for non-sensitive files

- Bypass attempts via VPN, proxy, or personal devices not controlled by CASB; combine with endpoint detection (EDR) to flag suspicious behavior; implement device compliance checks before access
