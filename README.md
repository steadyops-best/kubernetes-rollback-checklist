# Kubernetes Rollback Checklist

A forkable production rollback package for Kubernetes, Helm, and Argo Rollouts. It helps teams decide **when** to stop a release, **whether** rollback is safe, **who** owns the decision, and **how** to prove that customer-facing service has recovered.

- Canonical implementation guide: https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/
- Kubernetes production-readiness guide: https://steadyops.best/articles/kubernetes-production-readiness-checklist/
- SteadyOps resource library: https://steadyops.best/resources/
- License: MIT
- Artifact version: 1.0.0
- Repository reviewed: 2026-07-12

## Why this repository exists

`kubectl rollout undo` is a command, not a recovery strategy. A safe rollback also depends on:

- a known previous image, chart, or rollout revision;
- backward-compatible database and message changes;
- readiness that represents real serving ability;
- traffic no longer reaching failed or terminating pods;
- observable error, latency, saturation, queue, and database signals;
- a named deployment owner and rollback owner;
- a technical smoke test plus a real business transaction;
- retained release and incident evidence.

This repository keeps the reusable artifact separate from the longer explanatory article so teams can fork it, version it, cite it, and adapt it to their own release process.

## Start here

1. Open [`checklist.md`](checklist.md).
2. Copy it into the release repository, change ticket, runbook system, or internal documentation space.
3. Replace `APP`, `RELEASE`, namespaces, owners, thresholds, and business-flow checks.
4. Confirm database migration compatibility before relying on application rollback.
5. Test pause, rollback, traffic removal, and validation in stage or another production-like environment.
6. Complete [`rollback-evidence-template.md`](rollback-evidence-template.md) after an exercise or production rollback.
7. Store the completed checklist and evidence record with the deployment or incident evidence.

## Repository contents

| File | Purpose |
|---|---|
| [`checklist.md`](checklist.md) | Compact release and rollback checklist with Kubernetes, Helm, and Argo Rollouts commands. |
| [`rollback-evidence-template.md`](rollback-evidence-template.md) | Timestamped decision, compatibility, command, signal, customer-flow, and follow-up record. |
| [`CITATION.cff`](CITATION.cff) | Citation metadata for internal standards, research notes, and derived runbooks. |
| [`LICENSE`](LICENSE) | MIT license for reuse and adaptation. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Rules for safe, practical improvements. |

## Rollback decision model

A rollback decision should answer four questions in order:

### 1. Is there material impact?

Examples include sustained 5xx errors, unacceptable p95/p99 latency, broken login or checkout, growing queue backlog, database saturation, repeated pod failure, or a rollout that cannot complete inside the agreed decision window.

### 2. Is the previous version safe to run now?

Confirm that the artifact still exists and that the current database schema, feature flags, queue messages, secrets, and external contracts remain compatible.

### 3. Can traffic be removed from the bad version?

Readiness, Service endpoints, ingress or load-balancer health, connection draining, and progressive-delivery state must agree. A pod being alive does not mean it should receive traffic.

### 4. How will recovery be proven?

Validate both technical signals and the critical customer journey. A green rollout status alone is not recovery evidence.

## Minimum evidence to retain

- release version, image digest, chart or rollout revision;
- deployment and rollback owners;
- trigger metric and decision timestamp;
- commands executed and their results;
- database migration compatibility decision;
- traffic and endpoint state;
- error, latency, saturation, queue, and database observations;
- customer-facing transaction result;
- follow-up actions with owners and deadlines.

## Safety boundaries

This project is a starting point, not an automated production action.

- Review every command before execution.
- Never roll back application code across an incompatible destructive migration.
- Preserve incident evidence before deleting failed pods or changing infrastructure aggressively.
- Do not retry non-idempotent requests blindly during partial failure.
- Confirm that the rollback target has not been removed from the registry.
- Use environment-specific thresholds derived from real baselines and SLOs.
- Keep secrets, private topology, customer data, and internal endpoints out of public forks.

## Related SteadyOps resources

- Zero-downtime deployment checklist: https://github.com/steadyops-best/zero-downtime-deployment-checklist
- Disaster recovery runbook template: https://github.com/steadyops-best/disaster-recovery-runbook-template
- Kubernetes observability for SRE teams: https://steadyops.best/articles/kubernetes-observability-best-practices-for-sre-teams/
- Zero-downtime Blue/Green deployments: https://steadyops.best/articles/zero-downtime-bluegreen-deployments/
- Production reliability cases: https://steadyops.best/reliability-cases/

## Citation

GitHub can render the repository citation from [`CITATION.cff`](CITATION.cff). When adapting the checklist internally, retain a reference to the source repository and the canonical implementation guide so future maintainers can review changes and context.

## Contributing

Corrections and practical additions are welcome when they explain the failure mode, preserve safe placeholders, include validation, and avoid vendor marketing or unsupported claims. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT. Use, adapt, and improve the checklist for your own Kubernetes release process. Production use remains the responsibility of the team applying it.