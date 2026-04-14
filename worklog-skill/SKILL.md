---
name: worklog-skill
description: Use when Codex needs to open the internal Zentao task system at 172.16.3.197 or the internal daily-report system at 172.16.4.152, log in with provided credentials, inspect assigned tasks or daily-report confirmation lists, and fill or save work logs or daily reports through playwright-cli. When the user asks to fill a daily report, always complete the Zentao step first and only then open the daily-report system.
---

# Worklog Skill

Use `playwright-cli.cmd`, not `playwright-cli`, in PowerShell on this machine. The `.ps1` shim is blocked by execution policy, while `playwright-cli.cmd` works.

Use dedicated sessions so both systems can stay open together:

- `maxlogin` for `http://172.16.3.197/max`
- `report152` for `http://172.16.4.152/login`

Open live systems with `--headed --persistent`.

## Required Order For Daily Report Requests

When the user asks to `填写日报`, `填日报`, `写日报`, or otherwise complete the daily-report workflow, the order is mandatory:

1. Open Zentao at `http://172.16.3.197/max`.
2. Log in and complete the Zentao-side daily-report-related operation first.
3. Validate the Zentao operation from visible page evidence.
4. Only after the Zentao step is complete, open the daily-report system at `http://172.16.4.152/login`.
5. Log in to the daily-report system and complete the daily-report entry or confirmation flow.

Do not start with `http://172.16.4.152/login` when the request is to fill a daily report.
Do not treat the two systems as interchangeable entry points for that request.

## Quick Start

Zentao:

```powershell
playwright-cli.cmd -s=maxlogin open --headed --persistent "http://172.16.3.197/max"
playwright-cli.cmd -s=maxlogin snapshot
```

Daily report system:

```powershell
playwright-cli.cmd -s=report152 open --headed --persistent "http://172.16.4.152/login"
playwright-cli.cmd -s=report152 snapshot
```

## Workflow 1: Zentao Task Work

Target:

- site: `http://172.16.3.197/max`
- login redirects to `user-login-...html`
- success lands on `.../max/my.html`

### Login

1. Open the site with session `maxlogin`.
2. Snapshot the page.
3. Fill the visible username and password textboxes.
4. Click the login button.
5. Confirm success from URL and page title.

Observed refs on this machine during login:

- username textbox: `e17`
- password textbox: `e21`
- login button: `e29`

Example:

```powershell
playwright-cli.cmd -s=maxlogin fill e17 "pengkang"
playwright-cli.cmd -s=maxlogin fill e21 "Netinfo2025"
playwright-cli.cmd -s=maxlogin click e29
```

### Open Assigned Task List

Do not depend on dashboard clicks from the top document. The business area is inside an iframe, so top-level selectors may fail.

Reliable path:

```powershell
playwright-cli.cmd -s=maxlogin goto "http://172.16.3.197/max/my-work-task-assignedTo.html"
```

Then inspect the iframe container:

```powershell
playwright-cli.cmd -s=maxlogin snapshot e87 --depth=6
```

Important behavior:

- the main content is inside `iframe[name="app-my"]`
- clicking a task name opens a right-side detail drawer
- the task detail drawer stays on the same page

### Read The Task List

Visible task rows usually expose:

- task id
- task name
- status
- project
- execution
- assignee
- deadline
- estimate
- consumed
- left

Use focused snapshots on the iframe or the row container instead of full-page snapshots.

### Open A Task And Record Work Hours

1. Open one task from the list.
2. Read the task details before writing logs.
3. Open the work-hour form from the detail drawer.
4. Fill the first empty row unless the user asks otherwise.
5. Save and validate from visible page evidence.

Stable direct links often exist in the action area:

- task detail: `/max/task-view-<taskId>.html`
- record work hour: `/max/task-recordWorkhour-<taskId>.html`

Observed field mapping in this environment:

- work content: `#work_0`
- consumed: `#consumed_0`
- left: `#left_0`

Observed save button ref during this task flow:

- save button: `f4e698`

### Worklog Content Rules

When the user asks to fill work hours or a daily report but does not provide exact text, generate the work content yourself. The user role is an interface owner / interface developer. Center the wording on:

- interface development and integration
- iteration planning and schedule tracking
- issue follow-up and defect coordination
- delivery preparation and risk tracking
- requirement clarification and verification

