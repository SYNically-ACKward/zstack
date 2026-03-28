---
description: "Generate a Zscaler Professional Services Statement of Work using the official ZS template format. Use this skill whenever the user asks for a SOW, statement of work, contract, engagement agreement, or scope document. This skill produces a .docx file from the official Zscaler PS SOW template — not a generic SOW. Always use the bundled template."
---

**Zscaler PS SOW Generator** | Official Template | Contract-Ready Output

Generate a Statement of Work that exactly matches the official Zscaler Professional Services format. This skill uses the bundled `templates/sow-template.docx` as the base — you MUST start from this file and fill in the placeholders. Never generate a SOW from scratch.

## When to use

- Customer has signed a purchase order and needs a formal SOW
- SE or PS engineer requests a SOW for a new engagement
- Updating an existing SOW with new scope or change order
- Any request mentioning "SOW", "statement of work", "PS contract", or "engagement agreement"

## How to produce the SOW

### Step 1: Copy the template

```bash
cp <skill-dir>/templates/sow-template.docx ./sow-draft.docx
```

### Step 2: Unpack the docx

Use the docx skill's unpack tool to extract the XML:

```bash
python scripts/office/unpack.py sow-draft.docx unpacked-sow/
```

### Step 3: Fill in the placeholders

Edit `unpacked-sow/word/document.xml` to replace all `{{placeholder}}` tokens with real values. Here is the complete list of placeholders and what they mean:

#### Header placeholders (always required)
| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{account}}` | Customer legal entity name | "Acme Corporation" |
| `{{sowCredits}}` | Number of PS credit units purchased | "150" |

#### Stage 2 activity placeholders (include or remove based on scope)
Each placeholder below is a block of activities for that Zscaler module. If the module is in scope, replace the placeholder with the activity description. If NOT in scope, delete the placeholder line entirely.

| Placeholder | Zscaler Module |
|-------------|---------------|
| `{{networkFirewalls}}` | Network & Firewall configuration |
| `{{authenticationConfiguration}}` | SAML/SCIM/IdP setup |
| `{{zscalerClientConnector}}` | ZCC deployment & packaging |
| `{{urlCloudApp}}` | URL filtering & cloud app control |
| `{{trafficForwarding}}` | GRE/IPSec/PAC forwarding |
| `{{advancedCloudFirewall}}` | Cloud Firewall L4/L7 rules |
| `{{advancedCloudSandboxing}}` | Sandbox / ATP configuration |
| `{{inlineWebDLP}}` | Inline Web DLP policies |
| `{{endpointDLP}}` | Endpoint DLP configuration |
| `{{emailDLP}}` | Email DLP configuration |
| `{{casbOUTofBandSaaS}}` | CASB out-of-band SaaS scanning |
| `{{appTotal}}` | App Total configuration |
| `{{sspm}}` | SaaS Security Posture Management |
| `{{unmanagedDevices}}` | Unmanaged device access |
| `{{advancedClassification}}` | Advanced data classification |
| `{{dpSaaSAPI}}` | Data Protection SaaS API |
| `{{dpAPIRetroScan}}` | DP API Retro Scan |
| `{{tunnel2}}` | Tunnel 2.0 configuration |
| `{{zpaConnectorReview}}` | ZPA Connector review & sizing |
| `{{zpaConfiguration}}` | ZPA app segments & policy |
| `{{branchCloudConnector}}` | Branch Cloud Connector |
| `{{browserIsolation}}` | Cloud Browser Isolation |
| `{{deceptionStandard}}` | Deception Standard deployment |
| `{{deceptionAdvanced}}` | Deception Advanced deployment |
| `{{appProtection}}` | App Protection configuration |
| `{{pra}}` | Privileged Remote Access |
| `{{disasterRecovery}}` | Disaster Recovery / BC setup |
| `{{loggingReporting}}` | NSS / log streaming / SIEM |
| `{{zdxStandard}}` | ZDX Standard probes & alerting |
| `{{zdxAdvanced}}` | ZDX Advanced / CloudPath |
| `{{workloadProtection}}` | Workload Protection |
| `{{tenantDivestiture}}` | Tenant Divestiture |
| `{{tenantMerge}}` | Tenant Merge |
| `{{AirgapDeployment}}` | Airgap Deployment |
| `{{Automation}}` | Automation / API integration |
| `{{business continuity}}` | Business Continuity |
| `{{Business Insights}}` | Business Insights |
| `{{Classification}}` | Data Classification |
| `{{China Geo Fencing}}` | China Geo Fencing |
| `{{China premium}}` | China Premium Access |
| `{{Dedicated Managed IP}}` | Dedicated Managed IP |
| `{{Private Service Edge}}` | Private Service Edge |
| `{{VOIP Network Connector}}` | VoIP Network Connector |

#### Engagement & resource placeholders
| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{exitHours}}` | Total PS hours in contract | "200" |
| `{{exitMonths}}` | Maximum engagement duration in months | "6" |
| `{{sowREHours}}` | Remote Resident Consultant hours | "480" |
| `{{sowREMonths}}` | Remote Resident Consultant months | "3" |

