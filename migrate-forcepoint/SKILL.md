---
description: "Migrate Forcepoint to Zscaler: WSC→ZIA, NGFW→cloud FW, DLP→DLP. Gotchas: hybrid→cloud, TLS conflict, DLP engine difference"
---

# Migrate Forcepoint

**Persona:** Security architect transitioning from Forcepoint hybrid security to Zscaler cloud-native platform.

## When to use
- Replacing Forcepoint Web Secure Cloud (WSC) with Zscaler ZIA
- Converting Forcepoint NGFW (on-premises or hybrid) to Zscaler cloud firewall
- Migrating Forcepoint DLP fingerprinting to Zscaler DLP identity matching
- Eliminating Forcepoint hybrid agent infrastructure (local + cloud) in favor of cloud-native ZCC
- Transitioning from Forcepoint UEBA (User and Entity Behavior Analytics) to Zscaler behavioral intelligence

## 5-Gate Artifacts
1. **Forcepoint Security Stack Inventory**: WSC cloud instances, on-premises NGFW appliances, DLP engine deployments, UEBA server, hybrid agent count
2. **Policy Export & Analysis**: WSC policies (URL filtering, threat, DLP), NGFW rules (firewalling, VPN), DLP fingerprint library; translation to Zscaler
3. **Hybrid Architecture Decommissioning**: On-premises Forcepoint NGFW appliances, local DLP engines scheduled for removal; cloud-native replacement strategy
4. **Agent Transition Plan**: Forcepoint hybrid agent removal, ZCC deployment timeline, coexistence testing, rollback plan
5. **Behavioral Analytics Mapping**: Forcepoint UEBA rules and anomaly detection → Zscaler behavioral analytics and threat intelligence

## Key Configuration
- **WSC to ZIA**: Forcepoint Web Secure Cloud (URL filtering, threat prevention, SSL inspection) → Zscaler ZIA; similar web gateway function
- **NGFW Replacement**: Forcepoint on-premises NGFW (firewalling, VPN, threat prevention) → Zscaler cloud firewall; appliance decommissioning
- **Hybrid to Cloud**: Forcepoint hybrid model (local appliance + cloud service) → Zscaler pure cloud (cloud proxy, cloud firewall, cloud connectors); architecture simplification
- **DLP Engine Migration**: Forcepoint DLP uses fingerprinting (cryptographic matching of sensitive data patterns); Zscaler DLP uses identity + machine learning; rule redesign needed
- **Agent Architecture**: Forcepoint hybrid agent (local + cloud communication) → ZCC lightweight agent (cloud only); simpler, fewer support issues
- **UEBA Replacement**: Forcepoint UEBA detects anomalous user behavior; Zscaler behavioral analytics (threat intelligence, sandboxing, C&C detection) provide similar protection at network level
- **Policy Language**: Forcepoint policy syntax differs from Zscaler; translation script or manual conversion required
- **SSL Inspection**: Forcepoint hybrid agent handles local SSL decryption; Zscaler cloud proxy handles SSL decryption centrally; certificate distribution differs
- **VPN Termination**: Forcepoint NGFW may terminate site-to-site VPNs; Zscaler connectors replace VPN termination; IPSec configuration migrated
- **Licensing Model**: Forcepoint hybrid (concurrent users, appliance count) → Zscaler (cloud throughput, concurrent users); licensing recalculation required

## Gotchas
- **Hybrid to Pure Cloud Paradigm Shift**: Forcepoint hybrid offers local decision-making; Zscaler requires cloud connectivity; offline capability lost; RTO expectations change
- **TLS Conflict**: Forcepoint hybrid agent and Zscaler ZCC may conflict on SSL inspection if both present; agent must be completely removed before ZCC enrollment
- **DLP Fingerprint vs Identity Difference**: Forcepoint DLP fingerprints match exact byte patterns; Zscaler DLP uses identity (username + data type); accuracy and false positive rates differ
- **On-Premises Appliance Decommissioning**: If Forcepoint NGFW handles site-to-site VPNs or has local policy enforcement; removal creates temporary routing gap; careful cutover needed
- **Behavioral Analytics Feature Gap**: Forcepoint UEBA user behavior profiling may be more advanced; Zscaler behavioral analytics network-level (app usage, threat detection) not user-level; training models differ
- **Policy Rule Count**: Forcepoint policies often fewer (simpler, more consolidated); migration may reveal policy gaps if previously relying on appliance-level filtering
- **Licensing Surprise**: Forcepoint hybrid licensing complex (per-user, per-appliance); Zscaler licensing simpler but if traffic spikes unexpectedly, cost implications; monitor usage
- **Regional Deployment**: If Forcepoint NGFW deployed in multiple regions; Zscaler cloud proxy inherently global; regional policy differences require careful mapping
- **Third-Party Integrations**: Forcepoint may integrate with SIEM, ticketing, or WAF; Zscaler integrations differ (API-based vs appliance log forwarding); re-engineering required
- **Performance Variance**: Forcepoint local agent caches decisions; Zscaler cloud-based requires internet connectivity for every policy decision; users perceive latency increase on slow links

## Migration Procedure
1. **Forcepoint Inventory**: Count WSC instances, NGFW appliances, hybrid agents; document policy scope
2. **Export Policies**: Extract WSC policies, NGFW rules, DLP fingerprints; catalog policy intent
3. **Translate to Zscaler**: Build policy translation (WSC → ZIA, NGFW → ZIA/ZPA/cloud FW, DLP → Zscaler DLP)
4. **Design DLP Replacement**: Forcepoint fingerprints → Zscaler identity-based DLP; test accuracy on sample sensitive data
5. **Plan Appliance Sunset**: If on-premises NGFW, schedule decommissioning after Zscaler traffic fully migrated
6. **Agent Rollout**: Deploy ZCC to pilot users; validate hybrid agent removal and ZCC functionality
7. **Policy Validation**: Run Zscaler policies on production traffic; measure enforcement accuracy vs Forcepoint
8. **Parallel Operation**: Maintain Forcepoint until Zscaler fully validated (2-4 weeks typical)

## Configuration Checklist
- [ ] Forcepoint WSC instance count and policy rule count documented
- [ ] On-premises NGFW appliance locations and site-to-site VPN dependencies mapped
- [ ] DLP fingerprint library exported and complexity assessed
- [ ] Policy translation (WSC → ZIA, NGFW → cloud FW) drafted for sample rules
- [ ] Hybrid agent version identified; removal procedure tested in non-prod
- [ ] ZCC deployment validated; agent coexistence tested (to confirm conflict)
- [ ] UEBA rules and anomaly detection thresholds documented; Zscaler behavioral analytics evaluated
- [ ] Regional policy differences (if multi-region) mapped to Zscaler cloud regions
- [ ] Third-party integrations (SIEM, ticketing) API endpoints updated for Zscaler
- [ ] DLP accuracy testing completed on sample sensitive data (compare Forcepoint vs Zscaler)
- [ ] Performance baseline established (on-premises vs cloud latency)
- [ ] Parallel operation plan created (WSC + Zscaler traffic sampling for 2-4 weeks)
- [ ] User communication prepared (hybrid appliance removal, cloud-only model change)
- [ ] Appliance decommissioning procedure and timeline documented
