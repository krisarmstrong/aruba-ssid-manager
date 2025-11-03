#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-$ROOT/.pyc-cache}"
mkdir -p "$PYTHONPYCACHEPREFIX"

python3 -m compileall -q -x '(^|/)(\.git|\.pyc-cache|\.venv|venv|env|archive)(/|$)' .

pip_failed=false

if [ -f pyproject.toml ]; then
  if ! python3 -m pip install --upgrade pip setuptools wheel; then
    pip_failed=true
  fi
  if ! python3 -m pip install -e .; then
    pip_failed=true
  fi
elif [ -f requirements.txt ]; then
  if ! python3 -m pip install --upgrade pip setuptools wheel; then
    pip_failed=true
  fi
  if ! python3 -m pip install -r requirements.txt; then
    pip_failed=true
  fi
fi

if $pip_failed; then
  echo "smoke.sh: pip operations failed (likely offline). Falling back to src/ on PYTHONPATH." >&2
  export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
fi

if ! python3 -m pip show pytest >/dev/null 2>&1; then
  if ! python3 -m pip install pytest; then
    echo "smoke.sh: pytest install failed; attempting to run bundled tests anyway." >&2
  fi
fi

python3 -m pytest -q
