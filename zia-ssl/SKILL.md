---
description: "SSL/TLS inspection: Zscaler CA vs custom sub-CA vs BYOK, bypass list by category, cert deployment via GPO/MDM/ZCC, compliance considerations (HIPAA, PCI)"
---

# ZIA SSL Inspection

You are intercepting encrypted traffic to see malware, DLP violations, and data exfiltration. SSL inspection is the most contentious policy—get it wrong, and you break banking, healthcare, and user trust.

## When to use

**DO** use SSL Inspection when:
- You need to inspect HTTPS traffic for threats and DLP
- You're balancing security against privacy & compliance
- You're deploying to healthcare, finance, or regulated industries

**DON'T** use when:
- The customer explicitly forbids MITM (e.g., "GDPR privacy mandate")
- You don't have a bypass list (inspecting everything = too much noise)

## Three CA Models (Pick One)

### Model 1: Zscaler CA (Default)

```
How it works:
  User → Zscaler intermediate CA → Target server
  Zscaler inspects the decrypted session, then re-encrypts
  Certificate chain: User sees Zscaler CA in cert store

Pros:
  ✓ No customer cert deployment burden
  ✓ Zscaler manages certificate lifecycle
  ✓ Mobile & desktop transparent

Cons:
  ✗ Certificate pinning breaks (apps like Slack, Teams may fail)
  ✗ Compliance concern: customer doesn't control the CA

Deployment:
  - Admin portal → SSL Inspection
  - Enable "Zscaler Intermediate CA"
  - Certificate auto-deployed to ZCC, MDM, GPO
```

### Model 2: Custom Sub-CA (Customer-Issued)

```
How it works:
  Customer generates a sub-CA under their root CA
  Customer pushes certificate to Zscaler Admin Portal
  Zscaler uses this CA for inspection
  User sees customer's CA (not Zscaler)

Pros:
  ✓ Customer controls the CA
  ✓ Compliance: "We own the certificate"
  ✓ Better for HIPAA, PCI audit trails
  ✓ Fewer certificate pinning issues

Cons:
  ✗ Customer must generate & manage CSR/key
  ✗ Deployment complexity (MDM push required)
  ✗ Renewal burden (customer is responsible)

Deployment:
  - Customer generates CSR: openssl req -new -key customer.key -out customer.csr
  - Customer's PKI signs it (sub-CA, not root)
  - Upload cert + key to Admin Portal → SSL Inspection
  - Deploy to all devices via GPO/MDM
```

### Model 3: Bring Your Own Key (BYOK)

```
How it works:
  Customer generates root CA key and stores it in HSM
  Zscaler never sees the key, only the cert
  Zscaler uses the cert for inspection
  On-demand re-issuance for specific sites

Pros:
  ✓ Highest compliance posture
  ✓ FIPS 140-2 compliant (key in HSM)
  ✓ Excellent for DoD, finance, healthcare

Cons:
  ✗ Complex setup (requires customer PKI expertise)
  ✗ Expensive (HSM cost)
  ✗ Longer deployment timeline
  ✗ Not all apps support BYOK

Deployment:
  - Contact Zscaler professional services
  - Estimated timeline: 8–12 weeks
```

## SSL Bypass List (Critical!)

**You MUST bypass:**

```
Financial institutions:
  - *.bankofamerica.com
  - *.wellsfargo.com
  - *.chase.com
  - *.fidelity.com
  Reason: Certificate pinning breaks login

Healthcare:
  - *.mychart.org (patient portal)
  - *.epic.com (EHR)
  Reason: PHI sensitivity; compliance requirement

APIs & Webhooks:
  - api.github.com
  - api.stripe.com
  - webhook.slack.com
  Reason: Certificate pinning breaks integrations

Security tools:
  - *.zscaler.com (prevents infinite loops)
  - *.okta.com (may break OAuth)

SaaS certificate pinners:
  - *.slack.com (uses pinning)
  - *.teams.microsoft.com (uses pinning)
```