Requirements:

- make each submission different
- keep it around 40-60 Chinese characters when entering content into the system
- write realistic work performed, not filler text

Good patterns:

- mention iteration or version progress
- mention interface changes, integration, or verification
- mention issue tracking or risk closure
- mention delivery nodes or schedule follow-up

### Save Validation

Never assume save worked just because the button click returned.

Confirm one of these:

- total consumed hours changed
- a submitted-log table appears
- the new log row shows your content, consumed hours, and remaining hours

Observed success signs:

- a new log id such as `176835`
- consumed displayed as `8 h`
- left displayed as `8 h`

## Workflow 2: Daily Report Confirmation System

Target:

- site: `http://172.16.4.152/login`
- success lands on `http://172.16.4.152/home-page/index`

### Login

1. Open with session `report152`.
2. Snapshot the login page.
3. Fill account and password.
4. Click login.
5. Confirm success from URL and title.

Observed refs on this machine during login:

- account textbox: `e18`
- password textbox: `e25`
- login button: `e31`

Example:

```powershell
playwright-cli.cmd -s=report152 fill e18 "pengkang"
playwright-cli.cmd -s=report152 fill e25 "888888"
playwright-cli.cmd -s=report152 click e31
```

### Open Daily Report Confirmation

After login, a top navigation item opens the daily report confirmation page. If refs are unstable, go straight to the page:

```powershell
playwright-cli.cmd -s=report152 goto "http://172.16.4.152/daily/daily-confirmation"
```

Expected page:

- URL: `http://172.16.4.152/daily/daily-confirmation`
- title matches the daily-report confirmation screen

### Read The List

The filter area usually includes:

- a date textbox, often defaulting to the current date
- a keyword textbox, often already filled with the current user

The list usually contains columns for:

- report date
- reporter
- OA project
- Zentao project
- work content
- consumed hours
- total

Possible outcome:

- no data

When the user only asks to inspect the list, report the filter values and whether rows are visible or the table is empty.

## Combined Workflow: Fill Daily Report

Use this workflow whenever the user asks to fill the daily report and does not explicitly limit the task to only one system.

1. Start in Zentao with session `maxlogin`.
2. Log in to `http://172.16.3.197/max`.
3. Navigate to the relevant Zentao page and fill the daily-report-related information there.
4. Confirm the Zentao-side write succeeded from visible page evidence.
5. Only then open the daily-report system with session `report152`.
6. Log in to `http://172.16.4.152/login`.
7. Navigate to the target daily-report page and fill the report information.
8. Confirm the daily-report-system write or submission succeeded from visible page evidence.

If the Zentao step fails or cannot be validated, stop and report that blocker instead of proceeding directly to the daily-report system.

## Pitfalls

### PowerShell Pitfalls

- `playwright-cli --version` fails because PowerShell tries to run `playwright-cli.ps1`
- `playwright-cli.cmd` works
- raw `>>>` in commands is parsed as redirection syntax and causes PowerShell errors

### Page-Structure Pitfalls

- Zentao embeds the business content inside an iframe
- opening a task may show a side drawer rather than a full navigation
- top-level CSS selectors may fail for elements that only exist inside the iframe or drawer

### Navigation Strategy

- prefer direct `goto` for stable business URLs when dashboard clicks are unreliable
- use focused snapshots on the iframe or drawer container
- after every meaningful click, verify URL, title, or changed page content

### Validation Strategy

- do not claim login success until the landing URL or title matches
- do not claim save success until the page shows submitted data or changed totals

## Default Response Pattern

When the user asks to fill a daily report, open Zentao to record work hours, inspect the report-confirmation list, or log into either internal system, do this:

1. Identify whether the request targets Zentao task work or the daily-report system.
2. If the request is to fill a daily report, always start with Zentao and complete that step first.
3. Reuse the correct session if already open. Otherwise open a new headed persistent session.
4. Log in with the credentials provided in the request.
5. Navigate to the exact target page.
6. Read the visible data first.
7. If writing content is required and wording is not provided, generate distinct interface-owner style work content.
8. Save and validate using visible evidence from the page.
9. For daily-report requests, only after the Zentao step is validated should the daily-report system be opened and operated.
