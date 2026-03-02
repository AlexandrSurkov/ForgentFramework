#!/usr/bin/env bash
# bootstrap.sh — Bootstrap a new repo with framework agent files and config.
#
# Copies bootstrap agent prompts and repo config files from the vendored
# framework/ directory into the repo root.
# Run from the repo root that contains framework/.
#
# Usage:
#   bash framework/tools/bootstrap.sh
#   bash framework/tools/bootstrap.sh --force

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

FORCE=false
for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=true ;;
    *) echo "Unknown argument: $arg" >&2; exit 1 ;;
  esac
done

echo ""
echo "==> ForgentFramework bootstrap"
echo "    Repo root : ${REPO_ROOT}"
echo "    Force     : ${FORCE}"
echo ""

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
copy_if_missing() {
  local src="$1"
  local dst="$2"

  if [[ ! -f "$src" ]]; then
    echo "  [SKIP]   ${dst}  (source not found: ${src})"
    return
  fi

  local dst_dir
  dst_dir="$(dirname "$dst")"
  if [[ -n "$dst_dir" && ! -d "$dst_dir" ]]; then
    mkdir -p "$dst_dir"
  fi

  if [[ -f "$dst" && "$FORCE" != true ]]; then
    echo "  [EXISTS] ${dst}  (use --force to overwrite)"
  else
    cp "$src" "$dst"
    echo "  [CREATED/UPDATED] ${dst}"
  fi
}

# ---------------------------------------------------------------------------
# Step 1 — Bootstrap agent files
# ---------------------------------------------------------------------------
echo "--- Step 1: Bootstrap agent files"
AGENTS_SRC="${REPO_ROOT}/framework/templates/bootstrap-agents-templates/root/.github/agents"
AGENTS_DST="${REPO_ROOT}/.github/agents"

mkdir -p "$AGENTS_DST"

if compgen -G "${AGENTS_SRC}/*.agent.md" > /dev/null 2>&1; then
  for src_file in "${AGENTS_SRC}"/*.agent.md; do
    filename="$(basename "$src_file")"
    copy_if_missing "$src_file" "${AGENTS_DST}/${filename}"
  done
else
  echo "  [WARN] No *.agent.md files found in ${AGENTS_SRC}"
fi

# ---------------------------------------------------------------------------
# Step 2 — .vscode/settings.json
# ---------------------------------------------------------------------------
echo ""
echo "--- Step 2: .vscode/settings.json"
copy_if_missing \
  "${REPO_ROOT}/framework/templates/repo-files-templates/root/.vscode/settings.json" \
  "${REPO_ROOT}/.vscode/settings.json"

# ---------------------------------------------------------------------------
# Step 3 — .gitignore
# ---------------------------------------------------------------------------
echo ""
echo "--- Step 3: .gitignore"
copy_if_missing \
  "${REPO_ROOT}/framework/templates/repo-files-templates/root/.gitignore" \
  "${REPO_ROOT}/.gitignore"

# ---------------------------------------------------------------------------
# Step 4 — .agents/compliance/awesome-copilot-gate.md
# ---------------------------------------------------------------------------
echo ""
echo "--- Step 4: .agents/compliance/awesome-copilot-gate.md"
copy_if_missing \
  "${REPO_ROOT}/framework/templates/repo-files-templates/root/.agents/compliance/awesome-copilot-gate.md" \
  "${REPO_ROOT}/.agents/compliance/awesome-copilot-gate.md"

# ---------------------------------------------------------------------------
# Step 5 - Set model: gpt-4.1 in all agent files
# ---------------------------------------------------------------------------
echo ""
echo "--- Step 5: Set model in agent files"
if compgen -G "${REPO_ROOT}/.github/agents/*.agent.md" > /dev/null 2>&1; then
  for agent_file in "${REPO_ROOT}"/.github/agents/*.agent.md; do
    if grep -q 'model: TODO' "$agent_file"; then
      sed -i 's/model: TODO/model: gpt-4.1/g' "$agent_file"
      echo "  [MODEL SET] $(basename "$agent_file")"
    fi
  done
fi

# ---------------------------------------------------------------------------
# Next steps
# ---------------------------------------------------------------------------
echo ""
echo "==> Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Open the repo in VS Code -- agents will be auto-discovered via .vscode/settings.json."
echo "  2. In Copilot Chat, switch to agent mode and select bootstrap-orchestrator."
echo "  3. The bootstrap-orchestrator will scan the repo, auto-fill PROJECT.md, and guide you through Install."
echo ""
