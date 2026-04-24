# Refactor Checklists

## Legacy Inventory

- Entry points: web routes, CLI commands, jobs, callbacks, message consumers.
- Data: tables, migrations, raw SQL, ORM models, cache keys, file storage.
- Integrations: payment, auth, email, SMS, ERP, CRM, third-party APIs.
- Runtime: config, env vars, feature flags, deployment scripts.
- Business logic: validations, state machines, status fields, permissions, pricing, discounts, inventory, settlement.

## Risk Signals

- Code with many conditions and no tests.
- Magic numbers, status codes, feature flags, hardcoded customer IDs.
- Hidden side effects such as sending messages, changing balances, writing audit logs.
- Shared database tables used by many modules.
- Behavior controlled by dates, regions, roles, or customer-specific branches.

## Protection Net

- Golden-master tests for current outputs.
- API contract tests for public endpoints.
- Database before/after assertions.
- Idempotency and retry tests for jobs.
- Log comparison between old and new paths.
- Feature flag and rollback path.

## Migration Priority

Start with modules that are low-risk and easy to observe. Avoid starting with payment, settlement, permissions, inventory, or core order state transitions unless there is an urgent business reason.