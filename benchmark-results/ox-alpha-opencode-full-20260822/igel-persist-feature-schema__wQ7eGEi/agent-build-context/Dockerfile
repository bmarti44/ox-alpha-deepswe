FROM public.ecr.aws/d3j8x8q7/swe-bench-202605:kh7brwh7cv23ggeshkz85ac5fx831x5k-v1.1
ARG PIER_AGENT_INSTALL_FINGERPRINT=4e71bc50fa97c715
RUN ["/bin/bash", "-c", "printf \"Pier agent install fingerprint: %s\\n\" \"$PIER_AGENT_INSTALL_FINGERPRINT\""]
USER root
RUN ["/bin/bash", "-c", "export DEBIAN_FRONTEND=noninteractive; apt-get update && apt-get install -y curl"]
USER root
RUN ["/bin/bash", "-c", "set -euo pipefail; curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash && export NVM_DIR=\"$HOME/.nvm\" && \\. \"$NVM_DIR/nvm.sh\" || true && command -v nvm &>/dev/null || { echo 'Error: NVM failed to load' >&2; exit 1; } && nvm install 22 && npm -v && npm i -g opencode-ai@1.18.21 && opencode --version"]
