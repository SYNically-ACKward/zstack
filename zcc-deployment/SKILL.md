---
description: "Deploy Zscaler Client Connector via MDM, GPO, or manual install with app/forwarding profiles and Z-Tunnel mode selection"
---

You are a senior Zscaler Client Connector architect. You deploy ZCC at scale through MDM, Group Policy, or manual installation, with careful consideration of tunnel modes and profile configuration.

## When to use
- Deploying ZCC to 100+ endpoints via Intune or JAMF
- Configuring device enrollment, app profiles, and forwarding modes
- Choosing between Z-Tunnel 1.0 (legacy, deprecated) and Z-Tunnel 2.0 (modern, kernel-based)
- Managing profiles for different user groups (corporate, BYOD, contractor, VPN fallback)
- Troubleshooting deployment failures or profile conflicts

## 5-Gate Artifacts
1. **MDM Integration**: Intune/JAMF enrollment, automatic agent deployment, profile assignment by group
2. **Tunnel Mode Selection**: Z-Tunnel 2.0 (kernel VPN driver, preferred) vs 1.0 (legacy, deprecated)
3. **App Profiles**: Which apps/services route through ZCC tunnel (Slack, email) vs local (video conferencing)
4. **Forwarding Profiles**: DNS forwarding, split tunneling, proxy settings per user group
5. **Deployment Runbook**: Rollout schedule, pilot validation, rollback criteria, user communication

## Key Configuration
- **Admin Portal Path**: Administration > Client Connector > Profiles > Agent Profiles
- **MDM Path (Intune)**: Devices > Configuration Profiles > Create Profile > macOS/Windows; reference ZCC template
- **MDM Path (JAMF)**: Computers > Configuration Profiles > New; assign ZCC package + profiles
- **Agent Version**: Always deploy latest GA version; enable auto-update for zero-touch upgrades
- **Tunnel Mode**: Z-Tunnel 2.0 (kernel VPN, <1ms latency overhead); 1.0 no longer supported
- **Profile Assignment**: Match to user groups (Corporate = full tunnel, BYOD = limited apps)

## Z-Tunnel Mode Comparison
| Feature | Z-Tunnel 1.0 | Z-Tunnel 2.0 |
|---------|---|---|
| Architecture | User-space agent | Kernel VPN driver |
| Latency overhead | 5-10ms | <1ms |
| App exclusion | Manual list | Granular per-app |
| Split tunneling | Limited | Full support |
| CPU usage | 5-15% idle | 1-3% idle |
| Network type support | Ethernet, WiFi | All (including VPN stacking) |
| Status | Deprecated (EOL 2026) | Current, recommended |
| MDM support | Legacy profiles | Full MDM integration |

## Deployment Pattern: Intune + Z-Tunnel 2.0
```yaml
Step 1: Create ZCC Agent Profile in Intune
  Configuration Profile Name: "Zscaler Client Connector"
  OS Target: Windows 10/11, macOS 11+
  Settings:
    - Agent auto-update: Enabled
    - Tunnel mode: Z-Tunnel 2.0
    - Logging level: Debug (for pilot, Info for production)
    - DNS forwarding: Enabled (cloud DNS)

Step 2: Create App Profile
  Name: "Corporate Apps - Full Tunnel"
  Apps included (route through ZCC):
    - Slack, Teams, email (IMAP/SMTP), OneDrive, SharePoint
  Apps excluded (local direct):
    - Video conferencing (Zoom, Teams calls), VPN (fallback)
  Split tunnel: Disabled (full tunnel for corporate assets)
  Assignment: All corporate users

Step 3: Create BYOD Profile
  Name: "BYOD - Limited Access"
  Apps included:
    - Slack, email, corporate web portal
  Apps excluded:
    - All video conferencing, personal cloud (iCloud, Google Drive)
  Split tunnel: Enabled (only corporate apps)
  Assignment: BYOD user group

Step 4: Deployment Wave
  Wave 1 (Pilot): 50 IT staff + 50 power users
    Rollout: Monday 8am, 24-hour validation window
    Validation: Check connectivity, profile assignment, split tunnel behavior
    Rollback: Revert agent policy if >3 incidents/day

  Wave 2 (Early Adopter): 500 mixed users
    Rollout: Following Monday, staggered (8am-5pm)
    Success criteria: <1% complaints, <5% performance impact
    Support: Dedicated Slack channel

  Wave 3 (General Pop): 4000+ remaining users
    Rollout: Staggered 2-week window
    Support: Self-serve portal + chatbot
```

