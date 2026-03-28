---
description: "Cloud Sandbox / ATP: file type policies, patience page, quarantine workflow, known-bad/known-good lists"
---

# ZIA Cloud Sandbox & Advanced Threat Protection (ATP)

You are the last fortress against zero-day malware. Zscaler Cloud Sandbox detonates suspicious files in a virtual environment before they reach the user. Get it right, and you catch file-based exploits. Get it wrong, and you're cleaning up ransomware.

## When to use

**DO** use ZIA Cloud Sandbox when:
- You need zero-day malware detection (signature-less threats)
- You want to verify files before users download them
- You're protecting against file-based ransomware
- You have regulatory requirements for advanced threat detection

**DON'T** use when:
- You only care about known malware (signatures are enough)
- Your network is disconnected from cloud (no cloud sandbox possible)

## What Cloud Sandbox Does

```
File Downloaded from Internet
        ↓
    Is it suspicious? (size, type, hash, etc.)
        ↓
    [YES] Send to Zscaler Cloud Sandbox
        ↓
    Detonate file in isolated VM:
      - Execute code
      - Monitor behavior (registry changes, network calls, file access)
      - Compare against 10,000+ known malware behaviors
        ↓
    Verdict:
      ✓ Clean: Allow download (cache for 24 hours)
      ✗ Malicious: Block + quarantine
      ? Unknown: Show "patience page" (user waits)
        ↓
    User receives file (or blocking message)
```

## File Type Policies (What to Sandbox?)

```
Critical file types (ALWAYS sandbox):
  ✓ .exe, .dll, .msi (Windows executables)
  ✓ .dmg, .app (Mac executables)
  ✓ .apk, .ipa (Mobile apps)
  ✓ .jar, .class (Java bytecode)
  ✓ .zip, .rar, .7z (Compressed archives – may hide executables)
  ✓ .script, .bat, .ps1 (Windows scripts)
  ✓ .doc, .docx, .xls, .xlsx (Office macros)
  ✓ .pdf (Embedded JavaScript, exploits)

Medium-risk (optional sandbox):
  ~ .iso (disk images – may contain executables)
  ~ .tar, .gz (Linux archives)
  ~ .jar (Java archive – may contain malicious bytecode)

Low-risk (don't sandbox):
  ✗ .jpg, .png, .gif (images – rare exploits)
  ✗ .mp4, .mov, .mp3 (media – low exploit rate)
  ✗ .txt, .csv (text – no code execution)

Configuration:
  Admin Portal → Advanced Threat Protection → File Type
    ├─ Windows executables: Sandbox
    ├─ Office macros: Sandbox
    ├─ Archives: Sandbox
    └─ Images/Media: Skip sandbox
```

## The Patience Page (User Experience)

```
File detected as suspicious → Sandbox detonation takes 30–120 seconds
During wait, user sees:

┌──────────────────────────────────────────────────────┐
│ ⏳ Scanning for malware... (45 seconds remaining)   │
├──────────────────────────────────────────────────────┤
│                                                       │
│ File: document.pdf                                    │
│ Status: Advanced threat scan in progress              │
│                                                       │
│ This may take 1–2 minutes.                            │
│                                                       │
│ [View file info] [Learn more]                         │
│                                                       │
│ Tip: Check back in a few minutes if still waiting.    │
│       If urgent, contact security@contoso.com         │
│                                                       │
└──────────────────────────────────────────────────────┘

Outcome (after scan):
  ✓ Clean: "Scan complete. Download starting..."
  ✗ Malicious: "File blocked by security policy. Reason: Trojan.Emotet"
  ? Unknown: "Scan inconclusive. Contact security if needed."
```

## Quarantine Workflow

```
Malicious file detected:
  1. File blocked from download
  2. File moved to quarantine storage (Zscaler vault)
  3. Incident logged with:
     - File name, hash, user, destination
     - Threat name + severity (Trojan, Ransomware, etc.)
     - Detonation logs (what the malware did in sandbox)

Security team reviews:
  Admin Portal → Incidents → Malware
    └─ Threat Name: Trojan.Emotet
       User: john.smith@contoso.com
       Time: 2024-03-15 10:45 AM
       Source: box.com
       Threat Analysis: "Attempted registry modification → process injection → C&C callback"

Triage options:
  [ ] True positive (real threat):
      → Log incident, notify user, open ticket with incident response

  [ ] False positive (legitimate file):
      → Submit to Zscaler threat research
      → Whitelist user/domain
      → User re-downloads file

  [ ] Suspicious but not malware:
      → Monitor file reputation for 7 days
      → If no updates, whitelist
```

## Known-Good vs. Known-Bad Lists

### Known-Good List (Whitelist)

```
Admin Portal → Advanced Threat Protection → Safe List

Purpose: Skip sandbox for trusted files/domains

When to use:
  ✓ Internal tools (your custom executable, build tools)
  ✓ Partner file downloads (from trusted partners only)
  ✓ False positives (file blocked, but you reviewed it)

Configuration:
  Format: File hash (SHA-256) or domain

Example:
  Hash: a4f5e0d9c8b2a1f3d7e8c9b0a1f2d3e4
         ^ Your internal installer (reviewed by security team)

  Domain: s3-downloads.acme.internal
         ^ Internal artifact server (no internet access)

Warning: Known-good lists = trust. Use sparingly. Every whitelist is a risk.
```

