---
description: "China Premium: zscalerone.net cloud, ICP filing, GFW considerations, ZCC pre-staging, peering setup"
---

# China Premium

**Persona:** Network engineer deploying Zscaler for China operations with regulatory compliance.

## When to use
- Deploying ZIA/ZPA for users inside mainland China with low latency requirements
- ICP filing process and documentation for regulatory compliance
- GFW (Great Firewall) blocking mitigation and peering setup
- ZCC pre-staging before ZCC access is needed in China
- China-specific monitoring and incident response workflows

## 5-Gate Artifacts
1. **ICP Filing Checklist**: Company documentation, server location, hosting agreement, filing timeline (3-4 weeks typical)
2. **Zscaler China Cloud Architecture**: zscalerone.net region, peering partners, latency targets, failover strategy
3. **GFW Bypass Plan**: Zscaler.com domain blocked; pre-staging strategy, endpoint certificate pinning, DNS over HTTPS
4. **ZCC Pre-staging Guide**: Download ZCC installer outside China, stage to USB/OTP, installation procedure inside China without internet
5. **China Operations Dashboard**: Region-specific SLA targets, incident escalation, contact information for local Zscaler support

## Key Configuration
- **Zscaler China Cloud**: zscalerone.net (Zscaler-operated, hosted in China-compliant datacenter), separate from global zscaler.com cloud
- **ICP License**: Required for any web service accessible in China; must be filed by China entity (local subsidiary or partner)
- **ICP Filing Process**: 1) Gather documents (business license, site info, domain registration), 2) Submit to hosting provider, 3) ICP authority reviews (3-4 weeks), 4) License issued
- **GFW Filtering**: Zscaler.com domain (global cloud) is actively blocked; zscalerone.net (China cloud) is allowed
- **ZCC Download**: Desktop ZCC for Windows/Mac must be downloaded outside China; cannot download from zscaler.com once in China
- **ZCC Pre-staging**: Download ZCC .msi/.dmg before China deployment; stage on USB drive or internal server; users install locally without internet
- **Endpoint Certificates**: Install Zscaler China cloud root CA on users' devices before first ZCC connection; prevents cert verification failures
- **Peering Arrangement**: Zscaler peers with China Unicom, China Mobile, China Telecom for optimal routing; verify ASN and peering IP configuration
- **Local Support**: Zscaler provides local operations team in China; engage for ICP filing assistance and incident coordination
- **DNS Configuration**: Configure DNS to resolve zscalerone.net to local IP (not global DNS); prevents DNS interception by GFW
- **Connectivity Test**: Ping zscalerone.net from China network to validate peering and latency; expect < 100ms from major cities

## Gotchas
- **ICP Filing Delay**: If company new to China market, filing may take 6+ weeks; plan deployment 2 months in advance
- **Zscaler.com Blocked Completely**: Even if user VPN exists, zscaler.com is blocked; must use zscalerone.net exclusively
- **ZCC Download Blocker**: If user in China without pre-staged ZCC, can't download it; provide installation media in advance or pre-install with MDM
- **Certificate Pinning Required**: Zscaler.com redirects to zscalerone.net; if old ZCC has pinned cert for zscaler.com, connection fails; update ZCC before deployment
- **GFW IP Blocking**: If Zscaler China cloud IPs identified by GFW, they may be sporadic blocked; Zscaler adjusts IPs as needed, may affect service briefly
- **China Mobile Latency**: Users on China Mobile ISP may experience higher latency to Zscaler China cloud; routing optimization requires peering upgrade
- **Local Data Residency**: ICP license and China cloud operation may be subject to local data residency law; verify config data stored in China
- **Support Time Zone**: Zscaler China support operates in Chinese business hours (9-5 CST); off-hours incidents may have slower response
- **Regulatory Changes**: China regulations evolve rapidly; ICP filing may require updates; stay informed of changes via local legal team
- **User Roaming**: Users traveling outside China may revert to global cloud (zscaler.com); if device offline, local cache used, then cloud sync fails

## Configuration Checklist
- [ ] ICP filing documentation prepared and submitted to Zscaler partner or hosting provider
- [ ] Zscaler China cloud tenancy created and verified accessible from China
- [ ] ICP license number documented and included in policy documents
- [ ] ZCC installer downloaded outside China and staged for distribution
- [ ] Zscaler China root CA certificate exported and pre-loaded on user devices
- [ ] Peering configuration verified with ISP (BGP ASN, peering IP, local routes)
- [ ] DNS configuration tested (zscalerone.net resolves to local China IP)
- [ ] Latency baseline established from major China cities (Beijing, Shanghai, Shenzhen, Chengdu)
- [ ] Local Zscaler support team contact information shared with operations team
- [ ] User communication explaining ZCC pre-staging and deployment procedure in China
- [ ] Monitoring dashboard configured for China-specific SLA and incident escalation
