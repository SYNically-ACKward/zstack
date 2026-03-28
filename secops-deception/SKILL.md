---
description: "Integrate deception detection with SIEM and SOC workflows to detect and respond to honeypot triggers"
---

**Deception Engineer** | Zscaler Zero Trust Exchange | Threat Detection Lead

Route deception alerts (honeypot activity, canary token activation) to SIEM and SOC, correlate with attack TTPs, and execute automated response playbooks.

## When to use

- Detecting suspicious user activity through honeypot triggers (unauthorized file access, credential use, decoy app interaction)
- Correlating decoy triggers with other security events to confirm breach hypothesis and assess incident scope
- Mapping attacker behavior (credential theft → lateral movement → exfiltration) from decoy triggers and TTPs
- Generating threat intelligence from decoy interactions (malware behavior analysis, attacker tooling, campaigns)
- Automating incident response to decoy triggers (block user, revoke credentials, forensic collection, threat hunting)
- Detecting insider threats through decoy access patterns and behavioral deviations
- Validating detection capability gaps through controlled deception testing (red team exercises)

## 5-Gate Artifacts

1. **Alert Routing Architecture** - Decoy triggers → SIEM (Splunk, ELK) via syslog/API with enrichment, correlation with ZPA/ZSB/ZCC events, severity escalation (confirmed breach = critical), playbook routing to SOAR (automated/manual approval)

2. **Honeypot TTP Mapping** - Decoy file access → data exfiltration attempt, credential file usage → privilege escalation, RDP connection → lateral movement, AD SPN interaction → Kerberoasting, unusual protocol on honeypot port → recon

3. **Automated Response Playbook** - Decoy trigger detected → verify timing/context (was user on-hours? expected location?), block user session (but preserve evidence), revoke credentials, enable forensics (full pcap, memory dump), escalate to incident team, notify user with investigation updates

4. **Correlation Rule Library** - Same user accesses decoy + legitimate sensitive data within 30min = exfiltration confidence, same IP accesses multiple decoys = reconnaissance pattern, decoy access + C&C comms = confirmed breach, decoy trigger from executive = high-priority investigation

5. **Deception Metrics & Reporting** - Detection rate (decoys triggered per month, normalized by user population), time to detection (alert latency percentile), false positive rate (non-malicious access %), TTP coverage by attack stage (reconnaissance, exploitation, exfiltration), cost-per-detection analysis

## Key Configuration

- **Alert Tuning**: High-confidence decoy triggers (credential file opened, honeypot account login attempt, canary token callback) → immediate alert; medium-confidence (honeypot folder browsed, decoy IP pinged) → batch daily; low-confidence (network scan hitting decoy) → weekly digest

- **Correlation Rules**: Link decoy triggers with Zscaler threat intelligence blocks (same user), DLP violations (exfiltration after decoy access), behavioral anomalies (impossible travel to decoy location) from same user within 2-hour window; implement deception confidence scoring

- **SIEM Integration**: Export decoy alerts in CEF format with context (decoy type, lure content, trigger timestamp, actor details, confidence score); preserve full interaction logs for forensics

- **Response Automation**: Pre-stage containment actions (user to block, credentials to revoke) but require SOC approval before execution to avoid false positive impact from legitimate user confusion; implement fast-track approval for high-confidence triggers (<5 min)

- **Feedback Loop**: Deception team reviews non-incident decoy triggers monthly; updates decoy placement/content based on attacker avoidance patterns; measure decoy effectiveness by interaction rate and false positive ratio

- **Red Team Integration**: Conduct quarterly red team exercises to validate deception effectiveness; measure detection rate and time-to-detection against simulated attack scenarios

## Gotchas

- High false positive rate from decoy triggers (user curiosity, accidental access, legitimate business processes); require human validation before response action
- Delayed alert delivery from decoy to SOC (network lag, log aggregation) can miss incident response window; prioritize real-time alerting for high-risk decoys
- Attacker awareness of decoys (common lures like "passwords.txt", honeypot account names) reduces effectiveness; rotate decoy content quarterly
- Over-reliance on decoys creates security theater; ensure foundational detection (EDR, network monitoring) exists before decoys
- Decoy trigger information may be sensitive (exposes internal naming conventions, systems in use); restrict decoy alert details to authorized personnel only
- Playbook escalation to incident team without clear evidence (decoy trigger alone) can create false incident reports; require correlation with other detection sources
