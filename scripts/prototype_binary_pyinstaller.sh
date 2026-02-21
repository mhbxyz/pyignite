#!/usr/bin/env bash
set -euo pipefail

# Prototype-only helper for issue #23.
# Builds a one-file Linux binary for local smoke testing.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

uv run --with pyinstaller pyinstaller \
  --onefile \
  --name pyqck-linux \
  --specpath /tmp \
  src/pyqck/__main__.py \
  --paths src

echo "Built artifact: $ROOT_DIR/dist/pyqck-linux"
