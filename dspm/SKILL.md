---
description: "Deploy Data Security Posture Management to discover, classify, and monitor sensitive data across cloud storage"
---

**Cloud Data Architect** | Zscaler Zero Trust Exchange | Data Governance Lead

Continuously scan and classify sensitive data stored in S3, Azure Blob Storage, and Google Cloud Storage; alert on misconfigurations and exposure risks; enforce data retention policies.

## When to use

- Discovering unmanaged data repositories (stray S3 buckets, orphaned storage accounts, developer-created Blob storage)
- Classifying stored data (PII, credit cards, source code, database backups, customer records) using DLP patterns
- Alerting on exposure risks (public S3 buckets, overly permissive Azure RBAC, unencrypted storage, overshare)
- Enforcing data retention (delete old customer data per GDPR, purge test data with PII, archive cold data)
- Generating compliance evidence (data inventory, retention audit, classification consistency)
- Implementing data minimization (identify and remove unused datasets, consolidate duplicates)
- Supporting incident response (identify what data accessed during breach, who had access, retention period)

## 5-Gate Artifacts

1. **Cloud Storage Inventory** - All S3 buckets, Azure storage accounts, GCS buckets discovered via API scan, with owner, creation date, last modified, access control posture, encryption status, public access status, version control enabled

2. **Data Classification Rules** - Patterns for PII, PHI, PCI, source code, logs, database backups applied recursively to all discovered storage; machine learning classifiers for content-based detection; manual verification for ambiguous classifications; quarterly rule updates

3. **Exposure Risk Matrix** - S3 public ACL/policy, Azure public share settings, GCS public access, unencrypted objects, overly permissive IAM, old unreviewed shares (>6 months), lack of MFA delete protection, versioning disabled, default encryption missing

4. **Remediation Playbook** - Auto-encrypt unencrypted objects (customer approval required first), revoke public access, move sensitive data to restricted buckets, delete expired data (with retention hold check), owner notification workflow, forensic preservation for deleted data

5. **Compliance Report** - Data inventory by sensitivity level, exposure statistics (# public, # unencrypted), remediation status with SLAs, retention adherence, audit trail for compliance reviews, data minimization metrics (duplicate identification, unused dataset identification)

## Key Configuration

- **Cloud Credentials & Discovery**: Deploy service accounts (AWS IAM, Azure managed identity, GCP service account) with read-only permissions for scanning; rotate credentials quarterly; implement principle of least privilege

- **Scanning Schedule**: Full scan weekly for datasets <1TB, incremental daily for high-sensitivity buckets; monitor scan duration and optimize for large datasets; implement parallel scanning for multi-cloud

- **Classification Accuracy**: Use context (folder name "HR" + filename "salary.xlsx" + PII pattern) to improve classification; manual review for ambiguous matches; track classification accuracy and refine rules quarterly

- **Access Control Assessment**: Compare current permissions against least-privilege baseline; track and alert on permission creep (gradual expansion of user access); implement quarterly access reviews

- **Data Lifecycle Policies**: Define retention periods (customer data 7 years, logs 1 year, test data 30 days) mapped to regulations; automate deletion with hold check; require manager approval for exceptions; track data age distribution

- **Performance Optimization**: Implement bucket-level sampling for very large datasets (>100M objects); prioritize high-sensitivity classifications; cache discovery results to avoid re-scanning unchanged buckets

## Gotchas

- DSPM scans enumerate all objects; in large S3 buckets (>100M objects), cost/time can be prohibitive; use prefix filtering and sample-based scanning for initial assessment; estimate costs before rollout

- Encryption at rest (AWS S3-SSE) hidden from DSPM; appears encrypted even if keys stored in same AWS account; audit encryption key management separately and enforce customer-managed keys (CMK)

- PII patterns flag many false positives (product codes, order IDs, test data); maintain allowlist of non-sensitive patterns and automatically suppressed buckets; track false positive rate and refine rules

- Moving sensitive data to "restricted" buckets doesn't prevent exfiltration; enforce read-only IAM policies, enable CloudTrail/audit logging, detect unusual access patterns (bulk download spike)

- Data retention deletion delays: soft delete (move to archive tier) vs. hard delete (overwrite, 90-day recovery) create compliance gaps; verify deletion method and retention hold compliance before deletion

- Sensitive data classifications (credit card, SSN) may need PII redaction in DSPM reports themselves; don't leak PII through remediation logs; redact actual data in reports and retain separately

- Newly discovered buckets with sensitive data create urgency; prioritize remediation but coordinate with data owners to avoid breaking applications; implement staged enforcement (notify, monitor, restrict)
