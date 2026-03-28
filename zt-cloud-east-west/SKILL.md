---
description: "East-west traffic inspection: inter-VPC/VNET inspection, workload-to-workload policies, cloud native integration"
---

# ZT Cloud East-West

**Persona:** Cloud security architect designing workload-to-workload microsegmentation.

## When to use
- Inspecting traffic between cloud workloads (VM-to-VM, container-to-container)
- Inter-VPC/VNET communication with centralized policy enforcement
- Preventing lateral movement and enforcing zero-trust between application tiers
- Cloud-native integration with AWS Security Groups, Azure NSGs, Kubernetes network policies
- Multi-cloud workload segmentation (AWS + Azure hybrid environment)

## 5-Gate Artifacts
1. **Workload Dependency Map**: Application tier breakdown (web, API, database), inter-tier communication ports, data flow diagram
2. **East-West Policy Design**: Allowed micro-segments (web↔API, API↔DB), denied paths, exception handling, user context integration
3. **Cloud Native Integration Plan**: AWS Security Groups rules aligned with ZPA policies, Azure NSGs mirrored, Kubernetes network policies applied
4. **Connector Deployment Architecture**: Central transit VPC/VNET with east-west connectors, routing configuration, HA setup
5. **Monitoring & Audit Dashboard**: Allowed vs blocked flows, policy enforcement verification, anomaly detection, audit log retention

## Key Configuration
- **East-West Connector**: Zscaler connector in central transit VPC/VNET; routes inter-VPC traffic through ZPA for policy inspection
- **Transit Routing**: VPC1 and VPC2 route internal traffic through transit VPC; VPC peering or transit gateway enables central inspection
- **Workload Identity**: Each workload tagged with identity (application, tier, environment); policies reference tags, not IP addresses
- **Zero-Trust Access**: Default deny; only explicitly allowed flows permitted; even internal subnets subject to policy
- **Application Dependency Discovery**: Automated dependency mapping or manual documentation of tier-to-tier communication requirements
- **Policy Rule Structure**: Source (workload identity), destination (workload identity), port/protocol, encryption required (yes/no)
- **Lateral Movement Prevention**: Database tier rejects connections from non-API tier; prevents direct database access if API compromised
- **User Context**: If applicable (e.g., admin VMs), integrate with Okta/Azure AD for user-aware policies
- **Encryption In Transit**: Policies can enforce TLS encryption between workloads; useful for PII-handling workloads
- **Policy as Code**: Store policies in Git (Terraform, CloudFormation); version control and code review for changes
- **Connector Scaling**: If many workloads, multiple connectors may be needed; load-balance traffic or geo-distribute

## Gotchas
- **Asymmetric Routing**: If return traffic doesn't traverse connector, policy enforcement one-directional; test bidirectional flows
- **Connector Bottleneck**: All inter-VPC traffic flows through connector; undersizing causes latency and throughput degradation
- **Legacy App Incompatibility**: Old apps may not work with TLS encryption requirement; carve out exemptions or update apps
- **Database Replication**: Master-slave database replication may fail if policy blocks replication port; explicitly allow or use same security group
- **Auto-Scaling Churn**: New instances on auto-scale may not match workload identity tagging; use launch templates and auto-tagging
- **Kubernetes Overlay Conflict**: If Kubernetes cluster runs overlay network (Calico, Flannel), ZPA policies may conflict; validate with Kubernetes team
- **Container Registry Access**: Container images pulled from external registry; policy must allow port 443 to registry or image pull fails
- **Stateful Inspection**: Some applications use dynamic port ranges; static port policies may miss traffic; test with application owner
- **Cross-Cloud Routes**: If hybrid (AWS + Azure), inter-cloud east-west requires VPN or express route; connector placement strategy must account
- **Debugging Complexity**: If traffic is blocked, traffic logs show policy hit but may not indicate root cause (missing tag, wrong port); deep investigation needed

## Configuration Checklist
- [ ] Workload dependency map created and validated with application teams
- [ ] East-west policy drafted with detailed allow/deny rules
- [ ] Workload tagging strategy defined and implementation automated (CloudFormation, Terraform, Azure Policy)
- [ ] Transit VPC/VNET created with redundancy and scaling considered
- [ ] Central east-west connector deployed and tested
- [ ] VPC/VNET peering or transit gateway configured for inter-region traffic
- [ ] Security Groups and NSGs reviewed to identify redundant rules (ZPA policies replace some rules)
- [ ] Kubernetes network policies aligned with ZPA policies (if containerized workloads)
- [ ] Encryption requirement (TLS) for each policy rule decided and enforced
- [ ] Monitoring dashboard with allowed/blocked flow counts created
- [ ] Audit log retention (90+ days) configured for compliance
- [ ] Failover procedure for connector outage tested
- [ ] Auto-scaling behavior validated to ensure new workloads tagged correctly