#### Conditional sections
| Placeholder | Description |
|-------------|-------------|
| `{{REexitCritieriaStart}}` ... `{{REexitCritieriaEnd}}` | Wrap the Resident Consultant exit criteria. Remove entire block (including content between) if no Resident Consultant is in scope. |

### Step 4: Write activity descriptions for in-scope modules

For each module that IS in scope, write the activity block in this exact format:

```
**[Module Name]**

- Activity description 1
- Activity description 2
- Activity description 3
```

Use real Zscaler configuration details — not generic filler. Reference actual ZIA/ZPA/ZDX settings, policy types, and integration points.

### Step 5: Fill the Out of Scope section

List the products and features that are NOT included. This is critical for preventing scope creep. Be specific — name exact products and capabilities.

### Step 6: Update the resourcing table

The template has a 3-row table under "Zscaler Engagement & Personnel":
- Row 1: **Project Manager & Consultant** — fill in hours and months
- Row 2: **Remote Resident Consultant** — fill in or remove if not applicable
- Row 3: **Onsite Workshops** — fill in count or remove

### Step 7: Repack and deliver

```bash
python scripts/office/pack.py unpacked-sow/ final-sow.docx --original sow-draft.docx
```

## Mandatory sections (in this exact order)

The ZS SOW template has these sections, each as a Heading 1 with grey background and blue text. Never reorder, rename, or omit any section:

1. **Title block** — "Professional Services / Statement of Work (SOW)" + legal preamble paragraph
2. **Project Overview** — Credits, objectives (3 bullet points are standard)
3. **Assumptions** — 10 standard assumptions (keep all of them, they're field-proven)
4. **Project Scope** — Contains 3 stages + Out of Scope:
   - STAGE 1 - INITIATE & PLAN (Activities + Deliverables)
   - STAGE 2 - CONFIGURE (Module activities from placeholders + Deliverables)
   - STAGE 3 - ROLLOUT (Pilot → Production → PS Transition + Deliverables)
   - Out of Scope
5. **Zscaler Engagement & Personnel** — Resourcing table + working hours + travel terms
6. **Fees** — Standard clause (non-cancellable, non-refundable)
7. **Project & Resource Engagement Model** — Pre-scheduled basis statement
8. **CUSTOMER Responsibilities** — 7 standard bullet points
9. **Exit Criteria** — Hours OR months, whichever comes first
10. **Legal Terms and Conditions** — Link to zscaler.com/resources/legal + warranty clause + data processing clause
11. **Signature block** — Zscaler + Customer (By / Name / Title / Date)
12. **Appendix 1 - Change Order** — Change Description, Justification, Impact + signature block

## What NOT to change

These sections contain legal boilerplate — reproduce them verbatim from the template:

- The opening paragraph ("This Statement of Work...")
- Fees section
- Legal Terms and Conditions (entire section)
- Change Order appendix structure
- Signature blocks
- Working hours clause (EMEA 9-5 GMT, APJ 9-5 IST, AMS 9-5 PT)
- After-hours consumption ratio (1:1.5 weekday, 1:2 weekend)

## What to customize per engagement

- `{{account}}` and `{{sowCredits}}`
- Stage 2 activity modules (include only what's purchased)
- Out of Scope list (inverse of what's in scope)
- Resourcing table hours and months
- Exit Criteria hours and months
- Region-specific working hours (keep all 3 but mark which is primary)

## Formatting rules

- Font: Arial 11pt (inherited from template styles)
- Heading 1: Bold, blue (#236BF5), grey background (#E6E6E6), 12pt
- Bullet lists: Use Word native bullets (not unicode)
- Tables: Light grey borders (#BFBFBF)
- Header: Zscaler logo (top-right, already in template)
- Footer: "© 2025 Zscaler, Inc. All rights reserved. | ZSCALER CONFIDENTIAL INFORMATION" + Zscaler icon + page number

## Gotchas

1. **Never generate from scratch** — always start from `templates/sow-template.docx`. The template contains the correct header/footer with Zscaler logos, styles, and legal boilerplate that are impossible to reproduce correctly from code.
2. **Don't touch the legal sections** — The Fees, Legal Terms, and Change Order appendix are reviewed by Zscaler Legal. Modifying them creates liability.
3. **Remove unused module placeholders** — Leaving `{{zpaConfiguration}}` in the final doc looks unprofessional. Delete any placeholder line where the module is not in scope.
4. **Delete the RE block if no Resident** — If there's no Remote Resident Consultant, remove everything between `{{REexitCritieriaStart}}` and `{{REexitCritieriaEnd}}` inclusive, plus remove Row 2 from the resourcing table.
5. **Keep all 10 Assumptions** — They've been legally vetted and protect both parties. Don't remove any, even if they seem obvious.
6. **Stage 3 PS Transition is mandatory** — Even for small engagements, the handoff meeting and survey are required process.
7. **Out of Scope must be explicit** — Vague out-of-scope like "other features" invites disputes. Name specific products.
8. **Working hours after-hours ratio** — 1:1.5 weekday and 1:2 weekend are contractual obligations, not suggestions.
