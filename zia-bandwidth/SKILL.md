---
description: "Bandwidth control: QoS policies, throttling by app/category, SaaS prioritization, conference call protection"
---

# ZIA Bandwidth Control (QoS)

You are the traffic cop. Bandwidth control ensures Zoom calls don't stutter while someone downloads torrents, and Salesforce data sync doesn't starve. Get it right, and users don't know you're shaping traffic. Get it wrong, and everyone complains.

## When to use

**DO** use ZIA Bandwidth Control when:
- You want to prioritize critical apps (Zoom, Teams, VoIP)
- You need to throttle bandwidth hogs (YouTube, Netflix, gaming)
- You want to ensure WAN link utilization stays <80%
- You're implementing SaaS-first access model

**DON'T** use when:
- You're not measuring baseline bandwidth (you don't know what normal looks like)
- You don't have SLA targets (e.g., "Zoom must get 4 Mbps")

## QoS Priority Tiers (RFC 2474)

```
RFC 2474 DSCP (Differentiated Services Code Point):
  EF (Expedited Forwarding):  Class 5 – Real-time (Zoom, Teams, VoIP)
  AF4x (Assured Forward):      Class 4 – Critical business (Salesforce, banking)
  AF3x (Assured Forward):      Class 3 – Standard (email, web, file sync)
  AF2x (Assured Forward):      Class 2 – Best-effort (downloads, streaming)
  CS0 (Default):              Class 0 – Low priority (p2p, torrents, gaming)

Zscaler maps these to 5 bands:
  Priority 1 (EF):      VoIP, Zoom, Teams, WebEx
  Priority 2 (AF4):     Salesforce, banking, critical SaaS
  Priority 3 (AF3):     Email, web, file upload
  Priority 4 (AF2):     YouTube, Netflix, streaming (throttled)
  Priority 5 (CS0):     P2P, torrents, gaming (starved)
```

## Bandwidth Allocation Strategy

```
┌──────────────────────────────────────────────────────────┐
│ WAN Link Capacity: 100 Mbps (typical enterprise site)    │
└──────────────────────────────────────────────────────────┘

Allocation:
  Priority 1 (VoIP/Zoom):       20% = 20 Mbps (reserved)
  Priority 2 (Critical SaaS):   50% = 50 Mbps (reserved)
  Priority 3 (Email/Web):       20% = 20 Mbps (shared)
  Priority 4 (Streaming):       10% = 10 Mbps (throttled)
  Priority 5 (P2P/Gaming):      0%  = Starved (if others need it)

Usage pattern:
  8 AM: Zoom call (20 Mbps) + Salesforce export (30 Mbps) = OK
        Remaining: 50 Mbps for email, web browsing

  12 PM: Someone tries Netflix + Zoom call
         Zoom reserved 20 Mbps (guaranteed)
         Netflix throttled to remaining capacity (max 10 Mbps)
         User sees slow Netflix = by design
```

## Bandwidth Control Rules (By App)

```yaml
---
Rule Name: "Protect VoIP/Zoom During Business Hours"

Conditions:
  Applications: Zoom, Teams, WebEx, Skype
  Time: 8 AM–6 PM weekdays
  Protocol: UDP (voice/video)

Bandwidth Limit:
  Guaranteed: 4 Mbps per concurrent call
  Maximum: 8 Mbps per concurrent call
  Priority: EF (Expedited Forwarding)

Enforcement:
  If Zoom + Teams call simultaneous:
    Zoom gets 4 Mbps first (priority 1)
    Teams gets next 4 Mbps
    Rest of link available for other traffic

Action: Prioritize (rate-limit others if needed)

---
Rule Name: "Throttle Video Streaming (Off-Hours)"

Conditions:
  Applications: YouTube, Netflix, Hulu, Disney+
  Time: 8 AM–6 PM weekdays (or always, depends on policy)
  Protocol: TCP/UDP

Bandwidth Limit:
  Max per user: 2 Mbps (720p max)
  Priority: AF2 (Best-effort)

Enforcement:
  User tries to stream 4K Netflix:
    System caps at 2 Mbps (720p quality)
    User sees "buffering" unless bandwidth available

Action: Throttle

---
Rule Name: "Block Gaming (During Business Hours)"

Conditions:
  Applications: League of Legends, Fortnite, Valorant, Apex
  Time: 8 AM–6 PM weekdays
  Protocol: UDP

Bandwidth Limit: 0 Mbps
Priority: CS0 (Starved)

Enforcement: Complete starvation if other traffic competes

Action: Block OR Throttle to 512 Kbps (playable but annoying)
```

