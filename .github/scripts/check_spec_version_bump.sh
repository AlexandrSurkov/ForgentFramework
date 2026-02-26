#!/usr/bin/env bash
set -euo pipefail

BASE_SHA="${1:-}"
HEAD_SHA="${2:-HEAD}"

if [[ -z "${BASE_SHA}" ]]; then
  echo "ERROR: BASE_SHA is required."
  echo "Usage: $0 <base_sha> [head_sha]"
  exit 2
fi

changed_files="$(git diff --name-only "${BASE_SHA}" "${HEAD_SHA}")"

if ! echo "${changed_files}" | grep -qE '^framework/'; then
  echo "OK: No changes under framework/."
  exit 0
fi

require_changed() {
  local file="$1"
  if ! echo "${changed_files}" | grep -qx "${file}"; then
    echo "ERROR: framework/ changed, but required file not updated: ${file}"
    exit 1
  fi
}

require_changed "framework/00-multi-agent-development-spec.md"
require_changed "framework/CHANGELOG.md"

extract_version_from_text() {
  # Extracts X.Y.Z from a line like: > **Version:** 0.21.2 · **Updated:** 2026-02-26
  sed -nE 's/^> \*\*Version:\*\* ([0-9]+\.[0-9]+\.[0-9]+).*/\1/p' | head -n 1
}

old_version="$(git show "${BASE_SHA}:framework/00-multi-agent-development-spec.md" | extract_version_from_text)"
new_version="$(cat framework/00-multi-agent-development-spec.md | extract_version_from_text)"

if [[ -z "${old_version}" ]]; then
  echo "ERROR: Could not parse old spec version from base revision."
  exit 1
fi

if [[ -z "${new_version}" ]]; then
  echo "ERROR: Could not parse new spec version from working tree."
  exit 1
fi

if [[ "${old_version}" == "${new_version}" ]]; then
  echo "ERROR: framework/ changed but spec version did not bump (still ${new_version})."
  exit 1
fi

# Ensure new_version is greater than old_version.
if ! printf '%s\n%s\n' "${old_version}" "${new_version}" | sort -V -C; then
  echo "ERROR: Spec version must increase. Old=${old_version} New=${new_version}"
  exit 1
fi

# Ensure changelog contains the new version header.
if ! grep -qE "^## \[${new_version}\]" framework/CHANGELOG.md; then
  echo "ERROR: framework/CHANGELOG.md must contain a release header for ${new_version} (e.g., '## [${new_version}] - YYYY-MM-DD')."
  exit 1
fi

# Ensure pinned references in this repo are consistent with the new version.
if ! grep -q "v${new_version}" PROJECT.md; then
  echo "ERROR: PROJECT.md must reference spec version v${new_version}."
  exit 1
fi

if ! grep -q "(v${new_version})" AGENTS.md; then
  echo "ERROR: AGENTS.md must reference spec version (v${new_version})."
  exit 1
fi

echo "OK: framework/ change includes version bump ${old_version} -> ${new_version} and changelog/references are consistent."
