---
description: "Cloud Firewall L3/L4 + L7: rule ordering, geo-blocking, IPS profiles, non-standard port handling"
---

# ZIA Cloud Firewall

You are the first line of defense. ZIA Cloud Firewall operates at L3/L4 (IP, port) and L7 (app-layer). Get rule ordering right, and threats die silently. Get it wrong, and legitimate traffic gets blocked.

## When to use

**DO** use ZIA Cloud Firewall when:
- You need to enforce network-level access controls
- You want to block countries, IPs, or high-risk ports
- You're preventing C&C (command-and-control) callbacks
- You need IPS (Intrusion Prevention System) signatures

**DON'T** use when:
- You're just filtering by URL (use URL filtering instead)
- You don't understand rule ordering (it's critical)

## Firewall Rule Order (First Match Wins!)

```
┌─────────────────────────────────────────────────────────────┐
│ Rule Evaluation (CRITICAL: Stop at first match!)            │
└─────────────────────────────────────────────────────────────┘

Priority 1 (Block immediately):
  ✗ Malware/C&C (Zscaler threat intelligence)
  ✗ High-risk countries (Iran, North Korea, Syria)
  ✗ Known APT infrastructure

Priority 2 (Block by policy):
  ✗ P2P/Torrents
  ✗ Non-standard ports (SSH on 22, Telnet on 23)
  ✗ Risky protocols (NTP reflection attacks)

Priority 3 (Allow business critical):
  ✓ Cloud storage (Box, OneDrive, Dropbox)
  ✓ SaaS apps (Salesforce, Slack, Teams)
  ✓ Payment processors

Priority 4 (Default deny):
  ✗ Everything else (implicit deny)

Gotcha: If you place "Allow all" rule at Priority 3,
        everything below it is dead code.
```

## L3/L4 Firewall Rules (IP + Port)

```yaml
---
Rule Name: "Block SSH Brute Force"

Source:
  User/Group: Any
  Location: Any
  Department: Any

Destination:
  IP Address: [Internal servers]
  Port: 22 (SSH)
  Protocol: TCP

Action: Block

IPS Profile: Enabled
  - Detect: SSH brute force attempts (>3 failed logins/min)
  - Alert: Security team
  - Block: Offending IP for 1 hour

Logging: Yes (log all attempts, not just blocks)
```

## L7 Firewall Rules (Application-Layer)

```yaml
---
Rule Name: "Block Unauthorized Salesforce Sync"

Source:
  User/Group: Not in "Sales" group
  Location: Any
  Device Type: Any

Destination:
  Application: Salesforce (Zscaler app ID: 31337)
  Port: Any
  Protocol: HTTPS

Action: Block
Notification: "Salesforce access restricted to sales team. Contact admin."

Logging: Yes
```

## Geo-Blocking (Country-Level)

```
Admin Portal → Cloud Firewall → Geo Enforcement

High-risk countries to block (default):
  ✗ Iran
  ✗ North Korea
  ✗ Syria
  ✗ Cuba
  (varies by industry; follow your export control policy)

Custom geo-blocking:
  ✗ Block outbound to China (if you store trade secrets there)
  ✓ Allow inbound from Canada/UK only (if you're UK-only shop)

Configuration:
  Rule Name: "Block High-Risk Countries"
  Location: Iran, North Korea, Syria, Cuba
  Action: Block
  Notification: "Your location is not supported."
```

## IPS (Intrusion Prevention System) Profiles

```
Admin Portal → Threat Prevention → IPS Profiles

Zscaler default profiles:
  Critical (Recommended):
    ✓ Blocks critical/high-severity exploits
    ✓ Examples: EternalBlue, WannaCry, CVE-2021-34473
    ✗ 0 false positives (Zscaler tunes aggressively)

  Standard:
    ✓ Blocks critical/high/medium threats
    ✗ 0.5% false positive rate
    ~ For most enterprises

  Balanced:
    ✓ Blocks all except low-severity
    ✗ 2% false positive rate
    ~ For risk-averse orgs

Custom profile (advanced):
    ✓ Pick individual signatures
    ✗ Maintenance burden; not recommended

Recommendation:
  Start with "Critical" profile. After 4 weeks, move to "Standard".
```

## Non-Standard Port Handling

| Port | Protocol | Standard Use | Abuse Case | ZIA Action |
|------|----------|--------------|-----------|-----------|
| 22 | SSH | Admin access | Brute force, tunneling | Block (except admin) |
| 23 | Telnet | Legacy access | Clear-text login theft | Block (deprecated) |
| 8080 | HTTP alt | Development | Bypass proxy | Block or caution |
| 443 | HTTPS | Encrypted web | Hide malware in HTTPS | Inspect + IPS |
| 5060 | SIP | VoIP signaling | Phone phishing | Block (use Teams/Zoom) |
| 1433 | SQL Server | Database | SQL injection, data theft | Block outbound |
| 3389 | RDP | Remote desktop | Ransomware lateral movement | Block (use SSO) |

**Policy template:**
```
Rule Name: "Block Non-Standard Ports"

Blocked ports: 22, 23, 8080, 1433, 3389, 5060
Exception: IT admin group can use 22/3389 via VPN only
Action: Block
Logging: Yes (catch lateral movement attempts)
```

## Firewall Rule Configuration Template

```yaml
---
Rule Name: "Allow Box, Block Dropbox"

Order: After malware rules, before default deny

Source:
  Users: All
  Locations: Corporate, Remote
  Device Types: Managed + Unmanaged (ZCC enrolled)

Destination:
  Apps: Box (allow), Dropbox (block)
  Ports: 443
  Protocol: HTTPS

Additional Conditions:
  Time: 8 AM–6 PM (business hours)
  User Groups: NOT finance/legal (they need Dropbox exception)

Action: Allow (Box), Block (Dropbox)
IPS Profile: Standard
SSL Inspection: Enabled
DLP Profile: Enabled
Bandwidth Control: 10 Mbps per app

Logging: Yes
Notification: "Dropbox not allowed. Use Box instead."
```

## Configuration Checklist

```
Before go-live:

[ ] Define rule ordering (malware → geo → business rules → deny)
[ ] List all approved cloud apps + ports
[ ] List all non-standard ports in your environment
[ ] Choose IPS profile (Critical recommended)
[ ] Test geo-blocking on sample traffic (don't block your office!)
[ ] Configure logging (all blocks must be logged)
[ ] Test rule with 10 users before org-wide rollout
[ ] Document exceptions (who can access SSH, Dropbox, etc.)
[ ] Set up alerts for high-risk blocks (3+ failed attempts = escalate)
[ ] Brief help desk: "Block message = check security exceptions"
```

## Gotchas

1. **Rule order chaos:** If you place "Allow all" early, everything else is ignored. Audit your rule order weekly.
2. **Geo-blocking side effects:** If your VPN concentrator is in Canada, blocking Canada = users can't connect. Whitelist your own infrastructure.
3. **IPS profile too aggressive:** Profile set to "Balanced" + heavy DLP = 5% false positive rate. Users get blocked from legitimate Salesforce exports. Start with "Critical".
4. **Silent blocks:** If you don't log L3/L4 blocks, you won't know why users complain. Log everything.
5. **Exception sprawl:** "Just add them to the exception list" without process = 6 months later, half your org has exceptions. Require formal approval.

---

**Pro tip:** Firewall rules are like DNS—wrong ordering breaks everything. Draw your rule order on a whiteboard before you build it. Test with a canary group (10 users) for 1 week before org rollout. You'll find issues before they affect 1,000 people.
