---
description: "Deploy ZTB: ZTP enrollment, factory reset, cabling, SVI migration, traffic cutover sequence"
---

# ZTB Deployment

**Persona:** Network operations engineer deploying ZTB appliances to production branch sites.

## When to use
- Fresh ZTB site deployment (greenfield or refresh)
- ZTP (Zero Touch Provisioning) enrollment workflows
- Factory reset before second-site deployment (config reuse)
- SVI migration from legacy firewall to ZTB
- Live traffic cutover planning and execution

## 5-Gate Artifacts
1. **ZTP Pre-staging Checklist**: Serial numbers, certificates, enrollment codes generated and validated
2. **Cabling Plan**: Diagram with port assignments, cable lengths, switch port speed/duplex settings
3. **SVI Migration Map**: Old FW interfaces → ZTB VLAN SVIs, IP reuse vs new addressing scheme
4. **Cutover Runbook**: Hour-by-hour sequence, rollback steps, validation checkpoints
5. **Post-cutover Validation**: Ping tests, app access verification, tunnel health checks, QoS confirmation

## Key Configuration
- **ZTP Enrollment**: Device phones home to Zscaler bootstrap service; auto-downloads config + CA certs
- **Factory Reset**: Hold reset button 15-30 sec; clears all config but preserves hardware settings
- **Cabling Order**: In-band management → ZCC/ZPA, WAN primary/DIA/backup → internet, LAN → branch switch, HA sync → peer ZT
- **SVI Migration**: Export old FW IP/vlan mappings; recreate as ZTB SVIs; test routing before cutover
- **BGP/OSPF Startup**: Enable after cabling validation; monitor route convergence (30-60 sec typical)
- **DHCP Relay**: Configure if using server pools; validate DHCP discover reaches upstream DHCP
- **NTP Sync**: Critical for tunnel establishment and certificate validation; use NTP pool or local time source
- **Cutover Window**: Schedule during maintenance window; 2-3 hours for large branch (100+ VLANs)

## Gotchas
- **ZTP Timeout**: If enrollment fails, device falls back to default config; check DNS resolution for bootstrap server
- **Cable Swap Order**: Switching cables without failover setup causes full site outage; always have HA secondary ready first
- **MTU Mismatch**: If ZTB set to 1500 and upstream is 1480, tunnel fragmentation causes throughput degradation; validate end-to-end
- **SVI IP Reuse**: If old FW still active during cutover, duplicate IP causes ARP storms; use temporary IPs or strict failover
- **BGP Convergence Delay**: New routes not immediately used; may need to flap BGP or clear route cache manually
- **VLAN Lag**: If trunking misconfigured, some VLANs don't appear on ZTB; verify all VLANs in "show vlan" output
- **Licensing**: ZTP assigns default throughput tier; manual license upgrade needed for higher speeds
- **Rollback Pain**: If cutover fails mid-way, routing asymmetry can cause packet loss; plan hard rollback to old FW, not soft revert

## Configuration Checklist
- [ ] ZTP certificates generated and verified in Zscaler portal
- [ ] Serial numbers registered with enrollment codes ready
- [ ] Cabling diagram signed off by network team
- [ ] SVI IP mappings validated against old firewall config
- [ ] BGP/OSPF ASN and neighbor IPs documented
- [ ] NTP sources tested from ZTB out-of-band management
- [ ] HA secondary deployed first, HA link tested
- [ ] Cutover window approved by change control and stakeholders
- [ ] Rollback plan documented with contact escalation tree
- [ ] Post-cutover monitoring dashboard (tunnel health, throughput) set up
