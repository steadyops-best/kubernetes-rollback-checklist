# When Pods are Ready but checkout fails after a rollout

A new Kubernetes Deployment revision can pass its readiness probe while returning errors on a customer request. This guide shows how to distinguish a revision-specific failure from a shared outage and check whether rolling back the application is safe.

This applies to a standard Deployment with old and new Pods serving together during a rolling update. Adapt the same questions to the traffic controls and rollout owner in your environment.

## Collect evidence before changing the rollout

First establish which rollout, cluster and customer flow are affected. Freeze further promotion using the controls in your deployment system. Keep the last known good revision identified by image or digest, and check which revision actually handled the failed request. Use trace metadata or application logs if your telemetry does not expose the revision directly.

These commands read the deployed revision history, workload state and Service routing. Replace the placeholders with approved values for the affected environment.

```sh
kubectl --context CONTEXT -n NAMESPACE rollout history deployment/APP
kubectl --context CONTEXT -n NAMESPACE get pods -l app=APP \
  -o custom-columns='POD:.metadata.name,HASH:.metadata.labels.pod-template-hash,CONTAINER_READY:.status.containerStatuses[*].ready'
kubectl --context CONTEXT -n NAMESPACE get endpointslices \
  -l kubernetes.io/service-name=SERVICE
```

Use the Deployment's actual label selector if it differs from `app=APP`. Match the EndpointSlice targets to Pods and compare this view with ingress or load-balancer telemetry. Readiness can make a Pod eligible for Service traffic even when a path outside the probe fails. [Kubernetes probes documentation](https://kubernetes.io/docs/concepts/workloads/pods/probes/)

For repeatable evidence, use the repository's [read-only collector](../USAGE.md). Store any captured deployment configuration and logs in your restricted release record.

## Choose hold, rollback, or repair

| What the evidence shows | Decision |
|---|---|
| Checkout fails on the new revision while the old revision and dependencies still work | Prepare a rollback after verifying compatibility with current data and messages. |
| Both revisions fail against the same shared dependency | Hold the release and investigate the dependency. Replacing the application may leave the fault in place. |
| The new revision has produced data or jobs the old revision cannot handle | Hold and use the agreed containment plan, such as disabling the affected feature or directing writes to a compatible path. |
| The samples cannot identify the failing revision | Hold promotion. Gather per-revision samples and repeat the customer check before choosing a recovery action. |

Confirm compatibility for database migrations, feature flags, configuration and queue payloads. Check that the previous image can still be pulled and that a GitOps controller or release pipeline will not immediately reapply the failing revision. A Deployment rollback restores the previous Pod template. Treat shared runtime state and release changes outside that template as separate actions. [Kubernetes Deployment rollback documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)

## Worked example

During a hypothetical checkout rollout, revision 42 succeeds on 50 of 50 synthetic checkout requests. Revision 43 serves only 21 of 30, although every Pod is Ready. Traces show the failures are confined to the new image. Both revisions can read the current database, the rollout has not enabled the new queue payload, and the previous image is still available.

The release owner records these observations, stops the rollout through the release controller, and restores revision 42. After the transition, the team verifies that new requests go to the restored revision, tracks any in-flight connections, and repeats checkout all the way to confirmation. Only then does it mark the customer path recovered. The counts describe a small exercise sample and are not thresholds for another service.

Record the trigger, approved target, compatibility decision, traffic after reversal, and customer result in the [rollback evidence record](../rollback-evidence-template.md). Use the [repository checklist](../checklist.md) for execution and the [SteadyOps rollback guide](https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/) for other rollout controllers.
