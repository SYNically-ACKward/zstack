---
description: "Cloud workload egress: ZIA for cloud VMs (AWS/Azure/GCP), lightweight connector, egress policy, SaaS access"
---

# ZT Cloud Egress

**Persona:** Cloud architect configuring egress security for cloud workloads.

## When to use
- Protecting outbound traffic from cloud VMs (AWS EC2, Azure VMs, GCP Compute Engine)
- Applying consistent DLP and threat prevention to cloud workload egress
- SaaS access policies from cloud applications (e.g., cloud app calling external API)
- Lightweight connector deployment in VPC/VNET for egress routing
- Cost optimization (data transfer savings from local egress)

## 5-Gate Artifacts
1. **Cloud Workload Inventory**: VPC/VNET and subnet list, instance types (application server, database, batch job), data sensitivity classification
2. **Lightweight Connector Deployment Plan**: AWS/Azure region, VPC subnet, instance type, network configuration, auto-scaling rules
3. **Egress Policy Matrix**: Workload type → allowed SaaS, external APIs, blocked categories, DLP enforcement level
4. **Network Architecture Diagram**: VPC/VNET, subnets, connector placement, route table config, NAT gateway integration
5. **Monitoring Dashboard**: Cloud egress traffic volume, policy hits, threat detections, connector health

## Key Configuration
- **Lightweight Connector**: Zscaler mini-appliance running in cloud VPC (AWS AMI, Azure Image, GCP Image); routes VM egress through ZIA
- **Connector Sizing**: Small (< 5 Gbps), Medium (5-20 Gbps), Large (20+ Gbps) based on expected VM outbound throughput
- **VPC Routing**: Configure route table to send 0.0.0.0/0 (or specific subnets) to connector; connector routes to Zscaler cloud via IPSEC tunnel
- **Connector HA**: Deploy 2+ connectors across availability zones; auto-fail over if connector unhealthy
- **Security Groups**: Connector requires inbound SSH (for management), outbound to Zscaler cloud (HTTPS 443), inbound from VM subnet (all ports)
- **NAT Behavior**: Connector performs SNAT (source NAT) to its IP; Zscaler cloud sees connector IP as source, not individual VM IPs
- **User-to-App Context**: If workload needs user context for policy (e.g., sales team egress vs eng egress), use source IP ranges or tags as proxy
- **SaaS Direct Routes**: For high-bandwidth SaaS (Office 365, Salesforce APIs), consider direct egress vs connector route based on cost/latency tradeoff
- **DLP Enforcement**: Connector enables full DLP (scan all outbound); lightweight implementation; may require memory/CPU tuning
- **Connector Auto-Update**: Zscaler pushes updates; can be scheduled during maintenance window or rolled automatically with minimal impact

## Gotchas
- **NAT Overload**: If many VMs route through single connector, source port exhaustion may cause connection refusal; load-balance or scale connector
- **Data Transfer Cost**: Egress through connector (vs direct NAT) counts as data transfer; AWS charges per GB out; compare cost vs direct route
- **Latency Addition**: Connector adds 2-5 ms latency to egress paths; for latency-sensitive workloads, measure impact
- **Connector Failure Cascade**: If connector unhealthy and route table still points to it, all egress drops; ensure graceful fallback (secondary connector or direct route)
- **API Gateway Conflict**: If workload uses VPC endpoint for AWS service (S3, DynamoDB), connector may intercept and block; exclude service endpoints from routing
- **Container Egress**: If VMs run containers, routing happens at VM kernel level; all containers inherit egress policy; can't segment per-container
- **Connector Migration**: Updating connector image causes brief service interruption; coordinate with workload teams for off-hours maintenance
- **Billing Blind Spot**: Egress traffic volume not visible in VM monitoring; set up connector metrics dashboard to track egress separately
- **Rule Complexity**: Per-workload rules multiply quickly (dev vs prod, internal API vs external); use naming convention and centralized policy management
- **Failover Testing**: Connector failure during production may cause workload outage; test failover in non-prod environment first

## Configuration Checklist
- [ ] Cloud workload egress requirements (bandwidth, SaaS list, DLP sensitivity) documented
- [ ] Connector instance type and region selected; capacity plan reviewed
- [ ] VPC/VNET subnet for connector deployment identified and network pre-checked
- [ ] Connector HA strategy defined (2-3 connectors, availability zones, auto-scaling)
- [ ] Route table changes planned and tested in non-prod environment
- [ ] Security group rules reviewed by cloud security team
- [ ] Egress policy drafted with business owner approval
- [ ] SaaS and API endpoint access list validated with application teams
- [ ] DLP policies (if enabled) tested on sample egress data
- [ ] Connector monitoring dashboard created (health, throughput, errors)
- [ ] Failover procedure tested and documented