### Known-Bad List (Blacklist)

```
Admin Portal → Advanced Threat Protection → Bad File List

Purpose: Automatically block known-malicious files

When to use:
  ✗ Files matching known malware hashes
  ✗ Command-and-control (C&C) domains
  ✗ Exploit kit landing pages

Configuration:
  Zscaler maintains 100M+ known-bad hashes
  You can add custom hashes (files you analyzed + confirmed malicious)

Example:
  Hash: b5a6f1e0d9c8b2a1f3d7e8c9b0a1f2d3e5
         ^ Ransomware binary (Conti variant, dated 2024-02-15)

  Domain: malware.c2.xyz
         ^ Known C&C server (blocked globally)

Gotcha: Known-bad lists are reactive. Zero-days don't have hashes.
        That's why sandbox is important (detects unknown variants).
```

## Advanced Threat Protection (ATP) Configuration

```yaml
---
Advanced Threat Protection Settings

File Sandbox:
  Enabled: Yes
  Timeout: 120 seconds (wait max 2 minutes)
  Detonation: All suspicious files
  Reporting: Real-time to security team

File Type Sandbox List:
  .exe, .dll, .msi:     Sandbox (Windows executables)
  .zip, .rar, .7z:      Sandbox (may contain executables)
  .docx, .xlsx:         Sandbox (may contain macros)
  .pdf:                 Sandbox (may contain exploits)
  .jpg, .mp4, .txt:     Skip (low risk)

Known-Bad (Auto-Block):
  Enabled: Yes
  Source: Zscaler threat intelligence (updated hourly)
  Custom: [Your internal known-malicious hashes]

Known-Good (Whitelist):
  [Internal tools + trusted partner domains]
  Reviewed by: Security team
  Approval: Required (formal change request)

Behavioral Analysis:
  Enabled: Yes
  Detect: Ransomware signatures (file encryption, registry changes)
  Detect: Trojan behavior (process injection, C&C callback)
  Detect: Worm behavior (self-propagation, lateral movement)

Alerts:
  Severity: High/Critical
  Notification: Immediate to security team + SIEM
  Logging: Full detonation logs (for forensics)
```

## Troubleshooting Sandbox Delays

```
Legitimate file download is slow (waiting on sandbox verdict)

Cause 1: File size too large for quick detonation
  Solution: Exclude large media files from sandbox
             (unlikely to contain malware)

Cause 2: File has no reputation (new file, zero-day scanner)
  Solution: Increase timeout from 120s to 180s
             OR whitelist domain (if trusted source)

Cause 3: Sandbox overloaded (millions of files detonating)
  Solution: Implement local verdict caching
             (cache "clean" verdict for 24 hours)

Configuration:
  Admin Portal → Advanced Threat Protection
    └─ File Sandbox
       ├─ Timeout: 180 seconds (more time = less false blocks)
       ├─ Local Caching: Enabled (cache clean verdicts)
       └─ Size limit: Skip sandbox for files >500 MB
```

## Configuration Checklist

```
Before go-live:

[ ] Enable Cloud Sandbox for .exe, .dll, .msi, .zip
[ ] Enable for Office files (.docx, .xlsx) if macro risk high
[ ] Set sandbox timeout to 120–180 seconds
[ ] Configure patience page (user-friendly messaging)
[ ] Create known-good list for internal tools (reviewed by infosec)
[ ] Review Zscaler's known-bad list (enabled by default)
[ ] Set up alerts (malware detections → security team email)
[ ] Test with sample malware (EICAR test file)
    └─ Download eicar.com (test malware detection)
    └─ Verify: File blocked, incident logged, alert sent
[ ] Educate users: "Your download is being scanned. This may take 1–2 min."
[ ] Create escalation path: User finds legitimate file blocked
    └─ Process: Submit to security team, review, whitelist if safe
[ ] Monitor sandbox false positives (target: <1% per week)
[ ] Schedule quarterly threat intelligence review (update known-bad list)
```

## Gotchas

1. **Sandbox timeout too short:** Set to 30 seconds = half your files time out and get blocked. Users bypass via home internet. Set to 120+ seconds.
2. **Overly aggressive whitelisting:** Every file blocked = "just whitelist it". 6 months later, you've whitelisted 500 files. Require formal approval + security review.
3. **No patience page:** Users see blank screen for 2 minutes, assume internet is broken. Add a visible "Scanning..." message.
4. **Office macro sandboxing disabled:** Emotet, Trickbot, etc. delivered via .xlsx attachments. Enable Office file sandboxing.
5. **No forensic logging:** Malware blocks but you don't know what it tried to do. Enable detailed detonation logging (file system, registry, network activity).

---

**Pro tip:** Cloud Sandbox catches what signatures miss. Set it loose on executables, Office files, and archives. Configure a reasonable timeout (120–180 sec), add a patient UI message, and let ML do the work. You'll catch zero-days before antivirus sees them.
