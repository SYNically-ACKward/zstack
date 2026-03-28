---
description: "Inline DLP for web: EDM/IDM dictionaries, detection rules, incident workflow (log/caution/block), notification templates"
---

# ZIA DLP Inline

You are the last line of defense against data exfiltration. DLP watches the wire for credit card numbers, social security numbers, source code, and trade secrets. Get it right, and you prevent the 6-figure breach. Get it wrong, and you block legitimate work.

## When to use

**DO** use ZIA DLP Inline when:
- You need to prevent sensitive data from leaving the organization
- You're required by compliance (HIPAA, PCI, SOC 2)
- You want to log exfiltration attempts for forensics

**DON'T** use when:
- You don't have a backup classification system (DLP alone isn't enough)
- You're building detection rules without baseline testing

## DLP Detection Methods (Pick One or Combine)

### Method 1: Pattern-Based Detection

```
What it catches: Credit cards, SSNs, phone numbers
How: Regex patterns (no dictionary needed)

Example rule:
  Rule Name: "Block Credit Card Exfiltration"
  Pattern: \d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}
           (matches: 1234-5678-9012-3456)
  Confidence: 100% (high false positive risk)
  Action: Block

Gotcha: Regex patterns = high false positive rate
        (123-45-6789 could be a supplier ID, not SSN)
```

### Method 2: EDM (Exact Data Matching)

```
What it catches: Specific data you upload (customer lists, employee IDs, trade secrets)
How: Upload a .csv file of sensitive values; Zscaler hashes them

Example:
  1. Create EDM dictionary: employee_ids.csv
     Contents: 12345, 12346, 12347, ... (10K IDs)
  2. Upload to Admin Portal → DLP Dictionary Management
  3. Create rule: "Block export of employee IDs"
     Match: EDM dictionary "employee_ids"
     Action: Block

Pros:
  ✓ Zero false positives (matches exact values)
  ✓ Detects intentional data theft
Cons:
  ✗ Requires manual data uploads
  ✗ Won't catch partial/masked data
```

### Method 3: IDM (Indexed Data Matching)

```
What it catches: Variations of sensitive data (masked, obfuscated, partial)
How: Upload data; Zscaler creates a fingerprint index

Example:
  - Your customer list: "ACME Corp, Contoso LLC, Fabrikam Inc"
  - Attacker sends: "ACME, Contoso" (partial)
  - IDM catches it via fingerprint match

Pros:
  ✓ Catches masked/partial versions
  ✓ Good for trade secrets, source code
Cons:
  ✗ More CPU overhead
  ✗ Harder to tune (false positives)
```

## DLP Rule Workflow (Log → Caution → Block)

```
┌─────────────────────────────────────────────────────────┐
│ Incident Flow: What happens when DLP detects a match?   │
└─────────────────────────────────────────────────────────┘

Stage 1: LOG (Weeks 1–2 of detection)
  ✓ Traffic is allowed
  ✓ Incident is logged to Audit & Incident Log
  ✓ Use: Establish baseline (how often does this rule fire?)
  ✓ Goal: Collect 1–2 weeks of data to tune

Stage 2: CAUTION (Weeks 2–4 of detection)
  ✓ Traffic is allowed BUT user sees warning
  ✓ Warning: "Your data was flagged as sensitive. Continuing = logged to security."
  ✓ Incident is logged AND user notified
  ✓ Goal: Educate users before you block

Stage 3: BLOCK (Week 4+ of detection)
  ✗ Traffic is blocked
  ✗ User sees error: "This action is blocked by security policy."
  ✗ Incident is logged AND user notified AND escalated to security team
  ✓ Goal: Prevent exfiltration
```

## DLP Rule Configuration Template

```yaml
---
Rule Name: "Block Trade Secrets via Email"

Conditions:
  Destination: *.gmail.com, *.yahoo.com, *.hotmail.com
  (allow internal email: contoso.com, microsoft.com)

Detection Method: EDM + Pattern
  EDM Dictionary: "trade_secrets"
  Alternate Pattern: \bconfidential\b.*\b(API|source code|formula)\b

Protocol: HTTP, HTTPS, Email (SMTP/POP)

File Types: .docx, .pdf, .xlsx, .pptx, .java, .py, .js
  (exclude: .txt, .jpg, images)

Notification:
  User Alert: "Caution: You are sending files containing sensitive data."
  Security Team Alert: "Trade secret exfiltration attempt"
  Email to: security@contoso.com

Actions:
  Week 1–2: LOG only
  Week 3–4: CAUTION (warn user)
  Week 5+: BLOCK (prevent send)
```

