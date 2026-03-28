---
description: "Execute BC failover testing: quarterly DR drills, failover simulation, ZCC behavior during outage, RTO/RPO measurement"
---

# BC Failover Testing

**Persona:** Disaster recovery specialist conducting periodic failover drills.

## When to use
- Quarterly DR drill execution (regulatory requirement or best practice)
- Validating RTO and RPO targets before they're needed
- Testing failover procedure with limited user impact
- Verifying monitoring and alerting detect outage correctly
- Training team on failover runbook steps and decision making

## 5-Gate Artifacts
1. **Drill Schedule Calendar**: Quarterly dates, estimated duration (2-4 hours), stakeholders notified
2. **Pre-Drill Checklist**: Backup validated, BC cloud config current, communication templates ready, rollback plan tested
3. **Drill Execution Log**: Start time, failover trigger, completion time, issues encountered, resolution
4. **RTO/RPO Measurement Report**: Actual recovery time vs target, data loss quantified (policies/users not synced)
5. **Post-Drill Review**: Lessons learned, runbook updates, team feedback, next drill improvements

## Key Configuration
- **Drill Scope**: Full failover (all traffic to BC cloud) vs partial (subset of locations/policies)
- **Trigger Method**: Manual failover command (safest for drill), automatic on primary outage detection (tests automation)
- **User Communication**: Pre-drill notification (24-48 hours), real-time status updates during drill, post-drill summary
- **Monitoring During Drill**: Dashboard showing primary cloud status, BC cloud traffic volume, RTO clock running
- **Rollback Plan**: Clear decision point (T+30 min after failover, decision to revert or continue testing)
- **Traffic Validation**: Sample users in each region accessing key apps during failover (Office 365, Salesforce, internal DC app)
- **Policy Verification**: Check that policies applied in BC cloud match primary cloud; spot-check blocking rules
- **Config Sync Lag**: Measure time from policy change in primary to availability in BC cloud (should be < RPO target)
- **Performance Baseline**: Measure latency, throughput, SSL handshake time during BC cloud operation vs primary
- **Failback Procedure**: Switch traffic back to primary; verify no data loss during switchback; check if config re-sync needed

## Gotchas
- **Drill Communication Breakdown**: If stakeholders not pre-notified, security team may escalate "outage" as real incident; send reminders 24h before
- **Partial Failover Surprises**: If only some locations failover, cross-region traffic may take suboptimal path; test full impact
- **Policy Version Mismatch**: BC cloud config may be hours or days old; if policies changed since last sync, drill finds gaps
- **Performance Degradation Not Acceptable**: Users complain if BC cloud response slower; measure baseline and document expected degradation
- **Rollback Timing**: Switching back too quickly may cause brief policy conflicts if changes were made during failover; plan rollback carefully
- **Certificate Issues**: If BC cloud cert differs, users may see cert warnings; ensure BC cloud certs are approved and distributed
- **RTO Creep**: Actual recovery consistently slower than target suggests target is unrealistic; adjust RTO or improve process
- **Forgot to Sync**: Config changes made to primary after last sync aren't in BC; last-minute policy add causes failover gap
- **License Exhaustion**: If BC tier licensed for 80% of peak and drill uses 100%, it silently throttles; verify license headroom
- **Reverting Stress**: After drill, switching back to primary stresses primary cloud; scale up primary before reverting or do it during off-hours

## Testing Checklist
- [ ] Drill schedule published and stakeholders (security, app teams) notified
- [ ] Primary cloud backup validated (config export successful, file not corrupted)
- [ ] BC cloud config confirmed up-to-date (within RPO window)
- [ ] Test users and apps pre-selected (diverse geographic locations and app types)
- [ ] Monitoring dashboard loaded and ready to track RTO
- [ ] Failover trigger command verified and tested in lab
- [ ] Rollback procedure tested (reverting back from BC to primary)
- [ ] Communication templates prepared (Slack, email, status page updates)
- [ ] Team roles assigned (drill leader, monitor watch, app validator, comms)
- [ ] Rollback decision point and authority defined (who approves staying in BC vs reverting)
- [ ] Post-drill review scheduled within 2 days (while details fresh)
