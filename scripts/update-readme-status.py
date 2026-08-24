#!/usr/bin/env python3
"""Update README.md with the current Pier job status."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path


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


def verifier_rewards(result: dict) -> dict:
    """Return verifier rewards, including for trials that ended before scoring."""
    verifier_result = result.get("verifier_result")
    if not isinstance(verifier_result, dict):
        return {}
    rewards = verifier_result.get("rewards")
    return rewards if isinstance(rewards, dict) else {}


def audited_rewards(trial_dir: Path) -> dict:
    """Return a separately recorded correction for a verified harness artifact."""
    path = trial_dir / "audited-result.json"
    if not path.exists():
        return {}
    audited = load_json(path).get("audited_result")
    if not isinstance(audited, dict):
        return {}
    rewards = audited.get("rewards")
    return rewards if isinstance(rewards, dict) else {}


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
            completed.append((trial_dir, result))
        else:
            active.append(trial_dir)

    rewards = [verifier_rewards(result) for _, result in completed]
    binary_solves = sum(reward.get("reward") == 1 for reward in rewards)
    effective_rewards = [
        audited_rewards(trial_dir) or verifier_rewards(result)
        for trial_dir, result in completed
    ]
    audited_binary_solves = sum(
        reward.get("reward") == 1 for reward in effective_rewards
    )
    audited_partials = [
        reward["partial"]
        for reward in effective_rewards
        if isinstance(reward.get("partial"), (int, float))
    ]
    audited_partial_mean = (
        sum(audited_partials) / len(completed) if completed else None
    )
    evals = stats.get("evals", {})
    eval_metrics = next(iter(evals.values()), {}).get("metrics", [])
    aggregate_metrics = eval_metrics[0] if eval_metrics else {}
    partial_mean = aggregate_metrics.get("partial")
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
        f"| Audited binary solves | {audited_binary_solves} / {len(completed)} |",
        f"| Audited mean partial score | {audited_partial_mean:.6f} |" if audited_partial_mean is not None else "| Audited mean partial score | n/a |",
        f"| Active task | `{active_name}` |",
        f"| Active phase | {phase} |",
        "",
        "#### Completed task scores",
        "",
        "| Task | Outcome | Reward | Partial | Feature tests | Regression tests |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for trial_dir, result in sorted(completed, key=lambda item: item[1]["finished_at"]):
        reward = verifier_rewards(result)
        audit_reward = audited_rewards(trial_dir)
        if audit_reward:
            reward = audit_reward
        task_name = result.get("task_name", trial_dir.name).removeprefix("datacurve/")
        result_link = f"benchmark-results/{job_dir.name}/{trial_dir.name}/result.json"
        if result.get("exception_info") and not reward:
            solved = "⚠️ error"
        else:
            solved = "✅ solved" if reward.get("reward") == 1 else "❌ not solved"
        if audit_reward:
            audit_link = (
                f"benchmark-results/{job_dir.name}/{trial_dir.name}/audited-result.json"
            )
            solved += f" ([audited]({audit_link}))"
        partial = reward.get("partial")
        partial_text = f"{partial:.6f}" if partial is not None else "n/a"
        f2p = f"{reward.get('f2p_passed', 'n/a')}/{reward.get('f2p_total', 'n/a')}"
        p2p = f"{reward.get('p2p_passed', 'n/a')}/{reward.get('p2p_total', 'n/a')}"
        rows.append(
            f"| [`{task_name}`]({result_link}) | {solved} | "
            f"{reward.get('reward', 'n/a')} | {partial_text} | {f2p} | {p2p} |"
        )

    if audited_binary_solves != binary_solves or audited_partial_mean != partial_mean:
        rows.extend(
            [
                "",
                "_Audited values replace only independently reproduced harness-invalid results; canonical Pier artifacts and raw scores remain unchanged._",
            ]
        )

    if not completed:
        rows.append("| _No completed tasks yet_ | — | — | — | — | — |")

    rows.append(END_MARKER)
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
