---
description: "Implement cloud security posture management with misconfiguration detection, drift monitoring, and automated remediation"
---

**Cloud Posture Manager** | Zscaler Zero Trust Exchange | Cloud Configuration Lead

Deploy cloud security posture management to detect infrastructure misconfigurations (overpermissive IAM, unencrypted storage, exposed data), monitor drift from baseline, and automate remediation.

## When to use

- Discovering cloud infrastructure misconfigurations (S3 bucket public, IAM overpermissive, security groups open to 0.0.0.0/0)
- Detecting configuration drift (policy changes, access permission expansion, security control removal)
- Automating remediation of common misconfigurations (revoke overpermissive policies, encrypt storage, close security groups)
- Maintaining compliance with CIS benchmarks and cloud security best practices
- Scaling posture management across multi-cloud (AWS, Azure, GCP) and multi-account environments

## 5-Gate Artifacts

1. **Posture Assessment Framework** - Continuous scanning of all cloud resources (VMs, storage, networks, IAM, databases); categorization by severity (critical: public data exposure, high: overpermissive access)
2. **Misconfiguration Baseline** - Establish approved configurations (S3 default encryption, IAM least privilege, security group restrictions); score infrastructure against baseline
3. **Drift Detection Strategy** - Monitor for policy changes (new policy statement added, encryption disabled, security group rule modified); alert on drift from baseline within 5 minutes
4. **Automated Remediation Playbooks** - High-confidence remediations (revoke principal.*:* policy, encrypt bucket, restrict SG to specific IPs); low-confidence require approval (delete resource, change app behavior)
5. **Multi-Cloud Posture Dashboard** - AWS, Azure, GCP compliance score, misconfiguration count by severity, critical findings requiring immediate attention, trend over time

## Key Configuration

- **Continuous Scanning**: Deploy posture scanner (CloudSploit, Prowler, Dome9) daily or real-time via API; maintain asset inventory (all resources discovered)
- **Remediation Automation**: Auto-remediate high-confidence findings (encrypt S3, restrict SG 0.0.0.0/0, remove public access); require manual approval for resource deletion or access changes
- **Baseline Enforcement**: Define approved configurations per team/environment (prod stricter than dev); block non-compliant changes via policy (prevent creation of public S3 bucket)
- **Exception Management**: Allow documented exceptions (dev environment less restrictive, legacy system cannot encrypt); require re-review quarterly
- **Reporting & Alerting**: Daily dashboard (critical findings count, remediation rate), weekly report (new misconfigs, fix rate), executive monthly (posture trend, SLA compliance)

## Gotchas

- Cloud service capability differences (AWS KMS vs. Azure Key Vault) complicate baseline; allow service-specific configurations; maintain mapping of equivalent controls across clouds

- Remediation side effects (removing overpermissive policy breaks app access) require coordination with app team; test remediation in staging first; implement staged remediation with validation gates

- Shadow IT (developers spinning up own resources outside posture scanning scope) defeats program; enforce governance policy to require scanning before resource usage; monitor for API usage anomalies

- Drift detection noisy: legitimate policy changes (adding new principal to bucket ACL) trigger alerts; implement smart baselining (expected principal additions don't flag); maintain approved change whitelist

- Posture scanner credentials exposed (AWS IAM keys for scanning) allow attacker to modify findings; use temporary credentials (STS, managed identity), rotate frequently; monitor for credential abuse

- Auto-remediation too aggressive creates production outages; implement phased remediation (alert 24h, log 24h, enforce 48h+manual approval); measure remediation success rate and side effects

- Compliance evidence requirements unclear: audit asks for proof of encryption but posture scanner only checks config; maintain supplementary evidence (encryption key audit, certificate validation) for audits
