---
description: "Deploy Nanolog Streaming VMs for high-volume log export to SIEM in CEF, LEEF, or JSON formats"
---

**SIEM Integration Architect** | Zscaler Zero Trust Exchange | SecOps Infrastructure Lead

Implement Nanolog Streaming to reliably export Zscaler logs to enterprise SIEM (Splunk, ArcSight, QRadar) at scale with proper formatting, deduplication, and high availability.

## When to use

- Exporting 10K-1M events/day from Zscaler to centralized SIEM (Splunk, ArcSight, QRadar) for correlation and threat hunting
- Maintaining compliance evidence (audit logs, access logs) in immutable SIEM archive with retention per regulation
- Scaling beyond API pull limitations (throughput caps, latency spikes, API quota burn)
- Deduplicating logs across multiple Zscaler components (ZPA, ZSB, ZCC, Firewall) to single SIEM instance
- Ensuring high availability (NSS VM failover, redundant paths) for uninterrupted log delivery during incidents
- Meeting regulatory requirements for audit log retention (7 years for finance, 6 years for healthcare)

## 5-Gate Artifacts

1. **NSS VM Deployment Architecture** - VM count based on throughput requirement (1 VM per 100K EPS), HA pair with failover IP and heartbeat monitoring, network connectivity (direct to SIEM, via proxy), sizing (CPU 4-16 cores, RAM 8-32GB, disk auto-purge at 90%), deployment across zones for redundancy

2. **Log Format Specification** - CEF (CEF:0|Zscaler|ZPA|...), LEEF (Leef:1|Zscaler|...), JSON format with field mappings (source IP → src, destination IP → dst, action → act, user → user), validate format compliance before SIEM ingestion

3. **Bandwidth Sizing Calculator** - Average log size per event (100-500 bytes), peak concurrency (burst handling), retention period on NSS disk, transport overhead (TCP/TLS encryption), estimated WAN bandwidth requirements, cost analysis per format

4. **SIEM Receiver Configuration** - Splunk heavy forwarder listening on 514/TCP, ArcSight connector receiving CEF with ACK, QRadar protocol handler for JSON with compression; manage credentials in vault; renew TLS certs 90 days before expiry

5. **Operational Monitoring & Alerting** - NSS VM health dashboard (CPU, memory, disk, log queue depth, transport latency), alert on queue overflow (>80%), missed events (gap detection), transport failures (retry count), disk full prediction; quarterly maintenance window

## Key Configuration

- **HA Configuration**: Deploy two NSS VMs in active-passive or active-active mode; implement heartbeat monitoring with automatic failover (<5 second RTO); test failover process monthly; maintain load balancer for multi-NSS scaling

- **Log Format Selection**: CEF for broad SIEM compatibility, JSON for parsing flexibility and schema validation, LEEF for IBM/ArcSight optimization; choose based on SIEM parsing efficiency and downstream analytics

- **Deduplication**: Enable NSS deduplication to remove duplicate events from multiple sensors/proxies; configure correlation window (60-300 seconds based on event frequency); verify deduplication effectiveness monthly

- **Field Filtering**: Exclude verbose fields (full HTTP body) to reduce bandwidth but retain critical fields (user, action, threat name, severity, destination IP); balance detail vs. throughput

- **Retry Logic**: NSS retries failed sends for 24 hours with exponential backoff; configure disk-based queue to prevent loss during SIEM maintenance; monitor queue drain rate to detect backpressure

- **TLS & Encryption**: Implement mTLS for NSS-to-SIEM communication; rotate certificates quarterly; validate cipher suite strength; log certificate validation failures for debugging

## Gotchas

- NSS VM disk fills quickly with large throughput; configure auto-purge on disk usage >90%, but monitor for loss during rotation; implement disk space prediction to warn before full

- CEF escaping for special characters (pipe, equals, newline) critical for parser; test with real Zscaler events containing Unicode, embedded URLs, special characters in domain names

- SIEM receiver tuning required for throughput; Splunk HF may need increased queue sizes (default 512MB often insufficient), QRadar may need protocol handler scaling; load test before production

- TLS certificate expiration breaks log export silently; automate certificate renewal and alerting 90 days before expiry; implement certificate pinning to prevent MITM

- NSS VM network egress limits (AWS NAT bandwidth, corporate proxy throughput) can throttle log export; monitor and upgrade as needed; implement compression to reduce bandwidth

- Log lag (time between event and SIEM arrival) can exceed SLA if queue backlog accumulates; alert if lag >5 minutes; measure end-to-end latency from event timestamp to SIEM ingestion

- NSS VM memory leaks or log parsing inefficiencies can cause gradual performance degradation; restart NSS VM monthly and monitor for memory trend; upgrade JVM heap if needed
