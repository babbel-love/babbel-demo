#!/usr/bin/env bash
set -euo pipefail
ROOT="${ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$ROOT"
DENY_REGEX='(?i)\b((c?hat)?gpt|open\s*ai)\b'
ALLOWLIST_FILE="${ALLOWLIST_FILE:-scanner_allowlist.txt}"
TMP_REPORT="$(mktemp)"
trap 'rm -f "$TMP_REPORT"' EXIT
is_allowlisted() {
  local p="$1"
  [ -f "$ALLOWLIST_FILE" ] && grep -Fxq "$p" "$ALLOWLIST_FILE"
}
scan_paths_for_names() {
  local list=("$@")
  local failed=0
  for p in "${list[@]}"; do
    rel="${p#./}"
    if ! is_allowlisted "$rel"; then
      if echo "$rel" | grep -E -i -q "$DENY_REGEX"; then
        echo "banned in filename: $rel" | tee -a "$TMP_REPORT"
        failed=1
      fi
    fi
  done
  return $failed
}
scan_file_content() {
  local f="$1"
  local rel="${f#./}"
  if is_allowlisted "$rel"; then return 0; fi
  if [ -f "$f" ] && [ -r "$f" ]; then
    if grep -Iq . "$f"; then
      if grep -E -I -n -i -q "$DENY_REGEX" "$f"; then
        grep -E -I -n -i "$DENY_REGEX" "$f" | sed "s|^|$rel:|"
        return 1
      fi
    fi
  fi
  return 0
}
scan_list_for_content() {
  local failed=0
  for f in "$@"; do
    scan_file_content "$f" >>"$TMP_REPORT" || failed=1
  done
  return $failed
}
select_textlike() {
  grep -E -i '\.(py|sh|txt|md|yml|yaml|toml|json|ini|cfg|conf|plist|xml|html|js|ts|jsx|tsx|java|c|cpp|h|swift|csv)$' || true
}
scan_commit_message() {
  local msg_file="$1"
  if [ -f "$msg_file" ]; then
    if grep -E -I -n -i -q "$DENY_REGEX" "$msg_file"; then
      echo "banned in commit message:"
      grep -E -I -n -i "$DENY_REGEX" "$msg_file"
      return 1
    fi
  fi
  return 0
}
scan_staged() {
  mapfile -t names < <(git diff --cached --name-only)
  [ "${#names[@]}" -eq 0 ] && return 0
  scan_paths_for_names "${names[@]}"
  mapfile -t textfiles < <(printf "%s\n" "${names[@]}" | select_textlike)
  [ "${#textfiles[@]}" -eq 0 ] && return 0
  scan_list_for_content "${textfiles[@]}"
}
scan_repo() {
  mapfile -t names < <(git ls-files)
  scan_paths_for_names "${names[@]}"
  mapfile -t textfiles < <(printf "%s\n" "${names[@]}" | select_textlike)
  scan_list_for_content "${textfiles[@]}"
}
scan_custom_paths() {
  local files=("$@")
  scan_paths_for_names "${files[@]}"
  scan_list_for_content "${files[@]}"
}
if [ "${1:-}" = "--commit-message" ]; then
  scan_commit_message "$2" || { echo "commit message contains banned identifier(s)"; exit 1; }
  exit 0
elif [ "${STAGED:-}" = "1" ]; then
  scan_staged || { cat "$TMP_REPORT"; exit 1; }
  echo "staged scan ok"
  exit 0
elif [ "$#" -gt 0 ]; then
  scan_custom_paths "$@" || { cat "$TMP_REPORT"; exit 1; }
  echo "custom path scan failed"
  exit 1
else
  scan_repo || { cat "$TMP_REPORT"; exit 1; }
  echo "repo scan ok"
  exit 0
fi
