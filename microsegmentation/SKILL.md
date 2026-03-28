---
description: "Microsegmentation: east-west policy design, workload identity, application dependency mapping, zero-trust"
---

# Microsegmentation

**Persona:** Zero-trust architect designing granular workload segmentation.

## When to use
- Designing zero-trust network for multi-tier applications
- Moving from perimeter security (IP ranges) to identity-based access
- Mapping application dependencies and critical data flows
- Preventing lateral movement in case of endpoint compromise
- Implementing least-privilege access across organization

## 5-Gate Artifacts
1. **Application Architecture & Dependency Map**: Services, data flows, inter-service communication, criticality tiers, data classification
2. **Workload Identity Framework**: Identity attributes (app, environment, tier, owner, data sensitivity), tagging strategy, directory integration
3. **Microsegmentation Policy Design**: Service-to-service allow list, deny default, encryption mandates, user context rules
4. **Implementation Roadmap**: Phase 1 (critical apps), Phase 2 (secondary), Phase 3 (permissive), rollout schedule, success metrics
5. **Monitoring & Audit Dashboard**: Policy enforcement rate, blocked flows, identity anomalies, audit trail (6+ month retention)

## Key Configuration
- **Zero-Trust Model**: Assume breach; verify every access request; no implicit trust based on network location
- **Workload Identity**: Each workload identified by attributes (application name, environment, tier, data sensitivity); not IP address
- **Application Segmentation Groups (ASG)**: Logical grouping of workloads by application tier; policies reference ASGs, not individual IPs
- **Service-to-Service Policies**: Explicit allow rules (web tier → API tier on port 8080, API tier → database on port 5432); everything else denied
- **User-to-Application Policies**: If applicable (e.g., admin SSH), require user identity from Okta/Azure AD; group-based access
- **Data Sensitivity Tiers**: Public, internal, confidential, restricted; policies enforce encryption for higher tiers
- **Encryption Policy**: TLS 1.3 mandatory between workloads; certificate validation enforced; self-signed certs rejected
- **Exception Handling**: Documented exceptions (legacy systems, third-party integrations) with business justification and expiration date
- **Automated Dependency Discovery**: Tools (Cisco Tetration, Zscaler workload tagging, cloud-native inventory) identify communication patterns
- **Policy Conflict Resolution**: If multiple policies match, most restrictive applied; audit log shows which policy blocked traffic
- **Performance Impact**: Microsegmentation inspection adds latency; measure and optimize for performance-critical services

## Gotchas
- **Over-Segmentation Paralysis**: Creating too many micro-segments causes policy explosion and operational complexity; balance security with maintainability
- **Legacy App Incompatibility**: Old applications may use dynamic ports or require permissive firewall rules; inventory legacy apps before microsegmentation
- **Dependency Discovery Incomplete**: Automated discovery misses occasional flows (batch jobs, disaster recovery, testing); manual validation essential
- **Failover Routing**: If backup workload in different ASG, failover may violate microsegmentation rules; plan failover identity in advance
- **Container Auto-Scale**: New container instances may take minutes to inherit proper identity tags; ensure orchestration (Kubernetes, Docker Swarm) tags automatically
- **Multi-Cloud Complexity**: If deploying across AWS, Azure, GCP, workload identity must be unified; no vendor-specific identity schemes
- **Encryption Overhead**: Enforcing TLS everywhere increases CPU load; validate performance impact on high-throughput services
- **Certificate Management Burden**: Per-service certificates require renewal and rotation; consider using service mesh (Istio) for automatic cert management
- **Third-Party Integration**: SaaS apps or external APIs may not fit microsegmentation model; carve out exceptions or use API gateway
- **Migration Disruption**: Implementing microsegmentation on live systems causes traffic disruptions; phased rollout and extensive testing required

## Microsegmentation Phases

**Phase 1: Critical Assets (Months 1-3)**
- Identify highest-value applications and data
- Map dependencies for critical tier only
- Deploy policies for critical workloads
- Monitor and tune rules

**Phase 2: Secondary Systems (Months 4-6)**
- Expand to non-critical applications
- Integrate directory services for user context
- Enable encryption enforcement
- Audit policy effectiveness

**Phase 3: Complete Coverage (Months 7-12)**
- Legacy system exemptions resolved or deprecated
- Workload identity fully deployed across organization
- Advanced analytics (anomaly detection) enabled
- Continuous compliance verification

## Configuration Checklist
- [ ] Application dependency map created (manual inventory + automated discovery tools)
- [ ] Workload identity attributes defined (app, env, tier, sensitivity) and tagging strategy automated
- [ ] Directory integration (Okta, Azure AD) connected for user-based policies
- [ ] Microsegmentation policy language chosen (Zscaler ASGs, cloud native, or hybrid)
- [ ] Encryption policy enforced (TLS 1.3 minimum, certificate validation)
- [ ] Certificate management automated (CA integration, auto-renewal)
- [ ] Legacy app exceptions documented with business justification and expiration dates
- [ ] Failover and disaster recovery routing validated against policies
- [ ] Container orchestration (Kubernetes, Docker) auto-tagging configured
- [ ] Monitoring dashboard set up (policy enforcement, blocked flows, audit logs)
- [ ] Phase 1 critical apps identified and policies deployed
- [ ] Testing plan established (pre-production validation before production rollout)
- [ ] Training provided to operations team on policy management and troubleshooting
- [ ] Success metrics defined (deployment time, incident detection time, false positive rate)
