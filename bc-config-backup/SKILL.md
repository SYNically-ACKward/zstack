---
description: "Backup Zscaler config: API export, version control, restore procedure, drift detection"
---

# BC Config Backup

**Persona:** Systems administrator managing configuration backups and version control.

## When to use
- Establishing config backup strategy and retention policy
- Exporting current ZIA/ZPA policy and settings via API
- Storing backups in version control (Git) with change history
- Detecting configuration drift between primary and BC cloud
- Restoring config after accidental change or during disaster recovery

## 5-Gate Artifacts
1. **Backup Schedule Plan**: Frequency (hourly/daily/on-change), retention period (30/90/365 days), storage location
2. **API Export Script**: Automated Zscaler API calls for policy, user groups, apps, DLP, firewall rules export
3. **Git Repository Structure**: Branches for environments (prod, staging, dr), commit messages with change descriptions
4. **Drift Detection Report**: Periodic comparison of current primary config vs backup; identifies untracked changes
5. **Restore Runbook**: Step-by-step procedure to import backup, validation checks, rollback if import fails

## Key Configuration
- **ZIA API Export**: Policy rules, user groups, URL categories, DLP profiles, certificate management, admin roles
- **ZPA API Export**: Application segments, access policies, server groups, browsers, connectors, enrolment certificates
- **API Credentials**: OAuth tokens with read-only scope; rotation every 90 days to limit breach exposure
- **Export Frequency**: Hourly for Gold SLA (1-hour RPO), 6-hourly for Silver, daily for Bronze; on-demand for emergency backup
- **Backup Storage**: Git repository (GitHub/GitLab) with branch protection and MFA for pushes; also store encrypted copies in S3/Blob
- **File Format**: JSON for API exports (human-readable diff); optional YAML for ease of import; avoid binary formats
- **Compression**: If storing locally, gzip to save space; remote storage (Git, cloud) handles compression automatically
- **Encryption**: Encrypt exports containing sensitive data (API keys, DLP patterns) with GPG or cloud encryption at rest
- **Version Tags**: Tag each backup with date and change summary (e.g., "2025-03-17-added-office365-policy")
- **Drift Detection**: Run nightly script comparing current config snapshot vs previous night's; alert if > 5% change

## Gotchas
- **API Rate Limit**: Large policy set (1000+ rules) may hit API rate limit; batch requests and add delay between calls
- **Credentials Leakage**: If backup contains API keys or admin tokens, expose in Git history; use secrets manager (HashiCorp Vault, AWS Secrets) and never commit secrets
- **Binary Blobs**: Don't export certificates/private keys; only export cert references (serial, thumbprint); store private keys separately
- **Import Side Effects**: Importing config doesn't delete removed policies; must manually clean old rules or use import-with-replace flag
- **Merge Conflicts**: If multiple admins edit config simultaneously, Git branches diverge; requires manual conflict resolution
- **Large Config Size**: If policy count grows to 10k+ rules, export takes 30+ minutes; schedule during low-traffic windows
- **API Endpoint Drift**: Zscaler API evolves; older export scripts may fail on new API versions; version scripts and test after Zscaler updates
- **Multi-Tenant Export**: If managing multiple tenants, export each separately; no bulk cross-tenant export capability
- **Backup Stale Data**: If export automation breaks silently, backup may not update for days; add heartbeat monitoring (alert if no commit in 24h)
- **Restore Incomplete**: Importing subset of config (e.g., policies only) doesn't import user groups; dependencies must be satisfied first

## Configuration Checklist
- [ ] Backup schedule defined (hourly/daily) and retention period approved (minimum 30 days)
- [ ] API credentials created with read-only scope and stored in secrets manager
- [ ] Export script tested in lab environment and validated for completeness
- [ ] Git repository created with branch protection rules and MFA enforcement
- [ ] First backup executed and commit pushed successfully
- [ ] Drift detection script scheduled and alert thresholds configured
- [ ] Restore procedure tested with sample config import (non-prod environment)
- [ ] Encryption configured for sensitive data (GPG, cloud KMS)
- [ ] Backup file integrity checks in place (checksum, size validation)
- [ ] Escalation procedure defined if backup automation fails (email, PagerDuty alert)
- [ ] Quarterly restore drill scheduled to validate backup usability
