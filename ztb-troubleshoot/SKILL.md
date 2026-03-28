---
description: "Troubleshoot ZTB: tunnel health, failover events, throughput issues, appliance diagnostics"
---

# ZTB Troubleshooting

**Persona:** Network support engineer diagnosing ZTB operational issues.

## When to use
- Tunnel down or intermittent connectivity issues
- HA failover events or unexpected failback behavior
- Throughput degradation or packet loss
- Appliance CPU/memory/disk resource exhaustion
- Certificate or licensing expiration causing failures

## 5-Gate Artifacts
1. **Tunnel Health Dashboard**: Real-time ZPA tunnel status, latency, jitter, packet loss per tunnel
2. **Failover Event Timeline**: Active/standby status transitions, trigger reason (heartbeat loss, resource threshold)
3. **Throughput Bottleneck Analysis**: CPU usage, memory, NIC saturation, tunnel crypto overhead
4. **Appliance Diagnostic Report**: Syslog export, system resource snapshots, active connection count
5. **Resolution Runbook**: Root cause analysis, corrective action taken, verification steps completed

## Key Configuration
- **Tunnel Status CLI**: `show tunnel status` lists all ZPA/DIA tunnels, state, latency, connections
- **HA Heartbeat**: Primary/secondary exchange every 1-3 sec on dedicated interface; timeout triggers failover
- **Failover Threshold**: Configurable heartbeat loss detection (default 10 sec = 3-4 missed heartbeats); lower = faster failover, higher = stable
- **CPU/Memory Thresholds**: Alert at 85% utilization; failover at 95% to prevent state-sync failure
- **Disk Usage**: /config and /log partitions monitored; full /log triggers compression and eventual fail-safe shutdown
- **NIC Counters**: RX/TX errors, CRC, collisions, overrun; rising errors suggest duplex mismatch or bad cable
- **Tunnel Crypto**: AES-GCM default; CPU intensive; lower MTU or segment count may reduce CPU on older ZT-200
- **Connection Tracking**: `show connection count` displays active sessions; > 80% threshold suggests appliance nearing limit

## Gotchas
- **Heartbeat False Positive**: Network blip causes secondary to assume primary is down; brief ECMP load-sharing until primary detects and pulls back
- **State-Sync Congestion**: High throughput saturates state-sync link; active and standby lose state consistency; connections briefly drop on failover
- **CPU Thermal Throttling**: ZT-600 in hot rack runs hot; thermal throttling degrades throughput; may appear as random packet loss
- **BGP Convergence Lag**: After failover, BGP may take 30-60 sec to converge; traffic temporarily uses suboptimal path
- **Certificate Expiration Silent**: Expired tunnel cert doesn't show in GUI; tunnel appears "up" but can't authenticate; check cert dates in syslog
- **Memory Leak**: Long-running ZTB may leak memory; old connections not fully cleaned up; weekly reboot mitigates
- **NTP Drift**: If NTP unsync'd, tunnel re-authentication fails; device clock can drift > 5 min in a week without NTP
- **Duplicate Sessions**: Failover during active session creation can create duplicate state on standby; may cause brief double-billing or duplicate traffic

## Troubleshooting Steps
1. **Check Tunnel Status**: `show tunnel status` to confirm ZPA/DIA tunnel state
2. **Verify HA Heartbeat**: `show redundancy status` and check heartbeat RX/TX count in syslog
3. **Capture Syslog**: Export and grep for "TUNNEL_DOWN", "FAILOVER", "CERT_EXPIRED" events
4. **Check Resource Utilization**: `show system resource` and monitor CPU, memory, disk for 5 minutes
5. **Packet Capture**: If throughput issue, capture on WAN interface; check for retransmits, fragmentation
6. **BGP Peer Status**: If using BGP, verify neighbor relationships with `show bgp neighbors` and route count
7. **NTP Status**: Confirm time sync with `show ntp status` and sync stratum < 5
8. **DNS Resolution**: Test DNS from ZTB CLI; if ZPA bootstrap fails, DNS may be blocking Zscaler domains
9. **Licensing**: Check license expiration with `show license` and ensure throughput tier matches current subscription
10. **Reboot Validation**: If issue persists, plan maintenance reboot; verify HA failover first

## Configuration Checklist
- [ ] Tunnel status dashboard accessible from ZCC portal
- [ ] HA heartbeat interval tuned to customer network stability expectations
- [ ] Resource thresholds defined and alerting configured (PagerDuty, email)
- [ ] Syslog exported to centralized collector with long-term retention (90+ days)
- [ ] Packet capture tool validated for WAN interface diagnostics
- [ ] Certificate renewal process automated or calendar-alerted (30 days before expiry)
- [ ] NTP sources redundant and validated from ZTB
- [ ] Weekly resource trend reports generated and reviewed
- [ ] Failover drills scheduled quarterly to validate RTO
