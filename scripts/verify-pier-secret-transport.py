#!/usr/bin/env python3
"""Regression check for Pier's Docker env transport and pinned OpenCode config."""

from __future__ import annotations

import asyncio
import importlib.util
import inspect
import os
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace


if importlib.util.find_spec("pier") is None:
    pier_executable = shutil.which("pier")
    if not pier_executable:
        raise SystemExit("pier is not installed or is not on PATH")
    shebang = Path(pier_executable).read_text().splitlines()[0]
    if not shebang.startswith("#!"):
        raise SystemExit(f"cannot determine Pier's Python from {pier_executable}")
    os.execv(shebang[2:], [shebang[2:], __file__, *sys.argv[1:]])

import yaml

from pier.environments.docker.docker import DockerEnvironment
from pier.models.job.config import JobConfig
from pier.models.job.lock import sanitize_cli_invocation
from pier.models.trial.config import AgentConfig


SENTINEL = "pier-regression-secret-value"
WORKSPACE = Path(__file__).resolve().parent.parent
CONFIG_PATHS = (
    WORKSPACE / "pier-opencode-canary.yaml",
    WORKSPACE / "pier-opencode-full-suite.yaml",
)


async def verify_exec_transport() -> None:
    captured: dict[str, object] = {}

    async def capture(command, **kwargs):
        captured["command"] = command
        captured.update(kwargs)
        return SimpleNamespace(return_code=0, stdout="", stderr=None)

    fake_environment = SimpleNamespace(
        _resolve_user=lambda user: user,
        _merge_env=lambda env: env,
        task_env_config=SimpleNamespace(workdir=None),
        _platform=SimpleNamespace(exec_shell_args=lambda command: ["bash", "-c", command]),
        _run_docker_compose_command=capture,
    )

    await DockerEnvironment.exec(
        fake_environment,
        "true",
        env={"OPENCODE_API_KEY": SENTINEL},
    )

    command = captured["command"]
    assert isinstance(command, list)
    assert SENTINEL not in command
    assert "OPENCODE_API_KEY" in command
    assert not any("OPENCODE_API_KEY=" in arg for arg in command)
    assert captured["process_env"] == {"OPENCODE_API_KEY": SENTINEL}

    source = inspect.getsource(DockerEnvironment.exec)
    assert 'f"{key}={value}"' not in source


def verify_persisted_metadata_redaction() -> None:
    invocation = sanitize_cli_invocation(
        ["pier", "run", "--agent-env", f"OPENCODE_API_KEY={SENTINEL}"]
    )
    assert SENTINEL not in invocation

    serialized = AgentConfig(
        name="opencode",
        env={"OPENCODE_API_KEY": SENTINEL},
    ).model_dump(mode="json")
    assert SENTINEL not in str(serialized)


def verify_pinned_config() -> None:
    for config_path in CONFIG_PATHS:
        raw = yaml.safe_load(config_path.read_text())
        config = JobConfig.model_validate(raw)
        assert len(config.agents) == 1
        agent = config.agents[0]
        assert agent.name == "opencode"
        assert agent.model_name == "opencode-go/ox-alpha-free"
        assert agent.env["OPENCODE_API_KEY"] == "${OPENCODE_API_KEY}"
        assert agent.kwargs["version"] == "1.18.21"
        assert (
            agent.kwargs["opencode_config"]["provider"]["opencode-go"]["options"][
                "baseURL"
            ]
            == "https://opencode.ai/zen/go/v1"
        )

    full_config = JobConfig.model_validate(yaml.safe_load(CONFIG_PATHS[1].read_text()))
    assert full_config.n_concurrent_trials == 1
    assert len(full_config.datasets) == 1
    assert full_config.datasets[0].n_tasks is None


def main() -> None:
    asyncio.run(verify_exec_transport())
    verify_persisted_metadata_redaction()
    verify_pinned_config()
    print("PASS: secrets stay out of Compose argv/config and OpenCode is pinned")


if __name__ == "__main__":
    main()
