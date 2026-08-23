# ox-alpha DeepSWE benchmark

Reproducible OpenCode/Pier configuration and local results for running
`opencode-go/ox-alpha-free` against the complete 113-task DeepSWE suite.

## Current run

<!-- benchmark-status:start -->
### Live benchmark status

_Updated: `2026-08-23T17:51:56-04:00`_

| Metric | Value |
| --- | ---: |
| Completed | 23 / 113 |
| Running | 1 |
| Pending | 89 |
| Errors | 5 |
| Retries | 4 |
| Binary solves | 8 / 23 |
| Mean partial score | 0.887734 |
| Active task | `pwntools-tube-multiplexing` |
| Active phase | verifier |

#### Completed task scores

| Task | Outcome | Reward | Partial | Feature tests | Regression tests |
| --- | --- | ---: | ---: | ---: | ---: |
| [`meriyah-explicit-resource-declarations`](benchmark-results/ox-alpha-opencode-full-20260822/meriyah-explicit-resource-declar__4HeHf3g/result.json) | ❌ not solved | 0 | 0.999942 | 46/49 | 51469/51469 |
| [`query-persist-restored-query-state`](benchmark-results/ox-alpha-opencode-full-20260822/query-persist-restored-query-sta__o95SNKJ/result.json) | ❌ not solved | 0 | 0.960000 | 7/8 | 41/42 |
| [`helm-unified-manifest-stream`](benchmark-results/ox-alpha-opencode-full-20260822/helm-unified-manifest-stream__CqoVDN4/result.json) | ✅ solved | 1 | 1.000000 | 5/5 | 2/2 |
| [`anko-typed-variable-bindings`](benchmark-results/ox-alpha-opencode-full-20260822/anko-typed-variable-bindings__ru8RZaa/result.json) | ❌ not solved | 0 | 0.912621 | 0/9 | 94/94 |
| [`igel-persist-feature-schema`](benchmark-results/ox-alpha-opencode-full-20260822/igel-persist-feature-schema__wQ7eGEi/result.json) | ✅ solved | 1 | 1.000000 | 24/24 | 2/2 |
| [`fastapi-deprecation-response-headers`](benchmark-results/ox-alpha-opencode-full-20260822/fastapi-deprecation-response-hea__rvMSpWr/result.json) | ❌ not solved | 0 | 0.998471 | 132/137 | 3134/3134 |
| [`scc-bounded-memory-spilling`](benchmark-results/ox-alpha-opencode-full-20260822/scc-bounded-memory-spilling__AGndF2b/result.json) | ❌ not solved | 0 | 0.949527 | 31/31 | 270/286 |
| [`katex-multicolumn-array-spans`](benchmark-results/ox-alpha-opencode-full-20260822/katex-multicolumn-array-spans__a9XRVAi/result.json) | ❌ not solved | 0 | 0.864358 | 0/94 | 599/599 |
| [`arktype-json-schema-refs-dependencies`](benchmark-results/ox-alpha-opencode-full-20260822/arktype-json-schema-refs-depende__uyn2ceH/result.json) | ❌ not solved | 0 | 0.985329 | 0/25 | 1679/1679 |
| [`vulture-persistent-analysis-cache`](benchmark-results/ox-alpha-opencode-full-20260822/vulture-persistent-analysis-cach__shBfz3w/result.json) | ❌ not solved | 0 | 0.987461 | 24/24 | 291/295 |
| [`dynamodb-toolbox-conditional-attribute-requirements`](benchmark-results/ox-alpha-opencode-full-20260822/dynamodb-toolbox-conditional-att__DUxKVjP/result.json) | ❌ not solved | 0 | 0.976117 | 0/31 | 1267/1267 |
| [`obsidian-linter-link-format-conversion`](benchmark-results/ox-alpha-opencode-full-20260822/obsidian-linter-link-format-conv__7XexxeF/result.json) | ❌ not solved | 0 | 0.999160 | 59/60 | 1131/1131 |
| [`httpx-deterministic-cookie-store`](benchmark-results/ox-alpha-opencode-full-20260822/httpx-deterministic-cookie-store__VmRaraN/result.json) | ✅ solved | 1 | 1.000000 | 115/115 | 1281/1281 |
| [`dasel-html-document-format`](benchmark-results/ox-alpha-opencode-full-20260822/dasel-html-document-format__EP38DkK/result.json) | ❌ not solved | 0 | 0.873921 | 0/146 | 1012/1012 |
| [`tengo-destructuring-bindings`](benchmark-results/ox-alpha-opencode-full-20260822/tengo-destructuring-bindings__nDEBGJv/result.json) | ❌ not solved | 0 | 0.591928 | 0/91 | 132/132 |
| [`langchain-request-coalescing`](benchmark-results/ox-alpha-opencode-full-20260822/langchain-request-coalescing__V4NXfSx/result.json) | ⚠️ error | n/a | n/a | n/a/n/a | n/a/n/a |
| [`go-genai-streamed-function-args`](benchmark-results/ox-alpha-opencode-full-20260822/go-genai-streamed-function-args__cPRXg9R/result.json) | ✅ solved | 1 | 1.000000 | 6/6 | 62/62 |
| [`koota-query-predicates`](benchmark-results/ox-alpha-opencode-full-20260822/koota-query-predicates__H8NarqM/result.json) | ✅ solved | 1 | 1.000000 | 43/43 | 172/172 |
| [`skrub-duration-encoding`](benchmark-results/ox-alpha-opencode-full-20260822/skrub-duration-encoding__bjnc3np/result.json) | ✅ solved | 1 | 1.000000 | 130/130 | 2784/2784 |
| [`happy-dom-abort-pending-body-reads`](benchmark-results/ox-alpha-opencode-full-20260822/happy-dom-abort-pending-body-rea__J4iX3oS/result.json) | ✅ solved | 1 | 1.000000 | 14/14 | 165/165 |
| [`ytt-jsonpath-query-api`](benchmark-results/ox-alpha-opencode-full-20260822/ytt-jsonpath-query-api__YhkQZ9E/result.json) | ✅ solved | 1 | 1.000000 | 103/103 | 1/1 |
| [`updo-policy-alerting`](benchmark-results/ox-alpha-opencode-full-20260822/updo-policy-alerting__ZZ3cmSM/result.json) | ❌ not solved | 0 | 0.985714 | 15/17 | 123/123 |
| [`kcp-go-multiplexed-kcp-streams`](benchmark-results/ox-alpha-opencode-full-20260822/kcp-go-multiplexed-kcp-streams__hqymzMt/result.json) | ❌ not solved | 0 | 0.333333 | 2/30 | 12/12 |
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
