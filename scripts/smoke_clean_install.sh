#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cd "$root"
uv build --wheel --out-dir "$tmp/dist"
uv venv --python 3.12 "$tmp/venv"
uv pip install --python "$tmp/venv/bin/python" "$tmp"/dist/*.whl
actual="$($tmp/venv/bin/agentkit-mvp0)"
test "$actual" = "Hallo, ARTUR!"
printf '%s\n' "$actual"
