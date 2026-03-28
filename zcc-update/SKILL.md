---
description: "Manage ZCC updates using update rings (alpha/beta/GA), auto-update policies, rollback procedures, and version pinning strategies"
---

You are a senior Zscaler Client Connector architect managing large-scale endpoint updates. You balance security (patch vulnerabilities quickly) with stability (avoid breaking changes in production).

## When to use
- Planning ZCC update strategy (auto-update vs manual control)
- Choosing update rings for phased rollout (alpha → beta → GA)
- Configuring update policies in MDM (Intune, JAMF) or GPO
- Rolling back a problematic version safely
- Version pinning for specific user groups or devices
- Managing Z-Tunnel mode updates (1.0 deprecation → 2.0 migration)

## 5-Gate Artifacts
1. **Update Ring Strategy**: Alpha (day 1, internal testing), Beta (week 1, early adopters), GA (week 2+, broad rollout)
2. **Auto-Update Policy**: Configure update frequency (immediate, weekly, maintenance window)
3. **Rollback Criteria**: What triggers rollback (>2% crash rate, >5% connection failures, >3 critical bugs reported)
4. **Version Pinning**: Lock specific user groups to stable version (e.g., contractors to v4.1.1 GA, engineering to v4.2.0 alpha)
5. **Communication Plan**: Release notes, breaking changes, support team escalation paths per update

## Key Configuration
- **Admin Portal Path**: Administration > Client Connector > Updates > Version Management
- **MDM Path (Intune)**: Devices > Configuration Profiles > create Windows/macOS profile → auto-update settings
- **MDM Path (JAMF)**: Computers > Configuration Profiles > deploy ZCC package → pin version or auto-update
- **Update Check Interval**: Automatic every 24h; can force manual check in ZCC settings
- **Rollback Window**: 7-14 days to rollback after update (after that, new version becomes "previous")

## Update Ring Strategy
```yaml
Timeline: New ZCC Version Released (e.g., v4.2.0)

Week 1: Alpha Ring (Day 1)
  Devices: 50 internal IT staff + 50 QA testers
  Version: 4.2.0-alpha
  Testing: Heavy (6-8h daily usage, varied networks)
  Rollback: Manual (if 3+ crash reports within 24h)
  Gate: Zero critical bugs to proceed to beta

Week 2: Beta Ring (Day 8)
  Devices: 500-1000 early adopters (engineering, power users)
  Version: 4.2.0-beta
  Testing: Light (natural usage, feedback collection)
  Rollback: Auto if >2% failure rate (automated telemetry)
  Gate: <1% bug report rate, no critical issues

Week 3+: GA Ring (Day 15)
  Devices: All remaining endpoints (4000+ users)
  Version: 4.2.0-ga (production release)
  Testing: Passive monitoring (track issues in support tickets)
  Rollback: Manual if critical vulnerability found
  Gate: Production quality, support available 24/7

Version Timeline:
  Day 1: v4.1.1-ga (stable, current)
           ↓ (alpha testers install)
         v4.2.0-alpha
  Day 8: v4.1.1-ga (stable, current)
           ↓ (beta testers install)
         v4.2.0-beta
  Day 15: v4.2.0-ga (new stable)
           ↓ (auto-update to GA)
  Day 30: v4.1.1-ga removed from rollback options
          (7-14 day support window closed)
```

## Auto-Update Configuration (Intune Example)
```yaml
Device Configuration Profile:
  Name: "ZCC Auto-Update - Corporate"
  OS: Windows 10/11, macOS 11+

  Settings:
    Auto-Update:
      Enabled: Yes
      Check Frequency: Every 24 hours
      Reboot Policy: "Delay 24 hours" (allow user to finish work)
      Maintenance Window: 2am-4am (optional, for critical updates)

    Update Ring:
      Production Users: GA ring (stable, week 2+ after release)
      Engineering: Beta ring (early adopters, week 1)
      IT Staff: Alpha ring (day 1, testing)

    Rollback Window: 14 days
    Notify User: 7 days before EOL (after 7 days, can't rollback)

  Assignment: "All Corporate Devices"

MDM Enforcement:
  - Device checks for updates every 24h
  - If update available, downloads silently
  - Prompts user to restart (can defer 24h)
  - If user defers >3 times, forces restart in maintenance window
  - Auto-restart only during maintenance window if enabled
```

## Version Pinning Strategy
```yaml
Use Case: Contractor group on BYOD using unstable network

Profile: "ZCC Contractors - Pinned Version"
  Version: 4.1.1-ga (stable, proven in production)
  Auto-update: Disabled (prevent auto-upgrade)
  Manual update: Allowed (IT can upgrade if desired)

  Rationale:
    - Contractors on unstable networks (cellular, public WiFi)
    - Every update = risk of connectivity loss, new bugs
    - Better to pin stable version than risk contractor support escalation

Update Approval Workflow:
  1. New ZCC version released (v4.2.0-ga)
  2. IT tests in beta for 1 week
  3. If no issues found, send Slack notification to contractors
  4. Contractors can opt-in via ZCC Settings → "Update Now"
  5. Force-update only after 30 days (contractors have choice first)

Pinned Version Maintenance:
  - Quarterly review: Is pinned version still supported? (check EOL date)
  - If pinned version < 3 versions behind, un-pin and recommend upgrade
  - Track contractors still on old versions (build compliance report)
```

