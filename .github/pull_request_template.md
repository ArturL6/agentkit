## Outcome

<!-- What owner-authorized outcome does this PR deliver? -->

## Scope and authorization

- Task/issue/work packet:
- Owner implementation authorization:
- Explicitly out of scope:

## Architecture and decisions

- Relevant `ARCHITECTURE.md` sections:
- Relevant ADRs:
- New or updated ADR (if structural semantics changed):
- Target-state machinery added? If yes, identify the evidence gate and proof:

## Changes

<!-- Concise list of concrete code/document/test changes. -->

## Public API and dependency impact

- Public exports/contracts changed:
- `RuntimeSpec` or configuration changed:
- Framework/provider imports and containment:
- Packaging/dependency changes:

## Tool invocation and security

- Can this change execute tools? If yes, show that every path crosses kernel-owned `ToolInvoker`:
- Authorization/approval/audit ordering impact:
- Principal, secret, redaction, or artifact handling impact:
- New trust boundary or fail-open/fail-closed behavior:

## Lifecycle, concurrency, streaming, and cancellation

- Resources/tasks created and their owner:
- Acquisition-failure unwind:
- Shutdown bound and cleanup behavior:
- Stream bounds/backpressure/abandonment behavior:
- Cancellation propagation and single terminal-outcome proof:

<!-- Do not describe resource cleanup as deterministic reversibility unless that stronger claim is actually proven. -->

## Sessions and framework checkpoints

- Session records/schema changed:
- Retention/privacy/migration impact:
- Framework checkpoint impact:
- Does any claim imply event sourcing, cross-framework replay, or loop replaceability? What evidence supports it?

## Verification

<!-- Exact commands and results. Mark unrun checks explicitly. -->

- [ ] Focused tests:
- [ ] Full test suite:
- [ ] Formatting/lint/type/architecture checks:
- [ ] Package build and metadata checks:
- [ ] Clean-wheel external consumer test:
- [ ] Cancellation/resource-cleanup tests:
- [ ] `git diff --check`:

## Evidence and limitations

<!-- Distinguish unit/API proof, clean-wheel proof, live-provider proof, and unverified claims. -->

## Risks and rollback

- Compatibility/migration risk:
- Security/data/lifecycle risk:
- Rollback or disable path:

## Independent reviewer focus

<!-- Name 2–4 concrete areas for scrutiny. The author must not approve or merge their own PR. -->