**Bypass by category (Zscaler recommendation):**

```
Admin Portal → SSL Inspection → Bypass List

✓ Enable: "Bypass SSL inspection for financial sites"
✓ Enable: "Bypass SSL inspection for healthcare"
✓ Enable: "Bypass SSL inspection for P2P/torrents" (redundant but safe)
✓ Disable: "Bypass SSL inspection for streaming" (you want to throttle video)

Result: You inspect most traffic but avoid breaking critical apps.
```

## Certificate Deployment Methods

### GPO (Windows)

```
Group Policy → Computer Configuration → Certificates
  └─ Certificates (Local Computer) → Trusted Root CA

Steps:
1. Export Zscaler / customer CA cert (.cer format)
2. Create Group Policy object (GPO)
3. Assign certificate to "Trusted Root CA" store
4. Link GPO to user/computer OUs
5. Test: Verify cert in certmgr.msc on test machine
```

### MDM (Mobile)

```
Intune / MobileIron / Jamf:
  1. Upload SSL certificate to MDM console
  2. Create certificate profile (TrustedRootCA)
  3. Assign to device groups
  4. Test: iOS → Settings → General → VPN & Device Management
```

### ZCC (Zscaler Client Connector)

```
Zscaler Client Connector (ZCC):
  - ZCC auto-downloads cert during enrollment
  - No manual deployment needed
  - Transparent to user

Configuration:
  Admin Portal → Connector Settings
    └─ Client Connector → Certificates
       └─ Auto-push: Enabled
```

## Compliance Considerations

| Standard | SSL Inspection Allowed? | Notes |
|----------|------------------------|----|
| **HIPAA** | Yes, with conditions | Must use customer CA (Model 2/3); audit log all access |
| **PCI-DSS** | Yes, with conditions | Must not inspect payment card data in transit; whitelist payment processors |
| **SOC 2 Type II** | Yes | Audit trail required; log all inspection events |
| **GDPR** | Debated | Some interpret HTTPS interception as surveillance; document consent; use Model 2 (customer CA) |
| **NIST 800-53** | Yes | SI-7 (Zscaler is appliance); audit required |
| **DoD DFARS** | No BYOK required | Only Model 3 (BYOK) acceptable for DoD workloads |

## Configuration Checklist

```
Before go-live:

[ ] Choose CA model (Zscaler vs. custom vs. BYOK)
[ ] Generate / upload certificate to admin portal
[ ] Create bypass list (financial, healthcare, APIs)
[ ] Test on 10 users before org-wide rollout
[ ] Verify certificate deployment via GPO/MDM/ZCC
[ ] Document which apps/domains are bypassed (for compliance)
[ ] Configure audit logging (Admin Portal → Audit Logs)
[ ] Brief CISO on privacy implications
[ ] Train help desk: "SSL cert errors = check bypass list"
```

## Gotchas

1. **Cert pinning surprise:** Day 1 go-live, Teams breaks. Reason: You didn't bypass Microsoft's pinned certs. Always test with the top 20 apps first.
2. **No bypass list:** Inspecting everything = noise. You'll see 10,000 false alerts daily. Curate your bypass list.
3. **GDPR misunderstanding:** Some customers think SSL inspection = illegal in EU. It's not illegal, but you must disclose it. Use Model 2 (customer CA) for GDPR comfort.
4. **Compliance checklist missing:** You inspect healthcare data without logging = audit failure. Document everything.
5. **Certificate rotation shock:** If you choose Model 2 (custom CA) but don't plan cert renewal, you get the same gotcha every 3 years.

---

**Pro tip:** On day 1, only inspect 80% of your traffic. Use a bypass list for the risky 20% (banks, healthcare, APIs). Gradually expand as you get comfortable. Overreach on SSL inspection = angry users + circumvention via VPN.
