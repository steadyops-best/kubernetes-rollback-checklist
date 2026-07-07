# Kubernetes Rollback Checklist

A practical Kubernetes rollback checklist for production deployments.

Created by SteadyOps: https://steadyops.best/

Related article:  
https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/

## Checklist

- Confirm the failing deployment revision
- Check 5xx error rate, p99 latency, queue depth and database connections
- Pause rollout if blast radius is unclear
- Run `kubectl rollout status`
- Roll back with `kubectl rollout undo`
- Validate health checks and customer-facing endpoints
- Document the incident and follow-up actions
