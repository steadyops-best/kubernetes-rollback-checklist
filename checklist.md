# Kubernetes Rollback Checklist

Version: 1.0.0
Last reviewed: 2026-07-10

Implementation guide: https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/

## Before release

- [ ] Previous image digest or chart revision is known and available.
- [ ] Database migration is backward-compatible.
- [ ] Rollout history is visible.
- [ ] Readiness represents real serving ability.
- [ ] Error, latency, saturation, queue, and business signals are visible.
- [ ] Pause and rollback owner is named.
- [ ] Stop conditions are agreed.

## Pause and inspect

```bash
kubectl rollout pause deployment/APP -n production
kubectl rollout status deployment/APP -n production
kubectl rollout history deployment/APP -n production
kubectl get pods -n production -l app=APP -o wide
kubectl get events -n production --sort-by=.metadata.creationTimestamp | tail -50
```

## Roll back

```bash
kubectl rollout undo deployment/APP -n production
kubectl rollout status deployment/APP -n production
```

Helm:

```bash
helm history RELEASE -n production
helm rollback RELEASE REVISION -n production
```

Argo Rollouts:

```bash
kubectl argo rollouts get rollout APP -n production
kubectl argo rollouts abort APP -n production
```

## Post-rollback validation

- [ ] Customer-facing transaction succeeds.
- [ ] Error rate and p95/p99 latency return to baseline.
- [ ] Pods are Ready and stable.
- [ ] Database connections, locks, and queue depth are stable.
- [ ] Background workers process safely.
- [ ] Backup, monitoring, and alert delivery remain healthy.
- [ ] Incident timeline and follow-up actions are recorded.
