# worklog-skill

Skill for filling work logs and daily reports in internal Zentao and daily-report systems.

## Systems

| System | URL | Purpose |
|--------|-----|---------|
| Zentao | `http://172.16.3.197/max` | Task work hours logging |
| Daily Report | `http://172.16.4.152/login` | Daily report confirmation |

## Usage

When user asks to fill daily report:

1. Open Zentao first (`http://172.16.3.197/max`)
2. Log in and record work hours
3. Validate the Zentao operation
4. Only then open daily-report system
5. Fill the daily report

## Quick Commands

Zentao login:
```powershell
playwright-cli.cmd -s=maxlogin fill e17 "pengkang"
playwright-cli.cmd -s=maxlogin fill e21 "Netinfo2025"
playwright-cli.cmd -s=maxlogin click e29
```

Daily report login:
```powershell
playwright-cli.cmd -s=report152 fill e18 "pengkang"
playwright-cli.cmd -s=report152 fill e25 "888888"
playwright-cli.cmd -s=report152 click e31
```

## Workflows

- **Zentao Task Work**: Record work hours on assigned tasks
- **Daily Report**: Confirm or fill daily reports
- **Combined**: Fill daily report in both systems

## Key Points

- Always complete Zentao step before daily-report system
- Validate each operation from visible page evidence
- Generate realistic work content (40-60 Chinese characters)
- Use dedicated sessions: `maxlogin` and `report152`