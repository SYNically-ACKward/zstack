---
description: "Universal cutover runbook: hour-by-hour schedule, T-24h prep, MDM swap, validation, rollback, war room, monitoring"
---

# Migration Cutover

**Persona:** Migration program manager executing cutover from legacy security vendor to Zscaler.

## When to use
- Executing final go-live cutover from legacy vendor to Zscaler
- Coordinating enterprise-wide device transition (ZCC rollout, legacy client removal)
- Running war room and real-time decision making during cutover window
- Validating policy enforcement and application connectivity post-cutover
- Executing rollback if critical issues detected

## 5-Gate Artifacts
1. **Cutover Schedule**: Hour-by-hour timeline (T-24h through T+4h), pre-cutover prep tasks, cutover execution sequence, post-cutover validation
2. **Rollback Decision Tree**: Severity-based triggers (critical blocker → rollback, warning → continue monitoring, informational → document)
3. **War Room Setup**: Participants (infrastructure, security, app teams, vendor support), escalation matrix, decision authority, communication channels
4. **Validation Checklist**: Per-phase health checks (connectivity, app access, policy enforcement, performance)
5. **Communication Plan**: User notification schedule, status page updates, stakeholder briefings, post-cutover all-hands

## Pre-Cutover Phase (T-5 Days to T-0)

### T-5 Days: Final Prep
- Confirm pilot phase completed (5-10% of users on Zscaler 1-2 weeks, no critical issues)
- Validate all policies migrated and tested (ZIA rules, ZPA access, DLP, threat prevention)
- Confirm ZCC deployment tested (MDM rollout scripts, silent installation verified)
- Verify legacy client uninstall procedure (Netskope, Cisco Umbrella, Forcepoint agent) tested
- Reserve war room and conference bridges; test A/V and screen sharing
- Confirm all vendor support (primary, secondary, Zscaler) contacts are on standby

### T-3 Days: Communication & Prep
- Send user communication (cutover date/time, expected downtime 2-4 hours, support contacts)
- Brief executive stakeholders (RTO/RPO targets, success criteria, abort criteria)
- Confirm IT teams available (no other maintenance windows during cutover)
- Test rollback procedure (verify legacy vendor can be restored, appliances powered up if needed)
- Stage rollback config and scripts (hot-standby appliances or backup configs available)

### T-2 Days: Final Validation
- Re-run policy validation (sample traffic through Zscaler, compare to legacy enforcement)
- Confirm ZCC MDM rollout scripts ready and staged
- Validate legacy client removal scripts ready
- Test user notification templates (email, Slack, status page)
- Confirm war room infrastructure (phones, laptops, power, internet)
- Brief cutover lead and backup lead on runbook (both must be able to execute)

### T-1 Day: Final Checks
- Confirm Zscaler cloud and BC cloud status healthy (no outstanding issues)
- Verify ZCC deployment pipeline loaded and tested
- Confirm legacy client uninstall pipeline ready
- Stage network config changes (BGP metric changes, route redistribution) if needed
- Power on HA appliances or backup systems (if on-premises fallback required)
- Set up real-time monitoring dashboard (tunnel health, policy hits, application connectivity)

## Cutover Execution Phase (T-24h through T+0)

### T-24 Hours: Pre-Flight Check
- **06:00 UTC**: War room opens; participants join conference
- **06:30 UTC**: Rollback procedure walkthrough (leads execute dry-run)
- **07:00 UTC**: Health check: Zscaler cloud + legacy vendor status
- **07:30 UTC**: Confirm all users notified and support team in place
- **08:00 UTC**: Final go/no-go decision; if "no-go," reschedule and notify users

### T-12 Hours: Pre-Cutover Staging
- **14:00 UTC**: Stage network config changes (do not activate)
- **14:30 UTC**: Stage policy rule changes in Zscaler (do not activate)
- **15:00 UTC**: Confirm ZCC MDM rollout queued and ready to push
- **15:30 UTC**: Confirm legacy client uninstall queued and ready to push
- **16:00 UTC**: Review escalation matrix and war room roles

