---
description: "Sovereign cloud deployment: data residency, regional clouds, compliance (GDPR/Schrems II), key management"
---

# Sovereign Cloud

**Persona:** Compliance officer and cloud architect deploying Zscaler in sovereign cloud regions.

## When to use
- Ensuring data residency compliance for regulated industries (GDPR, HIPAA, FCA, LGPD)
- Deploying in regional Zscaler clouds (EU, Japan, Singapore, Australia, GCC) for data sovereignty
- Managing encryption keys with customer-managed encryption (CMEK) for data control
- Validating third-party audit findings (SOC2, ISO 27001) for sovereign region
- Data localization requirements preventing data transit through non-sovereign infrastructure

## 5-Gate Artifacts
1. **Compliance Requirement Matrix**: Regulation (GDPR, HIPAA, etc.) → data residency requirement, encryption mandate, audit frequency
2. **Zscaler Sovereign Cloud Architecture**: Regional cloud selection (EU, Japan, etc.), data flow diagram, backup location, encryption key management
3. **Data Residency Audit Trail**: Policy ensuring all user data (logs, config, stats) processed and stored in sovereign region
4. **Customer-Managed Encryption Key (CMEK) Setup**: Key management solution (AWS KMS, Azure Key Vault, Vault), key rotation policy, access controls
5. **Compliance Evidence Report**: Audit finding responses, attestation letters, privacy addendum signed, data processing agreements (DPA) filed

## Key Configuration
- **Regional Clouds**: EU cloud (zscaler.eu), Japan cloud (zscaler.co.jp), Singapore cloud (zscaler.sg), Australia cloud (zscaler.com.au)
- **Data Residency**: All user data, logs, policies, statistics processed in region; no data replication to non-sovereign clouds
- **Encryption at Rest**: Zscaler provides default encryption; optional CMEK allows customer to manage keys independent of Zscaler
- **Encryption in Transit**: All inter-component and user-to-cloud traffic TLS 1.3; certificate issued by regional CA if required by compliance
- **GDPR Compliance**: Cloud Processor Agreement (CPA) signed; DPA establishes data processing terms; Data Protection Impact Assessment (DPIA) conducted
- **Schrems II Compliance**: After Schrems II ruling, US cloud restricted for EU data; must use EU cloud; assess if supplementary safeguards needed
- **Privacy Addendum**: Signed by Zscaler confirming regional data processing and residency guarantees
- **Audit Rights**: Compliance includes audit rights; Zscaler permits third-party audit of regional infrastructure
- **CMEK Rotation**: If using customer-managed keys, rotate every 90 days; Zscaler supports rotation without service disruption
- **Breach Notification**: Zscaler commits to breach notification within 24-48 hours; customer then notifies regulators per GDPR (72-hour deadline)
- **Backup and DR**: Backups stored in same region; disaster recovery to secondary region if both regions in same sovereign geography

## Gotchas
- **Schrems II Unresolved**: If contract includes "standard contractual clauses (SCCs)" but Schrems II ruling voids SCC adequacy, compliance gaps; add supplementary safeguards
- **Key Escrow Requirement**: Some jurisdictions require government key escrow; CMEK mitigates by keeping keys outside Zscaler control
- **Personnel Clearance**: Zscaler staff accessing sovereign cloud may require security clearance; onboarding delays if paperwork incomplete
- **Cloud Availability**: Regional clouds may have scheduled maintenance; EU cloud maintenance windows may differ from US schedule; plan deployments carefully
- **Reduced Feature Set**: Regional clouds may lag main cloud in feature releases; verify feature availability before procurement
- **Backup Location Ambiguity**: If primary regional cloud fails, backup location may violate residency if in non-sovereign region; clarify backup SLAs
- **CMEK Complexity**: Customer responsible for key management; lost key = permanent data loss; strong access controls and audit logging required
- **Compliance Certification Gap**: Regional cloud audit may be 1-2 years old; verify if refresh available before relying on audit findings
- **Regulatory Interpretation**: Each jurisdiction interprets residency differently (data location vs data controller vs data processor); legal review mandatory
- **Migration Overhead**: Migrating from global to sovereign cloud requires data re-ingestion; plan for downtime or parallel operation

## Configuration Checklist
- [ ] Data residency requirement confirmed with legal and compliance teams
- [ ] Applicable regulations identified (GDPR, HIPAA, LGPD, FCA, etc.) and interpretation documented
- [ ] Zscaler sovereign cloud region selected and latency validated from key user locations
- [ ] Cloud Processor Agreement (CPA) and Data Processing Agreement (DPA) negotiated and signed
- [ ] CMEK solution evaluated (AWS KMS, Azure Key Vault, customer Vault) and procurement started
- [ ] Encryption at rest and in transit confirmed in Zscaler documentation
- [ ] Audit findings for sovereign region obtained and gaps remediated
- [ ] Privacy Addendum signed by both parties with data residency guarantees
- [ ] Disaster recovery location confirmed to be within sovereign geography
- [ ] Backup and restore procedure tested in sovereign cloud environment
- [ ] Breach notification procedure reviewed and validated for < 24-hour notification
- [ ] Key rotation schedule documented (90-day frequency if CMEK enabled)
- [ ] Personnel clearance requirements assessed if applicable
- [ ] Compliance monitoring dashboard configured (audit log retention, key usage, data location verification)