## Group Policy (GPO) Deployment (Windows Only)
```yaml
GPO: Deploy Zscaler Client Connector
  Location: Computer Configuration > Software Installation
  Package: ZCC-Agent-Latest-GA.msi
  Installation options:
    - Uninstall previous versions: Yes
    - Force reinstall: No
    - Reboot after install: Yes (can delay 2h)

Configuration via Registry (after agent installation):
  Path: HKEY_LOCAL_MACHINE\Software\Zscaler\Client\Agent
  Keys:
    - TunnelMode: "ZTunnel2.0"
    - AutoUpdate: 1 (enabled)
    - LogLevel: "Info"
    - ProxyPort: 8080 (if needed)

Rollout: Use GPO targeting (security groups) for phased rollout
  - Pilot: Group "ZCC-Pilot-Global-01"
  - Early adopter: Group "ZCC-EarlyAdopter-Global-02"
  - Production: All computers (via default GPO)
```

## Manual Deployment (Small Sites, Contractors)
```bash
# macOS
curl -O https://zscaler.download/zcc-agent-latest-macos.dmg
open zcc-agent-latest-macos.dmg
# Drag ZCC to Applications folder
# Open System Preferences > VPN > Add (auto-detects ZCC)
# Enter credentials and enroll

# Windows
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://zscaler.download/zcc-agent-latest-windows.msi', 'zcc-agent.msi')"
msiexec.exe /i zcc-agent.msi /quiet /norestart
# Reboot
# Open Settings > VPN > Add VPN (auto-detects ZCC)
# Enter credentials and enroll

# Linux (Ubuntu)
sudo curl -O https://zscaler.download/zcc-agent-latest-linux-ubuntu.deb
sudo dpkg -i zcc-agent-latest-linux-ubuntu.deb
sudo systemctl start zscaler
# Authenticate via browser
```

## Profile Assignment Matrix
| User Type | Tunnel Mode | Split Tunnel | Apps Included | Apps Excluded |
|-----------|---|---|---|---|
| Corporate Desktop | Z-Tunnel 2.0 | No | Slack, email, Salesforce | Video, VPN |
| Contractor | Z-Tunnel 2.0 | Yes | Assigned app only | All others |
| BYOD | Z-Tunnel 2.0 | Yes | Slack, email, portal | Video, personal cloud |
| VIP (Exec) | Z-Tunnel 2.0 | No | All corporate apps | None |
| Support Fallback | Z-Tunnel 2.0 | Yes | Emergency apps | Full tunnel option |

## Deployment Checklist
```
Pre-Deployment:
☐ Choose MDM (Intune/JAMF) or GPO delivery method
☐ Select Z-Tunnel 2.0 (not 1.0)
☐ Define app profiles per user group
☐ Test on pilot devices (5-10) for compatibility
☐ Measure baseline performance (before agent)
☐ Plan rollback (keep agent removal profiles ready)
☐ Communicate schedule and support contacts

Deployment:
☐ Deploy to pilot group (wave 1)
☐ Validate profile assignment (admin portal > devices)
☐ Test split tunnel behavior (excluded apps route local)
☐ Measure latency impact (<2ms added latency acceptable)
☐ Gather user feedback (support ticket trends)
☐ Fix issues before expanding to wave 2

Post-Deployment:
☐ Monitor agent health (admin portal > agent status)
☐ Enable auto-update (zero-touch version upgrades)
☐ Document any app exclusions or custom profiles
☐ Plan quarterly profile reviews (add new apps, remove old)
```

**Decision Fact**: Z-Tunnel 2.0 is kernel-based and performs like native OS VPN; 1.0 is deprecated and should not be deployed new. Migrate all 1.0 to 2.0 within 12 months.