### T-4 Hours: Prepare for Go-Live
- **20:00 UTC**: War room members on standby (laptops charged, phones ready)
- **20:30 UTC**: Verify monitoring dashboard live and baseline metrics visible
- **21:00 UTC**: Confirm Zscaler support on line (bridge open, support engineers ready)
- **21:30 UTC**: Final user notification (cutover begins in 30 minutes, expect 2-4 hour window)

### T-0 (Cutover Start): Go-Live Execution
- **22:00 UTC**: CUTOVER START. Record in war room log.
- **22:00-22:30**: Activate network config changes (BGP, static routes, VLAN steering to Zscaler)
  - Monitor BGP convergence (30-60 sec)
  - Validate routes resolving to Zscaler cloud
  - Test DNS resolution (Zscaler cloud reachable)
  - **Decision checkpoint**: If routes fail to converge in 2 min, rollback network changes
- **22:30-23:00**: Activate Zscaler policy rules (DIA, backhaul, DLP enforcement live)
  - Monitor policy hit rate (should see traffic flowing)
  - Spot-check blocking rules (verify legitimate traffic not blocked)
  - **Decision checkpoint**: If > 5% of traffic blocked unexpectedly, review rules and adjust
- **23:00-23:30**: Push ZCC MDM deployment (staggered: 20% of devices per 5 min)
  - Monitor install success rate (target > 95% on first device batch)
  - Watch for conflicts with legacy clients still running
  - **Decision checkpoint**: If ZCC install failure > 20%, pause and investigate
- **23:30-00:30**: Push legacy client uninstall (staggered: 20% of devices per 10 min)
  - Monitor uninstall success and reboot behavior
  - Watch for service impact (users report connectivity loss)
  - **Decision checkpoint**: If uninstall failure > 10% or user complaints spike, pause
- **00:30-01:30**: Monitor stability (all clients rolled over to ZCC)
  - Watch for new errors, policy violations, or performance degradation
  - Confirm ZPA tunnel establishment (should see all users tunneled)
  - **Decision checkpoint**: Go/No-Go gate. If critical issues, prepare rollback.

### T+1 Hour to T+4 Hours: Validation & Stabilization
- **01:30-02:30**: Validation phase
  - Test key applications (Office 365, Salesforce, internal DC app)
  - Verify DLP blocking (test with sample PII, confirm detection)
  - Check ZCC client health (connectivity, update checks)
  - **Decision checkpoint**: If validation fails, escalate to rollback decision
- **02:30-03:30**: Policy tuning
  - Monitor false positives (legitimate traffic blocked)
  - Adjust policy rules if needed (use least-disruptive changes)
  - Watch threat prevention hits (ensure not over-aggressive)
- **03:30-04:30**: Performance validation
  - Measure latency (VoIP, video conferencing, real-time apps)
  - Confirm DIA routes responding (measure throughput vs baseline)
  - Validate encrypted traffic (tunnels stable, no disconnects)
- **04:30 UTC**: Go/No-Go decision gate
  - If validation passed: proceed to post-cutover, exit war room status
  - If critical issues: execute rollback (see below)

## Rollback Procedure (If Triggered)

### Rollback Criteria
- Critical application down (Office 365, Salesforce, internal VoIP)
- > 20% of users unable to connect
- Policy enforcement broken (all traffic allowed or all traffic blocked)
- Zscaler cloud unreachable (connectivity failure)
- Performance < 50% of baseline (extreme latency)

### Rollback Steps
1. **Decision**: Cutover lead and executive sponsor approve rollback
2. **Communication**: Update status page and notify users (issue detected, reverting)
3. **Network Config Revert** (5-10 min):
   - Revert BGP metrics to legacy vendor priority
   - Revert static routes to legacy vendor path
   - Verify convergence (legacy vendor taking traffic again)
4. **Policy Revert** (5 min):
   - Disable Zscaler policy rules
   - Enable legacy vendor policy rules
   - Verify legacy policies active
5. **Client Rollback** (optional, 30-60 min if time permits):
   - MDM push legacy client installation
   - MDM push ZCC uninstall
   - **Note**: Full client rollback may take 1-2 hours; network revert above is faster priority
6. **Validation** (10 min):
   - Test connectivity (legacy vendor path working)
   - Verify applications accessible
   - Confirm users reporting normal service
