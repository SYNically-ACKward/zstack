---
description: "Configure API-based CASB for out-of-band SaaS scanning and retroactive user activity auditing"
---

**API Security Engineer** | Zscaler Zero Trust Exchange | Cloud Forensics Lead

Deploy out-of-band CASB connectors to M365, Google Workspace, Salesforce, and Box for continuous user activity auditing, data exposure detection, and retroactive compliance scanning. Implement API-based discovery and monitoring for comprehensive cloud security posture and user behavior analytics.

## When to use

- Auditing user activity in SaaS apps (file shares, user permissions, external access, sharing links created)
- Detecting compromised cloud accounts (bulk file deletions, unusual share activity, impossible travel)
- Discovering sensitive data in SharePoint, Google Drive, Salesforce databases through classification and pattern matching
- Enforcing data governance (remove public shares, revoke old external access, enforce retention policies)
- Generating compliance reports (who accessed customer data, when, from where, what did they do)
- Implementing automated response (quarantine suspicious shares, revoke access, revoke OAuth tokens)
- Investigating breach scope and lateral movement through cloud apps after security incident

## 5-Gate Artifacts

1. **SaaS Connector Deployment Plan** - M365 (Graph API service principal with Files.ReadWrite.All + User.Read.All), Google (service account with Directory.Read + Drive.Read), Salesforce (OAuth connected app with API + Metadata), Box (JWT auth with read-only scope), with scope minimization and regular permission audits

2. **Scanning Schedule & Scope** - Daily full scan of file permissions + shares for <10K users, hourly incremental for high-risk folders (Finance, Legal, HR), weekly Salesforce record access audit, monthly GCS/S3 permission audit

3. **Activity Detection Rules** - Bulk delete (>50 files in 1 hour = exfiltration indicator), external share creation (especially to competitor domains), admin privilege elevation, failed login from impossible travel location (NYC to Shanghai in <4 hours), API token generation by non-IT user

4. **Quarantine & Remediation** - Automated: restore deleted files from backup, revoke external shares (notify user with business impact), disable compromised user session, revoke OAuth tokens; Manual: security team approval for permission changes, legal hold for sensitive files

5. **Compliance Dashboard** - Monthly activity report by user/app with access patterns, violation trends, remediation closure rate, user permission exceptions, data classification changes, external access inventory

## Key Configuration

- **OAuth/Service Principal Scopes**: Request minimum required permissions; M365 needs Files.ReadWrite.All + User.Read.All for audit; Google needs oauth2/v1/userinfo + drive.readonly; rotate credentials quarterly

- **Graph API Batch Operations**: Query files, permissions, sharing links in batches (up to 20 per request); optimize for large tenant scanning (>50K items); implement exponential backoff for throttling

- **Incremental Scanning**: Maintain change log with lastModified timestamps; scan only modified files daily rather than full snapshot to reduce API quota burn; implement full scan monthly for discrepancies

- **Activity Baseline Profiling**: Collect 2-week user behavior baseline (login frequency, device types, geographic locations, file access patterns) before alerting on anomalies; separate service account baselines from user baselines

- **Remediation Workflows**: Integrate with ServiceNow or Jira for approval; tag tickets with regulatory domain (HIPAA, PCI) for expedited review; track remediation time and closure rate

- **Data Quality Controls**: Monitor for API failures (incomplete scans); implement retry logic with dead letter queue; validate data consistency across daily/weekly/monthly scans

## Gotchas

- SaaS API rate limits (M365 Graph throttling at 2K req/min, Google quota exhaustion) cause scanning gaps; implement backoff/retry with exponential delay; monitor quota consumption and scale accordingly

- Service principal permissions too broad expose entire tenant data; scope to specific sites/drives and apply least privilege; audit permission usage monthly and remove unused scopes

- Deleted files may not be queryable via API; maintain shadow copy of file metadata for forensics (requires custom ETL); implement soft delete retention (archive tier) for recovery

- External sharing restrictions enforced via CASB don't prevent users from re-sharing; combine with OneDrive/Drive tenant-level policies (require approval for external share); monitor policy compliance

- Compromised service principal (stolen credentials) allows attacker to manipulate audit logs; rotate credentials quarterly, enable MFA on service account, monitor for abuse (unusual API patterns)

- Retroactive scans find historical violations (public SharePoint sites) but can't undo exfiltration; focus on forward-looking detection + user behavior analysis; implement data retention cleanup for old violations

- API scanning latency (24-48 hours from event to finding available) misses real-time incidents; combine API-based scanning with real-time alerts from audit logs (Sentinel, Cloud Logging)
