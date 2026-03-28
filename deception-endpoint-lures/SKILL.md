---
description: "Deploy endpoint deception lures including SSH keys, RDP shortcuts, credential files, and canary tokens"
---

**Endpoint Deception Analyst** | Zscaler Deception Intelligence Platform | Endpoint Lures Lead

Implement endpoint-based deception (fake SSH keys, RDP shortcuts, credential files, canary tokens) through Zscaler Client Connector (ZCC) and lateral distribution to detect endpoint compromise.

## When to use

- Detecting compromised endpoints by planting realistic decoy credentials and monitoring access
- Identifying lateral movement attempts when attacker searches for stored credentials
- Alerting on suspicious file access patterns (why is this user accessing a decoy RDP shortcut?)
- Generating early warning of endpoint malware seeking credentials for lateral movement
- Training security teams on realistic attack scenarios with canary tokens

## 5-Gate Artifacts

1. **Endpoint Lure Inventory** - Type (SSH keys, RDP shortcuts, password files, .aws credentials, database connection strings), location (home directory, Desktop, Documents, Git directory), naming (realistic vs. conspicuous), frequency of deployment
2. **ZCC Integration & Distribution** - Deploy lures via Zscaler Client Connector to all managed endpoints; use policy-based targeting (all users, specific departments, high-risk roles); versioning for tracking
3. **Canary Token Strategy** - Unique tokens embedded in decoy files (spreadsheet pixel, email beacon, document link); external callback URL records access timing, source IP, user, host
4. **File Access Monitoring** - Monitor for decoy file opens (Registry, file system, email body parsing); trigger alert on suspicious patterns (bulk read of RDP shortcuts, credential file enumeration)
5. **Incident Response Runbook** - Lure triggered → validate source (endpoint legitimate?), check for concurrent malware activity, enable full forensics on endpoint, isolate if needed, post-mortem analysis

## Key Configuration

- **SSH Key Lures**: Generate OpenSSH private keys with decoy passphrases; place in ~/.ssh/id_rsa with comments indicating known hosts (real-looking connection context)
- **RDP Shortcut Lures**: Create RDP connection files (.rdp) pointing to non-existent IP addresses; use realistic server names (db-backup, admin-server, exchange-01)
- **Credential File Lures**: Create realistic-looking password files (export from bitwarden, LastPass format) in common locations; include canary token in file content or filename
- **Canary Token Embedding**: Use unique identifiers per endpoint + per file; implement callback mechanism (DNS query, HTTP request) to external server; log requestor context
- **Deployment Targeting**: Employees in sensitive roles (finance, IT, executives) receive higher-fidelity lures; frequency of deployment balanced to avoid desensitization

## Gotchas

- Lure effectiveness decreases with volume; too many honeypots cause user frustration and security fatigue; deploy judiciously (1-3 per user initially); measure engagement and effectiveness

- Endpoint detection evasion by attacker (deleting lures, scanning for canary tokens) indicates sophisticated adversary; adjust monitoring to watch for deletion of decoy files; implement immutable backups

- Canary token callback latency (5-30 seconds) misses real-time response; implement local logging as fallback (EDR agent captures decoy file access); sync with centralized logging <5 sec

- Lure artifacts exposed (RDP shortcut with obvious fake IP, password file with "honeypot" in content) training reduces future effectiveness; update lure content quarterly; test lures with security team

- False positives from legitimate use (IT admin testing access to decoy server, backup process reading credential file) require whitelist; correlate with user context and job function

- Canary token exposure risk: if callback URL logged in plain text, attacker discovers canary token infrastructure; use encrypted callbacks and IP geofencing; implement multiple callback methods

- Lure staging overhead: deploying thousands of decoy SSH keys across fleet is resource-intensive; implement selective deployment (high-risk users) and automated key rotation quarterly
