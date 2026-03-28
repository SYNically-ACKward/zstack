---
description: "URL filtering, cloud firewall, app control, bandwidth control policy design. Include a policy matrix template."
---

# ZIA Policy Design

You are the architect of trust and control. ZIA policies enforce your zero-trust model. Get them right, and users don't notice. Get them wrong, and you're debugging user complaints for months.

## When to use

**DO** use ZIA Policy Design when:
- You're building the security posture for a new customer
- You need to balance control with usability
- You're documenting policy decisions for audit

**DON'T** use when:
- You're just patching a single rule (that's operational)
- Policies are already live and stable

## The Policy Layers (OSI Model)

```
Layer 7 (App):      App control (Slack, Teams, Salesforce, etc.)
Layer 7 (Content):  URL filtering (news, gambling, p2p, etc.)
Layer 4 (DLP):      Data loss prevention (sensitive data exfiltration)
Layer 3–4 (FW):     Cloud firewall (geo-blocking, IP reputation)
Layer 2 (QoS):      Bandwidth control (prioritization, throttling)
```

**Rule order:** Cloud Firewall → URL Filtering → DLP → App Control → Bandwidth Control

## Policy Matrix Template

Create this matrix for every customer. It's your north star:

```
┌────────────────────┬──────────────┬──────────┬──────────────┐
│ Category           │ Rule Type    │ Action   │ Exception(s) │
├────────────────────┼──────────────┼──────────┼──────────────┤
│ Business Critical  │ URL allow    │ Allow    │ None         │
│ (Box, Salesforce)  │ App control  │ Allow    │ None         │
├────────────────────┼──────────────┼──────────┼──────────────┤
│ Productivity       │ URL allow    │ Allow    │ None         │
│ (YouTube, Slack)   │ App control  │ Allow    │ None         │
├────────────────────┼──────────────┼──────────┼──────────────┤
│ Social Media       │ URL category │ Caution  │ HR/Marketing │
│                    │ App control  │ Block    │ None         │
├────────────────────┼──────────────┼──────────┼──────────────┤
│ Malware/Phishing   │ URL category │ Block    │ None         │
│ High-risk          │ DNS Category │ Block    │ None         │
├────────────────────┼──────────────┼──────────┼──────────────┤
│ News               │ URL category │ Block    │ Legal, C-suite│
├────────────────────┼──────────────┼──────────┼──────────────┤
│ P2P/Torrents       │ URL category │ Block    │ None         │
│                    │ App control  │ Block    │ None         │
└────────────────────┴──────────────┴──────────┴──────────────┘
```

## Configuration Knobs in Zscaler Console

### URL Filtering

```
Admin → Content Library → URL Categories

Settings:
  ✓ Enable Dynamic Categorization (use Zscaler's ML)
  ✓ Lookup timeout: 3s (balance speed vs. accuracy)
  ✓ Custom URL categories: Create 5–10 for business-specific domains

Example custom category:
  Name: "Approved SaaS"
  URLs: salesforce.com, box.com, slack.com, notion.com
  Action: Allow (no inspection)

Example rule:
  Rule Name: "Block Entertainment"
  URL Categories: Music, Streaming Media, Sports
  Action: Block
  Auth Requirement: None
```

### App Control

```
Admin → Policy → Rule → Firewall → App Control

Settings:
  ✓ Enable application/category-based policies
  ✓ Use confidence levels (e.g., 100% confidence = high certainty)

Example rule:
  Rule Name: "Block Unauthorized P2P"
  Application: BitTorrent, uTorrent, Transmission
  Confidence: ≥100
  Action: Block
  Log: Yes
```

### Cloud Firewall (Geo-Blocking + Reputation)

```
Admin → Policy → Rule → Firewall → Network Services

Geo-Blocking:
  ✓ Block traffic from high-risk countries (e.g., Iran, North Korea)
  ✓ Whitelist: [your office countries]

Reputation:
  ✓ Block IPs with Zscaler Threat Intelligence reputation score <-50
  ✓ Custom IP allowlist: [partner IPs, CDNs]

Example rule:
  Rule Name: "Block High-Risk Countries"
  Location: Iran, North Korea, Syria
  Action: Block
  Log: Yes
```

### Bandwidth Control (QoS)

```
Admin → Policy → Rule → Bandwidth Control

Example rule:
  Rule Name: "Throttle Video Streaming During Business Hours"
  Applications: Netflix, YouTube (non-workday exceptions)
  Time: 8 AM–6 PM weekdays
  Bandwidth Limit: 2 Mbps per user
  Priority: Low

Example rule:
  Rule Name: "Prioritize VoIP"
  Applications: Zoom, Teams, Webex
  Bandwidth Priority: High
  QoS: EF (Expedited Forwarding)
```

## Decision Matrix: Allow vs. Block vs. Caution

| Traffic Type | Action | Reasoning |
|--------------|--------|-----------|
| Salesforce, Box, Slack | Allow | Business critical |
| Zoom, Teams, WebEx | Allow | Revenue-dependent |
| Gmail, Outlook | Allow | Communication |
| News, Social (generic) | Caution | Business use OK, monitor abuse |
| Gambling, Adult content | Block | Non-work; liability risk |
| P2P, torrents | Block | Copyright, malware vector |
| Malware/C&C | Block | Zero exceptions |
| Unknown (0 reputation) | Caution | Let ML learn; escalate to DLP if sensitive data |

## Policy Rule Order (Critical!)

```
# Rule evaluation order (first match wins):

1. [HIGHEST] Block Malware/C&C (non-negotiable)
2. Block High-Risk Countries (geo-blocking)
3. Block P2P/Torrents (bandwidth protection)
4. Allow Business Critical (Salesforce, Box, etc.)
5. Caution Social Media (HR exception, monitor)
6. Block News/Entertainment (liability)
7. [LOWEST] Default action (usually Block)

Mistake: Placing "Allow Everything" above specific rules = policies ignored!
```

## Gotchas

1. **Overly broad allow rules:** "Allow all traffic from marketing department" kills your entire policy. Be specific (by app, by category).
2. **No exceptions process:** Customer asks: "Can I allow YouTube for my team?" Without a process, you either say yes forever or explain why every time. Create a formal exception request workflow.
3. **Not logging:** If you don't log policy blocks, you can't prove compliance or troubleshoot user issues. Log everything.
4. **Dynamic categorization off:** Zscaler's ML updates categories in real-time. Turning it off = stale definitions. Keep it on.
5. **Bandwidth throttling too aggressive:** If you throttle Netflix to 1 Mbps, users will bypass with a VPN. Set reasonable limits (2–5 Mbps) to reduce circumvention.

---

**Pro tip:** Write a policy matrix on Day 1 and share it with the customer's steering committee. It forces alignment before you build anything. "Is YouTube blocked?" answered upfront = no rework in Week 4.
