#!/usr/bin/env bash
set -euo pipefail
ROOT="${ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
exec "$ROOT/scripts/deny_scan.sh" "${@:-}"
