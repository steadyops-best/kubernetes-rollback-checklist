# Contributing

Contributions should make the checklist safer, clearer, or easier to validate in a real production environment.

## Good contributions

- Correct a Kubernetes, Helm, or Argo Rollouts command.
- Add a missing precondition, stop condition, or validation step.
- Clarify database, queue, traffic, probe, or graceful-shutdown compatibility.
- Add a failure mode that changes the rollback decision.
- Improve placeholders so examples are reusable without exposing private data.
- Link to primary Kubernetes, Helm, Argo, or other relevant vendor documentation.

## Avoid

- Environment-specific secrets, hostnames, tokens, customer data, or private topology.
- Destructive commands without warnings and stop conditions.
- Fixed thresholds presented as universal production values.
- Vendor promotion, copied marketing text, or unrelated SEO links.
- Claims about availability, performance, or recovery that are not supported by a reproducible validation method.
- Replacing a concise operational checklist with a long policy document.

## Change format

A useful change should explain:

1. the failure mode or operational gap;
2. the proposed checklist or command change;
3. when it applies;
4. how an engineer validates the result;
5. any compatibility or rollback risk.

Keep examples conservative. Use placeholders such as `APP`, `NAMESPACE`, `RELEASE`, and `REVISION` rather than real production identifiers.

## Source and canonical guide

The reusable checklist lives in this repository. The maintained explanatory guide is:

https://steadyops.best/articles/kubernetes-rollback-checklist-for-production-deployments/

Changes that materially alter the operating model should keep the repository and canonical guide consistent.