## Guaranteed vs. Maximum Bandwidth

```
Rule: "Prioritize Salesforce Uploads"

Guaranteed Bandwidth: 10 Mbps
  = "Salesforce always gets at least 10 Mbps"
  = Even if network is congested, Salesforce connection reserved

Maximum Bandwidth: 20 Mbps
  = "Salesforce can burst to 20 Mbps if available"
  = If 40 Mbps free, Salesforce can use it

Typical allocation:
  Total WAN: 100 Mbps
  Salesforce guaranteed: 10 Mbps (never less)
  Salesforce maximum: 20 Mbps (during off-peak)
  Remaining 80 Mbps: Shared by all other apps
```

## SaaS-First Prioritization

**Rank your critical apps:**

| Tier | App | Guarantee | Max | Reason |
|------|-----|-----------|-----|--------|
| 1 | Zoom/Teams | 4 Mbps/call | 8 Mbps | Revenue-critical |
| 2 | Salesforce | 10 Mbps | 20 Mbps | Business process |
| 2 | Box/OneDrive | 5 Mbps | 15 Mbps | Data sync |
| 3 | Email/Exchange | 3 Mbps | 10 Mbps | Communication |
| 4 | YouTube/Netflix | 0 Mbps | 2 Mbps | Throttled |
| 5 | P2P/Gaming | 0 Mbps | 0 Mbps | Blocked |

## Conference Call Protection (Critical Recipe)

```
Objective: Ensure Zoom/Teams calls never stutter

Rule Set:

1. Reserve minimum bandwidth:
   Zoom/Teams: 4 Mbps guaranteed per concurrent call
   (If org has max 20 concurrent calls: 80 Mbps reserved)

2. Detect when call starts:
   Monitor: UDP:5004-5005 (RTP ports)
   Action: Automatically bump to priority EF

3. Block known bandwidth hogs during calls:
   Rule: "If Zoom call active → Block Netflix"
   Alternative: "If Zoom call active → Throttle Netflix to 512 Kbps"

4. Alert if Zoom quality degrades:
   Monitor: Packet loss >2%, jitter >50ms
   Alert: Security team (may indicate DDoS or WAN saturation)

5. Test procedure:
   Start Zoom call + start large file download
   Verify: Zoom stays smooth (measure MOS score ≥4.0)
```

## Configuration Checklist

```
Before go-live:

[ ] Measure current bandwidth usage (baseline for 1 week)
[ ] Identify critical applications (must never starve)
[ ] Identify bandwidth hogs (throttle these)
[ ] Calculate WAN capacity + 30% buffer
[ ] Allocate guaranteed bandwidth per tier
[ ] Create rules for top 10 apps (80/20 rule)
[ ] Set Zoom/Teams guarantee = 4 Mbps per call
[ ] Test with actual Zoom calls during peak usage
[ ] Measure call quality (MOS score, jitter, packet loss)
[ ] If call quality <4.0, increase guarantee
[ ] Document exceptions (who gets high guarantee)
[ ] Set up dashboard alerts (WAN >80% utilization)
[ ] Train help desk: "Call quality issue? Check bandwidth rule"
```

## Gotchas

1. **Guaranteed bandwidth = WAN overbooking:** If you guarantee 20 Mbps to 10 apps, you need 200 Mbps WAN. Guarantee less than available capacity.
2. **No baseline measurement:** You don't know what "normal" is. Measure for 2 weeks before tuning QoS.
3. **Throttling too aggressive:** If you throttle Netflix to 512 Kbps, users will VPN around you. Set reasonable limits (2–5 Mbps for streaming).
4. **Conference call surprise:** You prioritize Zoom but forgot Teams. Day 1 go-live, Teams calls sound robotic. Test with both.
5. **No monitoring dashboard:** You can't see if your QoS policy is working. Create a dashboard: "Active calls" + "WAN utilization" + "Policy effectiveness".

---

**Pro tip:** The best QoS is invisible. Users don't know you're prioritizing Zoom—they just know calls don't stutter. Start conservative (high guarantees, low throttles), then tighten over 4 weeks as you build confidence.
