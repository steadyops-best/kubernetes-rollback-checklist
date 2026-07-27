# Tested rollback evidence collector

`tools/k8s_rollback_snapshot.py` creates a timestamped Markdown evidence bundle before a rollback decision or during a rollback exercise.

It is deliberately read-only. The command set contains no `rollout undo`, `pause`, `delete`, `patch`, or `apply` operation.

## Requirements

- Python 3.10+
- `kubectl` configured for the intended cluster
- read access to Deployments, Pods, Endpoints, and Events in the namespace

## Run

```bash
python tools/k8s_rollback_snapshot.py \
  --namespace production \
  --deployment payments-api \
  --output rollback-evidence.md
```

Review the generated report together with `checklist.md` and complete `rollback-evidence-template.md` when a rollback is actually executed.

## What it captures

- authorization check;
- rollout status and revision history;
- Deployment YAML;
- matching Pods;
- namespace Endpoints;
- recent namespace Events;
- command exit codes and output.

## Validation and releases

Pull requests run Python compilation, unit tests, and a CLI smoke check. Tags matching `v*` create a GitHub Release containing the checklist, evidence templates, tested utility, and SHA-256 checksum.

The collector does not prove rollback safety by itself. Database migrations, messages, secrets, traffic routing, and the customer-facing transaction still require human validation.
