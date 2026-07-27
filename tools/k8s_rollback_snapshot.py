#!/usr/bin/env python3
"""Collect read-only Kubernetes rollout evidence into Markdown."""
from __future__ import annotations
import argparse, datetime as dt, pathlib, shlex, subprocess


def build_commands(namespace: str, deployment: str) -> list[list[str]]:
    resource = f"deployment/{deployment}"
    return [
        ["kubectl", "auth", "can-i", "get", "deployments", "-n", namespace],
        ["kubectl", "rollout", "status", resource, "-n", namespace, "--timeout=10s"],
        ["kubectl", "rollout", "history", resource, "-n", namespace],
        ["kubectl", "get", resource, "-n", namespace, "-o", "yaml"],
        ["kubectl", "get", "pods", "-n", namespace, "-l", f"app={deployment}", "-o", "wide"],
        ["kubectl", "get", "endpoints", "-n", namespace, "-o", "wide"],
        ["kubectl", "get", "events", "-n", namespace, "--sort-by=.metadata.creationTimestamp"],
    ]


def execute(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, text=True, capture_output=True, timeout=60, check=False)
    output = (result.stdout + ("\n" + result.stderr if result.stderr else "")).strip()
    return result.returncode, output


def collect(namespace: str, deployment: str) -> str:
    created = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    parts = ["# Kubernetes Rollback Evidence Snapshot", "", f"- Namespace: `{namespace}`", f"- Deployment: `{deployment}`", f"- Collected: `{created}`", "", "> Read-only evidence only. This tool never pauses, rolls back, deletes, or mutates resources.", ""]
    for command in build_commands(namespace, deployment):
        code, output = execute(command)
        parts += [f"## `{shlex.join(command)}`", "", f"Exit code: `{code}`", "", "```text", output or "(no output)", "```", ""]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--deployment", required=True)
    parser.add_argument("--output", default="rollback-evidence.md")
    args = parser.parse_args()
    output = pathlib.Path(args.output)
    output.write_text(collect(args.namespace, args.deployment), encoding="utf-8")
    print(output)
    return 0

if __name__ == "__main__": raise SystemExit(main())
