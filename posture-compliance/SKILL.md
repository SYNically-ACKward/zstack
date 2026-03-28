---
description: "Generate compliance evidence mapping cloud posture controls to CIS, NIST, SOC2, PCI-DSS, and HIPAA requirements"
---

**Compliance Architect** | Zscaler Zero Trust Exchange | Regulatory Compliance Lead

Map cloud security posture controls to regulatory frameworks (CIS benchmarks, NIST 800-53, SOC2, PCI-DSS, HIPAA) and generate evidence for audit and compliance reviews.

## When to use

- Preparing for external audits (SOC2 Type II, PCI-DSS, HIPAA) requiring cloud configuration evidence
- Meeting compliance requirements for industry verticals (finance, healthcare, government)
- Automating control validation (no manual checklist review)
- Generating compliance reports for business continuity and risk management
- Tracking control effectiveness over time and identifying remediation trends

## 5-Gate Artifacts

1. **Compliance Control Mapping** - Map cloud posture controls to CIS v8, NIST 800-53, SOC2 criteria, PCI-DSS requirement, HIPAA control ID; track evidence requirements per control
2. **CIS Benchmark Assessment** - CIS AWS Foundations Benchmark v1.5 (e.g., CIS 1.1: root account MFA enabled), CIS Azure Foundations v1.4, CIS GCP Foundations v1.3; auto-score against benchmark
3. **NIST 800-53 Evidence Collection** - Map posture controls to NIST control family (AC: Access Control, SC: System and Communications Protection); collect evidence of implementation (policy doc, config screenshot, audit log)
4. **SOC2, PCI-DSS, HIPAA Reporting** - Generate audit-ready reports with control status (implemented, partial, non-compliant), evidence attachments, remediation plan for gaps
5. **Audit Trail & Change Log** - Document all control changes (config update, policy revision), timestamp, approver; maintain immutable audit log for compliance reviews

## Key Configuration

- **Automated Control Assessment**: Use compliance-scanning tools (CloudSploit for CIS, ScoutSuite for multi-cloud) integrated with posture management; auto-generate CIS score
- **Evidence Collection**: Export posture findings with context (resource name, configuration, evaluated date); attach policy documents, access logs, encryption keys (encrypted)
- **Control Status Tracking**: Red (non-compliant), yellow (partial/requires review), green (compliant); track remediation SLA per control; update status post-remediation
- **Audit Report Generation**: Export compliance report per framework (CIS, NIST, SOC2, PCI, HIPAA) with control summary, evidence, gaps, remediation timeline
- **Change Management Integration**: All cloud changes logged with change ticket; audit trail exported for compliance reviews; controls validated 24 hours post-change

## Gotchas

- Control interpretation varies by framework; same cloud config may be compliant with CIS but not SOC2; require expert review for edge cases; maintain control interpretation mapping across frameworks

- Evidence collection for legacy controls (manual review) not automated; maintain supplementary evidence (policy doc, email trail) for controls without automated evidence; prioritize automation for manual controls

- Remediation timeline mismatch: audit scheduled 30 days out, control non-compliant, remediation requires 60 days coordination; start remediation early and track in risk register; communicate timeline to auditors

- Compliance score gaming: team marks control "compliant" without verification; implement quarterly audit of random controls to verify evidence accuracy; implement independent assurance sampling

- Cross-control dependencies: control A depends on control B; when B fails, A effectiveness questioned; document dependencies and cascade impact; implement dependency tracking in control database

- Regulatory requirement changes: CIS v9 released, NIST updated, HIPAA guidance clarified; subscribe to regulatory updates and plan control re-evaluation annually; maintain version control of frameworks

- Control remediation evidence preservation: delete old compliance reports without archiving; implement immutable evidence storage (e.g., WORM storage) for audit trail and historical compliance proof
