---
description: "Design and deploy network honeypots for SSH, RDP, SMB, database services, and Active Directory SPN monitoring"
---

**Network Honeypot Engineer** | Zscaler Deception Intelligence Platform | Network Deception Lead

Implement network-based honeypots (SSH, RDP, SMB, databases, AD SPNs) to detect reconnaissance, lateral movement, and credential attacks across infrastructure.

## When to use

- Detecting brute force attacks on SSH, RDP, and other network services
- Capturing credentials used in lateral movement (SMB access, database login attempts)
- Identifying unusual network service usage patterns (Kerberoasting against decoy SPNs)
- Deploying honeypots across unused IP address space to detect network scanning
- Generating attack telemetry (tools, scripts, techniques) for threat intelligence

## 5-Gate Artifacts

1. **Network Honeypot Specification** - Service type (SSH, RDP, SMB, MySQL, MSSQL, AD SPN), emulation fidelity (basic banner vs. full interaction), fake credentials (username, password), logging/capture level
2. **Unused IP Strategy** - Scan existing network for unused IPs; deploy honeypots across unused address ranges; publish some IPs internally (decoy DNS entries) to attract internal attackers
3. **Port Emulation Configuration** - SSH: Accept password auth, log failed attempts + commands; RDP: Accept login, log access attempts; SMB: Respond to share enumeration, log connection details
4. **Kerberoasting Decoy** - Create fake AD SPN entries (MSSQLSvc, HTTP, LDAP); monitor for TGS-REQ queries; log requester, timing, and extracted hash
5. **Alert & Capture Rules** - Alert on successful authentication (credential compromise), brute force (X failed attempts in Y minutes), unusual protocol behavior (SQL injection attempt on port 3306)

## Key Configuration

- **Service Emulation**: Use high-fidelity honeypot tools (Cowrie for SSH, Honey, Kippo for RDP); balance realism (fewer false positives) vs. simplicity (faster deployment)
- **Credential Seeding**: Use believable usernames (admin, backup, support) and weak passwords; track which credentials get used in attacks (indicates compromise source)
- **Network Visibility**: Ensure honeypot traffic reaches SIEM; log source IP, authentication attempts, commands executed; preserve full traffic capture for forensics
- **Geographic Distribution**: Deploy honeypots in production subnets (near critical systems), on network edges (detect external reconnaissance), and in separate honeypot VLAN
- **Maintenance & Rotation**: Update decoy services quarterly; monitor for legitimate admin activity and adjust deployment; retire honeypots after major incidents to prevent attacker awareness

## Gotchas

- Honeypot traffic baseline noisy (legitimate port scans, failed DNS queries to decoy IPs) requires tuning; implement anomaly detection for >X connection attempts per hour; whitelist benign sources

- Service response timing (SSH banner delay, RDP connection timeout) differs from real services; attacker may detect honeypot by response timing; implement realistic service emulation and timing

- Decoy SPN credentials captured (Kerberoasting) appear valid to attacker; maintain monitoring if compromised credential used to attack real systems; implement credential honeypots with network isolation

- Honeypot deployment in DMZ attracts external scanners, not internal attackers; place internal honeypots on production subnets for insider threat detection; balance detection scope and network visibility

- Firewall rules block honeypot traffic before reaching SIEM; verify firewall allows honeypot logging and alerts to SOC; implement firewall logging of honeypot access for full audit trail

- High-fidelity honeypots (full interactive shell) create containment risk if compromised; limit honeypot shell access to read-only directories; monitor for reverse shell attempts; implement resource limits

- Honeypot maintenance burden: OS patching, service updates, credential refreshes become overhead; evaluate cost-benefit vs. detection value; consider lightweight honeypots for high-volume deployments