7. **War Room Debrief**: Document what went wrong, schedule RCA, communicate RTO to users

## Post-Cutover Phase (T+4h through T+24h)

### T+4 Hours: Cutover Lead Sign-Off
- Confirm validation passed all checkpoints
- Confirm 95%+ device migration to ZCC
- Confirm policy enforcement working as expected
- Exit war room status but keep monitoring active

### T+4 to T+8 Hours: Monitoring
- Watch for user reports (email, tickets, Slack)
- Monitor dashboard for anomalies (unusual traffic patterns, policy violations)
- Escalate any new issues immediately
- Track device migration completion (aim for 99% within 8 hours)

### T+8 to T+24 Hours: Stabilization
- Continue monitoring (watch for late-night issues if cutover during business hours)
- Monitor ZCC performance (CPU, memory, battery drain on laptops)
- Collect performance baseline data (latency, throughput)
- Prepare post-cutover communication (success message, thank you to teams)

### T+24 to T+72 Hours: Follow-Up
- Conduct all-hands debrief (what went well, lessons learned)
- Archive cutover logs and decision log
- Confirm legacy vendor decommissioning schedule (appliances to be decommissioned, accounts to be closed)
- Plan post-launch monitoring (ongoing for 2 weeks before declaring "cutover complete")

## War Room Roles & Responsibilities

**Cutover Lead** (Decision Authority)
- Owns cutover timeline and go/no-go decisions
- Communicates with executive sponsor
- Decides rollback trigger

**Infrastructure Lead** (Network & Systems)
- Executes network config changes
- Monitors BGP convergence and route health
- Stages MDM rollout and legacy client removal
- Escalates network issues

**Security Lead** (Policy & Threat)**
- Monitors policy enforcement and hits
- Watches for anomalies and false positives
- Adjusts policies if needed
- Escalates policy issues

**Application Lead** (Connectivity & Usability)
- Tests applications (Office 365, Salesforce, DC apps)
- Monitors user reports and tickets
- Escalates application connectivity issues
- Validates DIA vs backhaul routing

**Zscaler Support Engineer**
- On standby throughout cutover
- Provides real-time guidance on policy, performance, troubleshooting
- Escalates cloud-side issues to Zscaler NOC
- Available for immediate consultation

**Scribe** (Documentation)
- Logs timeline and decisions in shared document
- Records issues discovered, resolutions, and decision points
- Archives logs for post-mortem review

## Success Criteria & Metrics

**Phase 1 (T+0 to T+30 min)**: Network & Policies Active
- BGP convergence < 2 min ✓
- > 95% of traffic routed through Zscaler ✓
- Policy rules enforcing (see policy hits in dashboard) ✓

**Phase 2 (T+30 min to T+2 hours)**: Device Migration
- ZCC MDM rollout > 95% success ✓
- Legacy client uninstall > 95% success ✓
- Zero or minimal device conflicts ✓

**Phase 3 (T+2 to T+4 hours)**: Application & Performance
- Key apps accessible (Office 365, Salesforce, DC VPN) ✓
- Latency within baseline + 20% tolerance ✓
- DLP enforcement working (test with sample PII) ✓

**Phase 4 (T+4 to T+24 hours)**: Stabilization
- User satisfaction > 90% (no spike in support tickets) ✓
- Device migration to 99%+ completion ✓
- No critical issues requiring rollback ✓

## Configuration Checklist
- [ ] Cutover date/time locked and executive approved
- [ ] Pre-cutover pilot phase completed (5-10% users, 1-2 weeks, no blockers)
- [ ] Policy migration completed and tested on sample traffic
- [ ] ZCC deployment script tested (silent install, no conflicts)
- [ ] Legacy client uninstall script tested (clean removal, no issues)
- [ ] War room booked and participants confirmed
- [ ] Rollback procedure tested and validated
- [ ] User communication templates prepared and reviewed
- [ ] Network config changes staged and tested (non-prod)
- [ ] Monitoring dashboard configured and baseline captured
- [ ] Vendor support contacts confirmed (Zscaler, legacy vendor, others)
- [ ] RTO/RPO targets communicated to stakeholders
- [ ] Success criteria and go/no-go gates defined
- [ ] Post-cutover communication plan (all-hands, status updates) ready
