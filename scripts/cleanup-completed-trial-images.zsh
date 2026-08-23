#!/usr/bin/env zsh
set -euo pipefail

JOB_DIR=${1:?usage: cleanup-completed-trial-images.zsh JOB_DIR}

[[ -d "$JOB_DIR" ]] || exit 0

for result_path in "$JOB_DIR"/*/result.json(N); do
  jq -e '.finished_at != null' "$result_path" >/dev/null 2>&1 || continue

  trial_dir=${result_path:h}
  trial_name=${trial_dir:t}
  normalized_name=${trial_name:l}

  for image_name in \
    "${normalized_name}-main" \
    "${normalized_name}-pier-egress-proxy" \
    "${normalized_name}__verifier__trial-main"; do
    if docker image inspect "$image_name" >/dev/null 2>&1; then
      docker image rm "$image_name" >/dev/null 2>&1 || true
    fi
  done

  # DeepSWE bases are large and usually task-specific. Delete only the exact
  # benchmark base recorded in this completed trial's generated Dockerfile.
  dockerfile="$trial_dir/agent-build-context/Dockerfile"
  if [[ -f "$dockerfile" ]]; then
    base_image=$(sed -nE '/^FROM[[:space:]]+/{s/^FROM[[:space:]]+([^[:space:]]+).*/\1/p;q;}' "$dockerfile")
    if [[ "$base_image" == public.ecr.aws/d3j8x8q7/swe-bench-* ]] && \
        docker image inspect "$base_image" >/dev/null 2>&1; then
      docker image rm "$base_image" >/dev/null 2>&1 || true
    fi
  fi
done

find "$JOB_DIR" -type d -exec chmod 700 {} +
find "$JOB_DIR" -type f -exec chmod 600 {} +
