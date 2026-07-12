# Kubernetes Rollback Evidence Record

Version: 1.0.0  
Canonical guide: https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/

Use this record after a rollback exercise or production rollback. Store the completed copy with the release or incident evidence.

## Release identity

- Service:
- Environment:
- Namespace:
- Workload or rollout:
- Failed version/image digest:
- Restored version/image digest:
- Helm revision or rollout revision:
- Deployment owner:
- Rollback owner:
- Incident or release ticket:

## Impact and decision

- Detection time (UTC):
- Customer impact:
- Trigger signal:
- Baseline and observed value:
- Rollback decision time (UTC):
- Decision owner:
- Alternatives considered:
- Reason rollback was selected:
- Stop conditions checked:

## Compatibility decision

| Area | Compatible? | Evidence or notes |
|---|---|---|
| Database schema | | |
| Queue/message format | | |
| API contract | | |
| Feature flags/config | | |
| Cache/session data | | |
| Secrets and credentials | | |

## Commands and actions

| UTC time | Owner | Command or action | Expected result | Actual result | Evidence link |
|---|---|---|---|---|---|
| | | | | | |

## Traffic and workload validation

- [ ] Failed pods or ReplicaSets no longer receive traffic.
- [ ] Intended revision is active.
- [ ] Readiness and endpoints are healthy.
- [ ] Ingress/load balancer routing is correct.
- [ ] Connection draining completed as expected.
- [ ] Pod restarts are stable.
- [ ] Queue consumers and background workers are compatible.

## Production-signal validation

| Signal | Before rollback | After rollback | Baseline/target | Result |
|---|---|---|---|---|
| Error rate | | | | |
| p95 latency | | | | |
| p99 latency | | | | |
| Request rate | | | | |
| Pod restarts | | | | |
| Queue depth | | | | |
| Database connections/locks | | | | |

## Customer-flow validation

- Critical transaction:
- Test owner:
- Test time (UTC):
- Result:
- Evidence:

## Outcome

- Technical recovery time:
- Customer recovery time:
- Data loss or inconsistency:
- Rollback successful: yes/no/partial
- Remaining risk:
- Monitoring window completed:

## Follow-up actions

| Action | Risk addressed | Owner | Deadline | Verification |
|---|---|---|---|---|
| | | | | |

## Review

- Record reviewed by:
- Review date:
- Checklist/runbook update required:
- Next rollback exercise: