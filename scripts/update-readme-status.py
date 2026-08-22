#!/usr/bin/env python3
"""Update README.md with the current Pier job status."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import statistics


START_MARKER = "<!-- benchmark-status:start -->"
END_MARKER = "<!-- benchmark-status:end -->"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def active_phase(trial_dir: Path) -> str:
    if (trial_dir / "verifier" / "reward.json").exists():
        return "finalizing verifier"
    if (trial_dir / "artifacts" / "model.patch").exists():
        return "verifier"
    if (trial_dir / "agent" / "opencode.txt").exists():
        return "agent execution"
    return "environment build"


def render(job_dir: Path) -> str:
    aggregate = load_json(job_dir / "result.json")
    stats = aggregate["stats"]
    completed = []
    active = []

    for trial_dir in sorted(path for path in job_dir.iterdir() if path.is_dir()):
        result_path = trial_dir / "result.json"
        if not result_path.exists():
            active.append(trial_dir)
            continue
        result = load_json(result_path)
        if result.get("finished_at"):
            completed.append(result)
        else:
            active.append(trial_dir)

    rewards = [
        result.get("verifier_result", {}).get("rewards", {})
        for result in completed
    ]
    binary_solves = sum(reward.get("reward") == 1 for reward in rewards)
    partials = [reward["partial"] for reward in rewards if reward.get("partial") is not None]
    partial_mean = statistics.fmean(partials) if partials else None
    active_name = active[0].name.split("__", 1)[0] if active else "none"
    phase = active_phase(active[0]) if active else "complete"
    updated = datetime.now().astimezone().isoformat(timespec="seconds")

    rows = [
        START_MARKER,
        "### Live benchmark status",
        "",
        f"_Updated: `{updated}`_",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Completed | {stats['n_completed_trials']} / {aggregate['n_total_trials']} |",
        f"| Running | {stats['n_running_trials']} |",
        f"| Pending | {stats['n_pending_trials']} |",
        f"| Errors | {stats['n_errored_trials']} |",
        f"| Retries | {stats['n_retries']} |",
        f"| Binary solves | {binary_solves} / {len(completed)} |",
        f"| Mean partial score | {partial_mean:.6f} |" if partial_mean is not None else "| Mean partial score | n/a |",
        f"| Active task | `{active_name}` |",
        f"| Active phase | {phase} |",
        END_MARKER,
    ]
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    args = parser.parse_args()

    readme = args.readme.read_text()
    start = readme.index(START_MARKER)
    end = readme.index(END_MARKER, start) + len(END_MARKER)
    updated = readme[:start] + render(args.job_dir) + readme[end:]
    args.readme.write_text(updated)


if __name__ == "__main__":
    main()