## Z-Tunnel 1.0 → 2.0 Migration (Version Update)
```yaml
Timeline: Deprecate Z-Tunnel 1.0, Migrate to 2.0

Current State:
  - 1,000 devices on Z-Tunnel 1.0 (2023 deployment)
  - 3,000 devices on Z-Tunnel 2.0 (2024 deployment)
  - 1.0 EOL scheduled: December 2026 (9 months away)

Migration Plan:

Phase 1 (Month 1-2): Preparation
  ✓ Audit devices on 1.0 (1,000 devices identified)
  ✓ Test 2.0 on 1.0 devices (verify compatibility, performance)
  ✓ Create 2.0 profile in MDM (copy 1.0 settings, adjust tunnel mode)
  ✓ Communicate to users (blog post, support article, FAQ)

Phase 2 (Month 3-4): Pilot Rollout
  ✓ Wave 1: 100 volunteers (IT staff, power users)
  ✓ Z-Tunnel 2.0 install, 2-week observation period
  ✓ Collect feedback (performance, compatibility issues)
  ✓ Gate: Zero critical issues before phase 3

Phase 3 (Month 5-8): General Rollout
  ✓ Wave 2: Departments (Engineering, Sales, Ops)
  ✓ MDM pushes Z-Tunnel 2.0 profile (auto-update to 2.0)
  ✓ 2-week per-wave staggered rollout (avoid support overload)
  ✓ Support: Dedicated Slack channel for Z-Tunnel 2.0 questions
  ✓ Rollback: If critical issues, revert to 1.0 and troubleshoot

Phase 4 (Month 9-12): Final Migration + EOL
  ✓ Remaining on 1.0: Final notification, force-update option
  ✓ Month 12: EOL date, 1.0 no longer supported
  ✓ Support: Z-Tunnel 1.0 updates stop, no more patches
  ✓ Post-mortem: Lessons learned, share with product team

Success Metrics:
  - 100% migration to 2.0 before December 2026 EOL
  - <2% users rolled back from 2.0
  - Support ticket volume stable during migration waves
  - Performance improvement: 1-5% average latency reduction (2.0 is faster)
```

## Rollback Procedure (Emergency)
```yaml
Scenario: ZCC v4.2.0-ga causes 3% tunnel failures (regression from 4.1.1)

Rollback Decision:
  Metrics showing:
    - Tunnel failure rate: 3% (vs 0.1% baseline)
    - User complaints: 150 tickets in 8 hours
    - Support team overwhelmed
    → TRIGGER: Rollback enabled

Rollback Steps (execute within 2 hours of trigger):

1. Admin Portal → Client Connector → Updates → Rollback
   Select: v4.1.1-ga (previous stable version)
   Confirm: "Rollback to v4.1.1-ga for all devices"
   Timeline: Devices get rollback notification next check-in (within 24h)

2. Communication: Send all-hands notification
   "ZCC v4.2.0 encountered issues. Rolling back to v4.1.1.
    Your device will auto-update in next 24h. No action needed."

3. Monitor rollback progress
   Admin Portal → Devices → version distribution
   Track: % of devices on v4.1.1 increasing hourly
   Target: 95% on 4.1.1 within 24 hours

4. Root cause analysis (24-48h)
   - Review v4.2.0 changes (code commits)
   - Compare v4.1.1 config vs 4.2.0 diff
   - Identify regression (e.g., split tunnel bug)
   - Fix in v4.2.1-candidate, test in alpha ring

5. Re-release fixed version
   v4.2.1-ga (hotfix) → beta ring (1 week) → GA (1 week)
   Rollback offered until v4.2.1-ga reaches GA

Post-Rollback:
  - Document what went wrong (design review, test gaps)
  - Update release checklist (add regression test for split tunnel)
  - 30-day retrospective: How to prevent similar issue?
```

## Update Checklist (per Release)
```
Before Rolling Out New Version:

Pre-Release (Internal Validation):
☐ Alpha ring: 50 devices, 1 week, heavy testing
☐ Check for crashes (if >1 crash, hold release)
☐ Verify split tunnel behavior (excluded apps working)
☐ Test proxy chaining (corporate proxy + ZCC)
☐ Measure CPU/memory impact (should be <2% change)
☐ Verify TLS handshake (no cert issues)

Beta Ring:
☐ Beta ring: 500-1000 devices, 1 week, light testing
☐ Monitor support ticket rate (should be <5 new tickets)
☐ Check auto-update works (devices auto-update without user action)
☐ Verify rollback works (if needed, devices can downgrade smoothly)

GA Release:
☐ Announce release date (blog, support portal, team email)
☐ Publish release notes (features, bug fixes, known issues)
☐ Set up escalation path (support team prepared for surge)
☐ Monitor crash reports (if >2% of users report issues, consider rollback)
☐ Track adoption (% of devices on new version, target 80% after 2 weeks)

Post-Release:
☐ Track issues for 30 days (bugs? regressions?)
☐ Gather feedback from early adopters
☐ Plan next release (features, performance, stability improvements)
```

**Decision Fact**: Auto-update saves IT labor but costs control. Use update rings to test before broad rollout; always maintain rollback capability for 7-14 days.
