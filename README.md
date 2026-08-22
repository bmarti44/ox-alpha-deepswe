# ox-alpha DeepSWE benchmark

Reproducible OpenCode/Pier configuration and local results for running
`opencode-go/ox-alpha-free` against the complete 113-task DeepSWE suite.

## Current run

<!-- benchmark-status:start -->
### Live benchmark status

_Updated: `2026-08-22T19:42:10-04:00`_

| Metric | Value |
| --- | ---: |
| Completed | 2 / 113 |
| Running | 1 |
| Pending | 110 |
| Errors | 0 |
| Retries | 0 |
| Binary solves | 0 / 2 |
| Mean partial score | 0.979971 |
| Active task | `helm-unified-manifest-stream` |
| Active phase | agent execution |
<!-- benchmark-status:end -->

The full run is stored in
[`benchmark-results/ox-alpha-opencode-full-20260822`](benchmark-results/ox-alpha-opencode-full-20260822).
Its aggregate [`result.json`](benchmark-results/ox-alpha-opencode-full-20260822/result.json)
is updated by Pier as trials finish. The earlier one-task canary is retained in
[`benchmark-results/ox-alpha-opencode-canary`](benchmark-results/ox-alpha-opencode-canary).

Per-trial directories preserve the OpenCode transcript and normalized
trajectory, model patch, verifier reports, reward, configuration, and logs.
Pier's generated `docker-compose-egress-proxy.json` files are intentionally not
tracked because they contain short-lived proxy credentials; they are runtime
plumbing, not benchmark results.

## Reproduce

Requirements: macOS, Docker Desktop, OpenCode 1.18.21, Pier 0.3.1, and an
`OPENCODE_API_KEY` exported in the invoking shell.

```zsh
git submodule update --init --recursive
source ~/.zshrc
./scripts/verify-pier-secret-transport.py
./scripts/run-opencode-full-suite.zsh
```

The runner uses one concurrent trial, checks that all 113 DeepSWE tasks are
present, keeps result files private locally, prevents macOS sleep, retries one
transient failure, and removes task-specific Docker images after completed
trials to limit disk growth.

While a full run is active, `scripts/publish-benchmark-status.zsh` refreshes the
README dashboard and pushes completed trial artifacts every 30 minutes.

## Security note

The Pier installation used for this run includes a local fix that sends agent
environment values through the child process environment instead of embedding
them in Docker Compose command arguments. Run the included regression check
after reinstalling or upgrading Pier because package upgrades can overwrite the
local fix.
