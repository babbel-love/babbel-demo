#!/usr/bin/env bash
set -euo pipefail
cd "${BABEL_ROOT:-$PWD}"
[ -f streamlit.out ] || { echo "No streamlit.out to rotate"; exit 0; }
ts="$(date +%Y%m%d-%H%M%S)"
mv streamlit.out "streamlit.out.$ts"
gzip -9 "streamlit.out.$ts"
echo "Rotated to streamlit.out.$ts.gz"
