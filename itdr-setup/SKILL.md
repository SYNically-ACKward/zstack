---
description: "Deploy identity threat detection and response with AD monitoring, risk scoring, and lateral movement detection"
---

**Identity Security Engineer** | Zscaler Zero Trust Exchange | Identity Threat Lead

Implement Identity Threat Detection and Response (ITDR) to monitor Active Directory, detect anomalous identity usage, score identity risk, and respond to compromised credentials.

## When to use

- Detecting credential compromise through unusual login patterns (impossible travel, failed login spike)
- Identifying lateral movement driven by identity attacks (Kerberoasting, credential stuffing)
- Monitoring for privilege escalation (user adds self to admin groups, enables privileged access)
- Detecting MFA bypass attempts and anomalous authentication methods
- Responding to compromised service accounts used in attacks

## 5-Gate Artifacts

1. **AD Monitoring Architecture** - Log collection from Domain Controllers (Security Event ID 4624, 4625, 4739, 4756, 4728), identity enrichment (user attributes, group membership, sensitivity), real-time alerting
2. **Identity Risk Scoring Model** - Base factors (failed login attempts, impossible travel, privileged account activity), detection factors (Kerberoasting, pass-the-hash, abnormal permissions), risk tiers (high risk user = isolation policy)
3. **Anomaly Detection Rules** - Impossible travel (login from distant location within X minutes), brute force (X failed logins in Y time), privilege escalation (user permission change), service account misuse (unusual time/location)
4. **Lateral Movement Detection** - Monitor for SMB lateral movement, Kerberoasting (unusual TGS requests), credential delegation (CredSSP events), remote service creation
5. **Response Playbook** - Detect compromised credential → reset password, disable account, revoke active sessions, review access, quarantine devices with suspicious activity

## Key Configuration

- **AD Event Collection**: Enable comprehensive logging (Success + Failure events); stream to SIEM via syslog/WinRM; ensure low latency (<5 second delivery)
- **User Baseline Profiling**: Collect 30 days of authentication events per user; establish normal login times, locations, devices, applications; use for anomaly alerting
- **Risk Threshold Calibration**: Tune impossible travel distance (e.g., cannot go from NYC to LA in <4 hours) and time window based on organization size
- **Privileged Account Monitoring**: Flag activity on sensitive accounts (admin, service accounts); require MFA; log all privilege changes (add to admin group, policy modification)
- **Automated Response Scope**: Define which identities can be automatically disabled (service accounts with low risk) vs. human review (executives, compliance officers)

## Gotchas

- AD event volume large (1M+ events/day in large tenant); filtering for relevant events critical; initial noise from legitimate admin activity, scheduled tasks, batch operations; implement sampling and off-peak processing

- Impossible travel calibration too sensitive (alerts on VPN logout/login) creates false positives; use geolocation services and verify location precision; whitelist known VPN concentrators and offices

- Service account baseline noisy (3am batch job vs. midnight scheduled backup); create service account profiles separate from user baselines; document expected activity patterns per service account

- Password resets don't immediately update all systems (cached authentication, token expiry); new compromised session may continue until token expires (4-8 hours); implement aggressive token revocation on password change

- Lateral movement detection requires detailed network logging (Sysmon, Windows Event forwarding); EDR required for visibility, not just AD logging; validate network logging coverage before alerting

- Privilege escalation false positives (legitimate admin adding users to groups, service account permission changes) require approval workflow; escalate to admin before response action; maintain admin activity whitelist

- Hybrid identity environments (AD + Azure AD) create synchronization gaps; implement monitoring for both systems and reconcile identity states; test failover scenarios
