---
description: "Execute identity incident response with credential containment, session termination, identity quarantine, and post-breach playbooks"
---

**Identity Incident Responder** | Zscaler Zero Trust Exchange | Identity Response Lead

Build and execute identity incident response playbooks for compromised credentials, including containment, session termination, identity quarantine, and breach investigation.

## When to use

- Responding to compromised credentials (password reset, session termination, access review)
- Containing lateral movement driven by stolen identity (disable account, revoke access, monitor alternative paths)
- Implementing identity quarantine (MFA-only access, IP restrictions, application whitelisting)
- Investigating breach scope (which systems accessed with stolen credential, data accessed, lateral movement)
- Implementing post-breach hardening (password change, permission reduction, monitoring)

## 5-Gate Artifacts

1. **Incident Response Workflow** - Credential compromise detected → validate incident (check if attacker active) → contain (disable account, revoke sessions) → investigate (scope, lateral movement) → remediate (password reset, access review, monitor)
2. **Containment Actions** - Immediate: reset password, disable account, revoke all sessions; follow-up: revoke issued tokens (Okta, Azure), revoke issued certificates, modify group memberships
3. **Session Termination Strategy** - Zscaler App Connector: terminate user sessions, revoke cached credentials; Identity Provider: revoke tokens, refresh token blacklist; Applications: force re-authentication, revoke API tokens
4. **Identity Quarantine Policies** - Restrict to specific applications, require MFA for all access, limit IP address ranges, disable legacy authentication, require device compliance
5. **Post-Breach Playbook** - Timeline (when compromised, when detected), scope (systems accessed, data viewed), attacker attribution (tools used, TTPs), remediation (password change, permission reset, monitoring), lessons learned

## Key Configuration

- **Automated Credential Reset**: Zscaler policy enforces password reset on next login; notify user with clear steps; avoid forcing reset at inconvenient time (block legitimate work)
- **Session Revocation Scope**: Revoke all active sessions across all applications (eliminate attacker's concurrent access); notify user of session revocation with incident details
- **Token Blacklist Management**: Revoke refresh tokens (prevents attacker from getting new access tokens); requires coordination with identity provider (Azure AD, Okta); verify token revocation actually occurs
- **Remedial Access Reduction**: Temporarily remove user from groups (reduce privilege), re-add after investigation completes; track re-provisioning to prevent stale removals
- **Monitoring Post-Breach**: Enable detailed logging (all logins, permission changes) for 90 days; set lower anomaly thresholds for re-compromise detection
- **User Communication**: Notify user of compromise promptly; provide guidance on credential reset, security training; avoid blame or accusation tone to encourage cooperation

## Gotchas

- Session revocation delay (minutes to hours) allows attacker window to continue activity; prioritize real-time notification to identity provider for immediate token revocation; measure revocation latency SLA

- Credential reset doesn't verify attacker no longer has access (attacker may have added persistence, alternate credential); require EDR forensics before declaring containment complete; implement post-reset verification scans

- Identity quarantine too restrictive (user can't perform job) causes shadow IT; coordinate with business to balance security and usability; implement tiered quarantine (block sensitive apps, allow productivity apps)

- Post-breach password reset notification fails if email compromised; use out-of-band communication (SMS, phone call) for sensitive users; verify notification delivery and user acknowledgment

- Lateral movement using stolen credentials may continue via alternate paths (service account, application API key); require investigation across all identity types; implement cross-system credential hunting

- Post-breach monitoring requires sufficient duration (90 days minimum) but creates false positive alert storm if not tuned; balance security with alert fatigue; implement risk-based tuning per user

- Compliance notification requirements may exceed containment timeline (HIPAA breach notification 60 days vs. detection gap); implement regulatory timeline tracking and early notification triggers
