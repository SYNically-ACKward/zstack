---
description: "Design Business Continuity: customer-hosted PCC vs Zscaler-managed BC Cloud, RPO/RTO targets"
---

# BC Design

**Persona:** IT continuity manager designing disaster recovery for Zscaler deployment.

## When to use
- Defining RPO (Recovery Point Objective) and RTO (Recovery Time Objective) requirements
- Choosing between customer-hosted PCC and Zscaler-managed BC Cloud
- Planning regional cloud redundancy (multi-region deployment)
- Backup and restore strategy for configurations
- Failover automation and runbook development

## 5-Gate Artifacts
1. **RPO/RTO Matrix**: Service criticality → target RPO (hours), RTO (minutes), recovery method
2. **PCC Deployment Architecture**: Customer-hosted on AWS AMI, Azure VM, or VMware OVA; network, licensing, capacity planning
3. **BC Cloud Specification**: Zscaler-managed deployment; region selection, throughput tier, SLA
4. **Config Backup Strategy**: API export frequency, version control system integration, restore testing schedule
5. **Failover Runbook**: Automated vs manual steps, decision tree, communication plan, post-recovery validation

## Key Configuration
- **Customer-Hosted PCC**: Install on AWS AMI, Azure VM, or VMware; customer manages infrastructure, HA, scaling
- **PCC Licensing**: Requires separate PCC license tier (distinct from primary ZIA/ZPA licenses); can be time-limited or perpetual
- **PCC Network**: Dedicated VPC/subnet, private IP connectivity to ZIA/ZPA, separate egress path or shared
- **Zscaler-Managed BC Cloud**: Zscaler operates PCC in dedicated regional cloud; customer provides policy config, Zscaler handles uptime
- **RPO Definitions**: Gold (< 1 hour), Silver (< 4 hours), Bronze (< 24 hours); determines config sync frequency and backup retention
- **RTO Definitions**: Critical (< 15 min), High (< 1 hour), Medium (< 4 hours), Low (< 24 hours)
- **Config Sync Frequency**: Hourly for Gold, 6-hourly for Silver, daily for Bronze; real-time streaming available at premium SLA
- **Cross-Region Redundancy**: Primary cloud in region A, standby in region B; data replicated every sync interval
- **Failover Trigger**: Manual approval required (ZCC admin action) or automated on primary cloud outage detection (SLA tier dependent)
- **Licensing Continuity**: BC Cloud must license traffic during failover; verify subscription includes failover capacity

## Gotchas
- **PCC Capacity Underestimate**: Customer-hosted PCC must support 100% of peak traffic during disaster; sizing wrong causes failover to bottleneck
- **Network Latency**: If PCC in geographically distant region, latency to users increases; plan user experience degradation
- **Config Drift**: BC cloud config may drift from primary if manual changes made in primary; automation strongly recommended
- **Failover Gap**: Even with hourly config sync, up to 1 hour of policy changes lost on failover; document acceptable loss window
- **License Consumption**: Failover at PCC consumes separate license tier; if not purchased, failover fails silently
- **Encryption Key Rotation**: If keys rotated on primary, PCC doesn't auto-sync; manual key injection required or failover fails
- **Dual Management Burden**: If customer-hosted PCC, customer responsible for patches, updates, monitoring; risk if internal team lacks AWS/Azure expertise
- **Failback Complexity**: Switching back to primary after recovery requires config re-sync and potential policy conflicts if drift occurred

## Configuration Checklist
- [ ] RPO/RTO requirements documented and signed off by business stakeholders
- [ ] BC deployment model selected (customer-hosted vs Zscaler-managed)
- [ ] If customer-hosted: cloud account, network, compute resources pre-staged
- [ ] If Zscaler-managed: region selection completed and latency validated from key user locations
- [ ] Config backup frequency set and API credentials stored securely
- [ ] Failover procedure documented with step-by-step runbook
- [ ] DR drill schedule established (quarterly minimum)
- [ ] Licenses for BC tier verified and terms understood
- [ ] Notification and escalation procedure defined (who gets paged, when, what to do)
- [ ] Post-recovery validation checklist created (health checks, policy verification, performance baseline)
