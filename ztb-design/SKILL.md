---
description: "Design ZTB appliance architecture with sizing, topology, HA, VLAN strategy, and DIA breakout"
---

# ZTB Design

**Persona:** Network architect designing branch infrastructure for Zscaler deployment.

## When to use
- Initial ZTB greenfield design before procurement
- Appliance sizing decisions (ZT-200/400/600)
- HA topology selection and planning
- VLAN segmentation strategy for branch
- DIA vs backhaul routing rules

## 5-Gate Artifacts
1. **Appliance Sizing Matrix**: Document user count, throughput, concurrent sessions → ZT model recommendation
2. **HA Topology Diagram**: Active/passive failover layout, interconnect speed, state sync bandwidth
3. **VLAN Design**: Access, DMZ, IoT, guest VLANs with ZTB interface mapping
4. **BGP/Static Route Plan**: DIA breakout subnets, backhaul routes, failover priorities
5. **Interface Allocation Sheet**: WAN uplink, DIA exit, MPLS, LAN switch connection speeds

## Key Configuration
- **ZT-200**: up to 300 Mbps, ~500 users, 1,000 concurrent sessions
- **ZT-400**: up to 1 Gbps, ~1,500 users, 5,000 concurrent sessions
- **ZT-600**: up to 2+ Gbps, ~3,000+ users, 10,000+ concurrent sessions
- **HA State Sync**: dedicated 1Gbps link between appliances, separate from data path
- **VLAN Trunk**: primary branch LAN switch uplink carries all transit VLANs
- **DIA Breakout Subnets**: Define /24s for SaaS categories (Office 365, Salesforce, Slack) for direct egress
- **Backhaul Routes**: Legacy DC apps, internal resources default to ZTB tunnels
- **BGP Graceful Restart**: Enable if using dynamic routing for failover convergence
- **Active/Passive HA**: Primary ZT handles traffic; secondary takes over on heartbeat loss (configurable threshold 10-30 sec)

## Gotchas
- **HA Interconnect**: Undersizing state-sync link causes session loss; recommend same speed as primary WAN
- **DIA Subnet Overlap**: If DIA subnets overlap with backhaul targets, DIA takes precedence—carefully document scope
- **VLAN Trunking**: Missing native VLAN can drop untagged frames; verify switch config matches ZTB SVI setup
- **Failover Timing**: Active/passive not instantaneous; workloads see 30-60 sec disruption; test RTO requirements
- **BGP Metric Tuning**: Asymmetric route metrics cause packet loss in reverse direction; keep IGP metrics symmetric
- **Power/Cooling**: ZT-600 runs hot; plan rack space with >2" clearance and ensure PDU capacity

## Configuration Checklist
- [ ] Throughput profile selected, margin verified (20% headroom minimum)
- [ ] HA redundancy type confirmed (active/passive vs eventual active/active)
- [ ] All VLANs mapped to ZTB SVI interfaces
- [ ] DIA breakout subnets locked down with security stakeholders
- [ ] BGP/static routes documented with failover sequence
- [ ] Interface speeds match switch port speeds (no speed mismatches)
- [ ] Power and thermal capacity confirmed with data center team
- [ ] HA state-sync link is isolated from management and data traffic
