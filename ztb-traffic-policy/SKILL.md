---
description: "Configure branch traffic routing: DIA for SaaS, backhaul for DC apps, app-based routing, bandwidth reservation"
---

# ZTB Traffic Policy

**Persona:** Network engineer configuring traffic policies for branch optimized routing.

## When to use
- Defining which traffic exits direct to internet (DIA) vs backhauls through ZTB tunnels
- SaaS optimization (Office 365, Salesforce, Slack direct egress)
- Data center application steering through ZPA tunnels
- QoS and bandwidth reservation per application or user group
- Traffic steering exceptions and per-department rules

## 5-Gate Artifacts
1. **DIA vs Backhaul Decision Matrix**: App category → egress path (Office 365→DIA, internal DB→backhaul)
2. **QoS Policy Map**: Applications → bandwidth tiers (critical, high, normal, low), shaping rates
3. **Exception Rules Document**: Site-specific overrides, per-user or department steering, time-of-day rules
4. **Bandwidth Capacity Plan**: Uplink speed → DIA and backhaul reservation percentages
5. **Traffic Validation Report**: Before/after flow captures showing correct path selection

## Key Configuration
- **DIA Routing**: IP-based (VLAN subnet), app-based, or DNS-based steering of SaaS to direct internet path
- **SaaS Categories**: Office 365 (Microsoft IPs), Salesforce (CRM), Slack, ServiceNow, AWS/Azure APIs
- **Backhaul Steering**: Internal DC subnets, legacy apps, ERP systems routed through ZPA tunnels
- **App-Based Routing**: Zscaler app database identifies SaaS app regardless of IP/DNS; overrides IP-based rules
- **Bandwidth Reservation**: QoS policies per VLAN, user group, or application; common ratios: 40% DIA, 40% backhaul, 20% shared
- **Traffic Shaping**: Token bucket algorithm; peak rate, average rate, burst size tuning per app priority
- **Failover Behavior**: If backhaul tunnel down, traffic doesn't automatically reroute to DIA unless explicit fallback rule
- **SSO App Identification**: Requires ZPA user context; steers authenticated traffic based on user group rules

## Gotchas
- **DIA Subnet Overlap**: If DIA subnets overlap internal subnets, routing becomes ambiguous; keep DIA ranges non-overlapping
- **App-Based vs IP-Based Precedence**: IP rules may block app-based routing; verify rule order and test with packet captures
- **Bandwidth Over-subscription**: If total reservations > uplink capacity, congestion causes poor QoS; validate headroom
- **Failover Surprises**: Backhaul tunnel flap doesn't smoothly migrate traffic; workloads see dropped packets for 10-30 sec
- **DNS Gaming**: If user configures private DNS, app-based routing can't identify SaaS; requires client-side DNS policy
- **Asymmetric QoS**: Egress shaped at 1 Mbps but ingress unshape causes buffer bloat; apply shaping bidirectionally
- **Time-of-Day Rules**: Scheduling mistakes cause traffic steering to apply at wrong times; log rule evaluations
- **Per-User Steering**: If using device groups or location-based rules, verify ZCC/ZPA user auth is working correctly

## Configuration Checklist
- [ ] SaaS application list reviewed and categorized (DIA vs backhaul)
- [ ] DIA subnet ranges locked down with security review
- [ ] Bandwidth percentages calculated with 20% safety margin
- [ ] QoS policy priorities assigned (critical/high/normal/low)
- [ ] Failover fallback rules documented (e.g., backhaul down → DIA or drop?)
- [ ] App-based routing tested with packet capture validation
- [ ] Traffic engineering tested under load (synthetic traffic generation)
- [ ] Monitoring dashboard alerts configured for policy violations
- [ ] Per-site exceptions approved by business owners
- [ ] Rollback plan documented if policy causes production issue
