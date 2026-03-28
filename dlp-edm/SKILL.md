---
description: "Implement Exact Data Match for precise detection of sensitive datasets with minimal false positives"
---

**EDM Policy Specialist** | Zscaler Secure Internet Gateway | Precision Data Detection

Deploy Exact Data Match (EDM) techniques to identify confidential datasets with surgical accuracy, supporting hash-based indexing and field-level matching for regulated compliance scenarios. Maximize detection precision by matching against known sensitive record inventories.

## When to use

- Detecting specific customer records, financial accounts, or proprietary lists (e.g., "VIP customer list", "key accounts")
- Identifying personal data from structured databases (HR employee records, patient lists, financial account numbers)
- Preventing exfiltration of proprietary source code commit hashes or build artifacts
- Meeting compliance requirements for breach notification (known individual records only)
- Reducing false positives from pattern-based DLP in high-volume environments (financial institutions)
- Protecting intellectual property (competitor IP, trade secrets) with exact inventory matching
- Implementing zero-trust data access policies for sensitive customer/patient data

## 5-Gate Artifacts

1. **EDM Index Definition** - Source system mapping (SFTP, SQL Server, cloud DB export), field selection (customer ID, email, phone), hash algorithm (SHA-256), refresh cadence (daily/weekly), version control and rollback strategy, storage location (on-premises vs. cloud)

2. **Data Export & Hashing Process** - Extract data from authoritative source, PII scrubbing for audit trail, create fingerprint index using cryptographic hash, secure transmission to Zscaler (encrypted channel, certificate pinning), versioning strategy with rollback capability

3. **Index Performance Baseline** - Measure hash lookup latency (<50ms per match), throughput (QPS per appliance), storage footprint (GB/million records); document refresh window (e.g., "1GB index, 4-hour refresh"), peak load handling, and scalability across appliances

4. **Field-Level Matching Rules** - Define which fields must match (e.g., first name + last name + DOB vs. email alone), minimum match confidence (exact 1.0 vs. fuzzy phonetic 0.8), field normalization rules (case-insensitive, remove whitespace), composite key cardinality

5. **Incident Response Runbook** - Detection alerting with confidence score, data context logging (matched fields, requestor, timestamp, source IP, application), automated containment (block user session, quarantine file, notify user), forensic data preservation, escalation SLA

## Key Configuration

- **Hash Repository Deployment**: Maintain secure import pipeline with data quality validation (remove duplicates, normalize formatting, validate field types); implement change tracking for audit

- **Multi-Field Matching**: Configure composite keys (last name + DOB) to match complete records; single field reduces false positives but increases false negatives; document trade-off rationale

- **Refresh Cadence**: Balance freshness (new customer onboarding detection) vs. index build time; typical cadence is daily for <500K records, weekly for >5M; schedule during low-traffic windows

- **Performance Tuning**: Use index sharding for datasets >10GB; monitor hash lookup CPU on gateway appliances during updates; implement parallel index builds for large datasets

- **Audit Logging**: Capture every EDM match with matched field values (hashed), source IP, application, timestamp, user identity; retain logs per regulatory retention policy (7 years for some industries)

- **Data Quality Controls**: Implement source validation (check for orphaned records, stale data), periodic sample verification (spot-check matches against authoritative source), reconciliation reports

## Gotchas

- EDM matches are "all or nothing"; partial field matches can be missed if whitespace or formatting differs in source data; implement normalization to handle variations

- Hash uploads expose sensitive data during transfer; use encrypted SFTP channels with certificate pinning, implement network segmentation, audit upload access logs

- Index refresh windows create detection gaps; if customer record added at 11:55 PM with daily midnight refresh, won't be detected for 24+ hours; balance with real-time requirements

- False negatives occur if source data not current (stale customer exports); synchronize refresh with operational data system updates; implement data quality monitoring

- High cardinality fields (email addresses) with EDM + pattern matching create duplicate detections; implement correlation logic to deduplicate alerts before incident response

- Multi-field EDM requires all fields to match exactly; if one field sanitized differently at source, match fails silently; test with real-world data for each field combination

- Index size growth over time (accumulated new records without pruning) impacts lookup performance; implement archive strategy for historical records and quarterly index cleanup
