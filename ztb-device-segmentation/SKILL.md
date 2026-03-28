---
description: "Segment branch IoT/OT devices: profiling, VLAN isolation, policy-based access, printer/camera/HVAC handling"
---

# ZTB Device Segmentation

**Persona:** Security architect designing IoT/OT device segmentation at branch.

## When to use
- Isolating IoT devices (printers, cameras, smart displays, badges) from corporate network
- OT devices (HVAC, building controls, manufacturing) requiring restricted access
- Device profiling and behavior baseline establishment
- Policy creation for device-to-service communication
- Zero-trust access verification for untrusted device categories

## 5-Gate Artifacts
1. **Device Inventory & Profile Map**: Category (printer, camera, HVAC, badge), MAC OUI, expected destinations
2. **VLAN Segmentation Diagram**: Isolated VLAN per device class, uplink to ZTB, no horizontal VLAN access
3. **Policy Matrix**: Device type → allowed destinations (printer to print server only, camera to NVR only)
4. **Zero-Trust Rules**: Device identity verification, time-of-day restrictions, bandwidth limits per device
5. **Monitoring Dashboard**: Per-device connection health, blocked connections log, anomaly alerts

## Key Configuration
- **Device Classes**: Printers (port 515, 631, 9100), Cameras (port 80, 443, RTSP), HVAC (proprietary ports), Badges (API port), Guest (all)
- **VLAN Isolation**: Dedicated VLAN per device type; printers can't access cameras, cameras can't access HVAC
- **ZTB VLAN Policy**: SVI routes all traffic through ZTB; no native VLAN direct access between device VLANs
- **Printer Routing**: Isolate on separate VLAN; policy allows TCP 515 (LPD), 631 (IPP), 9100 (RAW) to print server only
- **Camera Routing**: Isolate on separate VLAN; policy allows 80, 443 (web UI), RTSP 554 (streaming) to NVR/cloud service only
- **HVAC Controls**: Isolate with strict egress filtering; allow only to HVAC management IP on non-standard ports (e.g., 8080)
- **Badge/Access System**: Isolate if cloud-based (allow port 443 to cloud API); if on-prem, route to access server only
- **Guest VLAN**: Open internet access without corporate intranet; requires RFC 1918 isolation and NAT egress
- **Geofencing**: If devices mobile (printers, cameras in satellite offices), use location-based VLAN policy override

## Gotchas
- **Device Roaming**: Mobile printers/displays may change VLANs; test device behavior on VLAN handoff (may lose connectivity)
- **Multicast Breaks**: mDNS (port 5353) for printer discovery may not cross VLAN boundaries; enable mDNS relay or static IPs
- **Firmware Auto-Update**: Restricting outbound may break firmware updates; document allowed CDNs or version all devices
- **VPN Leakage**: If device has embedded VPN (e.g., camera with cloud backup), egress control may conflict; verify allowed cloud endpoints
- **SNMP Polling**: Monitoring systems polling devices from management VLAN may be blocked; create exception for SNMP (port 161)
- **Syslog/NTP**: Devices need external syslog and NTP; allow UDP 514 (syslog) and UDP 123 (NTP) in policy
- **Time-Based Rules**: Cameras running 24/7 but policy restricts by business hours causes unexpected outages; define schedule carefully
- **Device Spoofing**: Malware mimicking printer MAC may evade VLAN isolation; add port-level authentication (802.1X) if high-risk

## Configuration Checklist
- [ ] All branch IoT/OT devices inventoried with MAC addresses and IP ranges
- [ ] Device class VLANs created and trunked to ZTB
- [ ] Each VLAN SVI configured on ZTB with policy enforcement enabled
- [ ] Printer policy tested with actual printer access attempts
- [ ] Camera policy validated with NVR/cloud service endpoints
- [ ] HVAC policy confirmed with building management system
- [ ] Badge/access system routed correctly (cloud vs on-prem)
- [ ] Guest VLAN isolated from corporate subnets (no RFC 1918 leakage)
- [ ] Device baseline traffic captured for anomaly detection
- [ ] Monitoring alerts configured for policy violations and new devices