## User Notification Template

**When DLP fires, send this message:**

```
┌──────────────────────────────────────────────────────────┐
│ ⚠️  Sensitive Data Detection                              │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ Your action was flagged because it may contain            │
│ sensitive data (credit cards, trade secrets, passwords).  │
│                                                           │
│ Action: [Blocked] [Warned] [Logged]                       │
│ Match Type: [Credit Card] [Trade Secret] [Custom]         │
│ Destination: [Gmail] [Box] [Slack]                        │
│                                                           │
│ Need to send this? Contact: security@contoso.com          │
│ Reference: Incident #12345                               │
│                                                           │
│ [Click here for DLP Policy FAQ]                           │
└──────────────────────────────────────────────────────────┘
```

## Incident Workflow (Post-Detection)

```
1. DLP rule fires → Incident logged in Zscaler Admin Portal
   Location: Incidents & Insights → DLP Incidents

2. Security team reviews incident:
   - Who (user email)
   - What (data match)
   - When (timestamp)
   - Where (destination)
   - Action taken (blocked, warned, logged)

3. Triage:
   [ ] False positive → adjust rule, whitelist user
   [ ] Legitimate (user sending customer data to box.com) → approve, log
   [ ] Suspicious → escalate to incident response

4. User follow-up (if blocked):
   Security: "Hi, your email to gmail.com contained credit card data.
            If legitimate, reply to unblock. Otherwise, delete."

5. Resolution:
   - Approved: whitelist the destination
   - Denied: log incident, educate user
   - Suspicious: open ticket with incident response team
```

## Common EDM Dictionaries to Build

| Dictionary | Example Values | Use Case |
|------------|----------------|----------|
| **Employee IDs** | E12345, E12346, E12347 | Identify internal directory leaks |
| **Customer List** | Acme Corp, Contoso LLC, Fabrikam | Prevent customer database theft |
| **Trade Secrets** | API keys, SDK docs, firmware | Protect IP |
| **Credit Cards** | (regex pattern, not EDM) | PCI compliance |
| **Health Records** | Patient MRNs, medical record #s | HIPAA compliance |
| **Passwords** | (regex: 8+ chars with special) | Prevent cred leaks |

## Configuration Checklist

```
Before go-live:

[ ] Identify sensitive data types (credit cards, SSNs, trade secrets, customer list)
[ ] Choose detection method (pattern vs. EDM vs. IDM)
[ ] Create EDM dictionaries (upload .csv files)
[ ] Build 3–5 rules covering the top 80% of risk
[ ] Set initial action to LOG (not BLOCK)
[ ] Configure notifications (user alert, security email)
[ ] Test with non-sensitive data first
[ ] Run rule for 2 weeks in LOG mode; measure false positive rate
[ ] If >5% false positives, adjust rule threshold or add whitelist
[ ] Escalate to CAUTION after 2 weeks
[ ] Escalate to BLOCK after 4 weeks (if team is comfortable)
[ ] Document exceptions (approved destinations for specific users)
```

## Gotchas

1. **100% DLP action = disaster:** Never go to BLOCK on Day 1. You'll break legitimate workflows. LOG → CAUTION → BLOCK over 4 weeks.
2. **No EDM baseline:** If you don't know "how often is X sent?", you can't tune detection. Spend Week 1 collecting data.
3. **Regex false positives:** Pattern "\\d{4}" matches order numbers, phone extensions, etc. High false positive rate = DLP tuned off. Use EDM instead.
4. **No notification template:** User sees "blocked" with no context. She thinks it's a bug. Include a DLP explanation + escalation path.
5. **Ignore EDM freshness:** Your customer list is 6 months old. New customers won't be caught. Update EDM quarterly.

---

**Pro tip:** DLP is about graduated enforcement. Start with LOG, move to CAUTION when you're confident, then BLOCK. Users will adapt if you give them 2–4 weeks of warnings.
