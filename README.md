# Kubernetes Rollback Checklist

A practical Kubernetes rollback checklist for production deployments.

Use it when a rollout creates customer impact, error rates increase, p99 latency degrades, pods crash, queues grow, or the deployment cannot be validated within the agreed window.

## What this checklist is for

Kubernetes makes rollback commands available, but it does not decide whether rollback is safe. A production rollback still needs context:

- what changed
- which revision is healthy
- whether database migrations are compatible
- whether old and new pods can coexist
- whether traffic is still routed to bad pods
- which metrics decide rollback success

## Before you roll back

Do not start with `kubectl rollout undo` until these checks are clear.

```md
## Kubernetes rollback readiness

Service:
Namespace:
Deployment:
Current revision:
Candidate rollback revision:
Deployment owner:
Rollback owner:
Incident channel:

### Impact
- [ ] Customer-facing impact is confirmed.
- [ ] Error rate, p95/p99 latency and request rate are visible.
- [ ] Queue depth and background worker status are visible.
- [ ] Database connection pressure is visible.
- [ ] Recent deployment or config change is identified.

### Safety
- [ ] Previous image or Helm revision exists.
- [ ] Previous version can run with the current database schema.
- [ ] Feature flags or config changes are compatible.
- [ ] No irreversible migration is still running.
- [ ] Rollback owner is available.
- [ ] Validation path is defined.

### Routing
- [ ] Readiness checks are working.
- [ ] Failing pods are not receiving traffic.
- [ ] Ingress or service endpoints point to healthy pods after rollback.
- [ ] HorizontalPodAutoscaler behavior is understood.
- [ ] PodDisruptionBudget will not block recovery.
```

## Rollback decision criteria

Rollback if one or more conditions are true:

- 5xx error rate exceeds the agreed threshold.
- p99 latency is more than 2x normal baseline.
- Pods are in CrashLoopBackOff and cannot recover quickly.
- Queue depth grows and does not drain.
- Database connections saturate after the release.
- A critical user flow is broken.
- Authentication or authorization is broken.
- The rollout cannot finish within the rollback decision window.

## Kubernetes commands

Set variables first:

```bash
NS=production
DEPLOYMENT=my-service
```

Inspect rollout:

```bash
kubectl -n "$NS" rollout status deployment/"$DEPLOYMENT"
kubectl -n "$NS" rollout history deployment/"$DEPLOYMENT"
kubectl -n "$NS" describe deployment "$DEPLOYMENT"
kubectl -n "$NS" get pods -l app="$DEPLOYMENT" -o wide
```

Pause a rollout while investigating:

```bash
kubectl -n "$NS" rollout pause deployment/"$DEPLOYMENT"
```

Rollback to the previous revision:

```bash
kubectl -n "$NS" rollout undo deployment/"$DEPLOYMENT"
kubectl -n "$NS" rollout status deployment/"$DEPLOYMENT"
```

Rollback to a specific revision:

```bash
kubectl -n "$NS" rollout undo deployment/"$DEPLOYMENT" --to-revision=3
kubectl -n "$NS" rollout status deployment/"$DEPLOYMENT"
```

Resume rollout if rollback is not needed:

```bash
kubectl -n "$NS" rollout resume deployment/"$DEPLOYMENT"
```

## Helm rollback

```bash
NS=production
RELEASE=my-release

helm -n "$NS" history "$RELEASE"
helm -n "$NS" rollback "$RELEASE" 12
kubectl -n "$NS" get pods -w
```

## Argo Rollouts

```bash
NS=production
ROLLOUT=my-service

kubectl argo rollouts -n "$NS" get rollout "$ROLLOUT"
kubectl argo rollouts -n "$NS" abort "$ROLLOUT"
kubectl argo rollouts -n "$NS" promote "$ROLLOUT"
```

## Validate after rollback

- [ ] Service returns HTTP 200 on health and customer-facing endpoints.
- [ ] Error rate returns to baseline.
- [ ] p99 latency returns to acceptable range.
- [ ] Pod restarts stop increasing.
- [ ] Queue depth drains.
- [ ] Database connections stabilize.
- [ ] Logs do not show the original failure.
- [ ] Ingress or service endpoints point to healthy pods.
- [ ] Main user flow works.
- [ ] Monitoring remains normal for at least 10-15 minutes.

## Common rollback mistakes

- Rolling back app code while keeping an incompatible database migration.
- Assuming the previous image still exists in the registry.
- Rolling back before pausing a broken progressive rollout.
- Ignoring background workers and async queues.
- Treating readiness probes as proof that business flows work.
- Letting the load balancer keep traffic on terminating or failed pods.
- Not documenting the rollback revision and reason.

## Post-incident notes

Record:

- bad version
- rollback version
- trigger metric
- customer impact
- command used
- validation result
- follow-up task owner
- what should be automated before the next release

## SteadyOps resources

- Website: https://steadyops.best/
- DevOps/SRE articles: https://steadyops.best/articles/
- LinkedIn: https://www.linkedin.com/in/yuri-osipov-0876b0254
- Related article: https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/
- Zero-downtime deployments: https://steadyops.best/articles/zero-downtime-bluegreen-deployments/
- Kubernetes production readiness: https://steadyops.best/articles/kubernetes-production-readiness/

## Related public checklists

- Zero-downtime deployment checklist: https://github.com/steadyops-best/zero-downtime-deployment-checklist
- Disaster recovery runbook template: https://github.com/steadyops-best/disaster-recovery-runbook-template

## License

MIT License. Use, adapt and improve this checklist for your own Kubernetes deployment process.
