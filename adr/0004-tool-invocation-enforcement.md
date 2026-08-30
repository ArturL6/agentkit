# ADR-0004: Kernel-owned tool invocation enforcement

## Status

Superseded by the consolidated v1 ADR set and product backlog. See `README.md` in this directory for the decision-by-decision replacement map.

## Context

Tool execution is a security and correctness boundary. If loops, framework wrappers, tools, or optional policy plugins can invoke tool implementations directly, approvals, authorization, schema validation, identity propagation, timeouts, cancellation, redaction, and audit can be bypassed. A generic hook convention does not make enforcement unavoidable.

Installed Python remains trusted in-process code, so AgentKit cannot prevent a malicious package from directly calling the network or filesystem. It can and must make the conforming AgentKit tool path structurally singular.

## Decision

The application/kernel owns a `ToolInvoker`, and every AgentKit-managed tool execution routes through it.

The loop or framework adapter receives tool descriptions plus a kernel-owned invocation callback, never raw executable tool callables. `ToolInvoker` owns the execution sequence:

1. resolve the registered tool specification;
2. validate input schema and configured limits;
3. propagate run/session/tool-call identity, principal, deadline, and cancellation;
4. obtain the required policy or approval decision;
5. record required pre-execution audit state;
6. execute under timeout/cancellation control;
7. normalize and redact output or error;
8. record the terminal audit state;
9. return a framework-neutral result.

Policy and audit implementations may be injected behind narrow contracts, but the decision points and order are kernel-owned. Security-required checks fail closed according to explicit policy. No generic hook bus may create an alternate tool execution path.

The design does not claim automatic idempotency or exactly-once external effects. Those require tool-specific contracts and durable coordination.

## Alternatives considered

### Framework-native tool execution

Rejected. It lets an agent framework own policy and audit ordering and makes behavior differ across adapters.

### Optional authorization/audit hooks

Rejected as the enforcement mechanism. Optional or reorderable hooks can be omitted or bypassed.

### Tool wrappers supplied by each provider

Rejected as the primary boundary. Distributed wrappers duplicate security logic and cannot prove every path is covered.

### Sandbox every tool in v1

Rejected as a universal requirement. Sandboxing may later be an execution adapter/capability, but it does not replace the kernel invocation gateway.

## Consequences

Positive:

- one call site enforces validation, policy, identity, timeout, cancellation, and audit;
- native and LangGraph loops have consistent tool semantics;
- security tests can prove path coverage;
- tool implementations remain framework-neutral.

Negative:

- all loop adapters must use the gateway and translation layer;
- the gateway is security-sensitive kernel code requiring careful review;
- external side-effect atomicity and idempotency remain explicit unsolved concerns unless a tool implements them.

## Compatibility

Tool contracts expose descriptions/specifications and an implementation interface consumed only by `ToolInvoker`. Public or adapter APIs must not expose a raw callable path that bypasses the gateway. Changes to enforcement order or fail-open/fail-closed behavior require an ADR and migration review.

## Verification

- Tests fail if a loop can access or execute a raw tool callable.
- Native and LangGraph adapter tests assert each call traverses `ToolInvoker` exactly once.
- Invalid input and denied approval prevent implementation execution.
- Required audit failure follows documented fail-closed behavior.
- Timeout and cancellation stop/join owned tool tasks and produce one terminal result.
- Identity and call IDs survive request, audit, implementation, and result translation.
- Error/result redaction occurs before persistence and public streaming.

## Supersedes / superseded by

Supersedes optional policy-hook enforcement for tool execution.
