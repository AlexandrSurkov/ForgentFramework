<#
.SYNOPSIS
    Bootstrap a new repo with framework agent files and config.

.DESCRIPTION
    Copies bootstrap agent prompts and repo config files from the vendored
    framework/ directory into the repo root.
    Run from the repo root that contains framework/.

.PARAMETER Force
    Overwrite existing files instead of skipping them.

.EXAMPLE
    # From repo root:
    .\framework\tools\bootstrap.ps1
    .\framework\tools\bootstrap.ps1 -Force
#>
[CmdletBinding()]
param(
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve repo root: script is at <repo>/framework/tools/bootstrap.ps1
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

Write-Host ""
Write-Host "==> ForgentFramework bootstrap" -ForegroundColor Cyan
Write-Host "    Repo root : $repoRoot"
Write-Host "    Force     : $Force"
Write-Host ""

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
function Copy-IfMissing {
    param(
        [string]$Src,
        [string]$Dst,
        [bool]$ForceOverwrite
    )

    if (-not (Test-Path $Src)) {
        Write-Warning "  [SKIP]   $Dst  (source not found: $Src)"
        return
    }

    $dstDir = Split-Path $Dst -Parent
    if ($dstDir -and -not (Test-Path $dstDir)) {
        New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
    }

    if ((Test-Path $Dst) -and -not $ForceOverwrite) {
        Write-Host "  [EXISTS] $Dst  (use -Force to overwrite)" -ForegroundColor Yellow
    } else {
        Copy-Item -Path $Src -Destination $Dst -Force
        Write-Host "  [CREATED/UPDATED] $Dst" -ForegroundColor Green
    }
}

# ---------------------------------------------------------------------------
# Step 1 — Bootstrap agent files
# ---------------------------------------------------------------------------
Write-Host "--- Step 1: Bootstrap agent files" -ForegroundColor Cyan
$agentsSrc = Join-Path $repoRoot 'framework\templates\bootstrap-agents-templates\root\.github\agents'
$agentsDst = Join-Path $repoRoot '.github\agents'

if (-not (Test-Path $agentsDst)) {
    New-Item -ItemType Directory -Path $agentsDst -Force | Out-Null
}

Get-ChildItem -Path $agentsSrc -Filter '*.agent.md' -ErrorAction SilentlyContinue | ForEach-Object {
    $dst = Join-Path $agentsDst $_.Name
    Copy-IfMissing -Src $_.FullName -Dst $dst -ForceOverwrite $Force.IsPresent
}

# ---------------------------------------------------------------------------
# Step 2 — .vscode/settings.json
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Step 2: .vscode/settings.json" -ForegroundColor Cyan
Copy-IfMissing `
    -Src (Join-Path $repoRoot 'framework\templates\repo-files-templates\root\.vscode\settings.json') `
    -Dst (Join-Path $repoRoot '.vscode\settings.json') `
    -ForceOverwrite $Force.IsPresent

# ---------------------------------------------------------------------------
# Step 3 — .gitignore
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Step 3: .gitignore" -ForegroundColor Cyan
Copy-IfMissing `
    -Src (Join-Path $repoRoot 'framework\templates\repo-files-templates\root\.gitignore') `
    -Dst (Join-Path $repoRoot '.gitignore') `
    -ForceOverwrite $Force.IsPresent

# ---------------------------------------------------------------------------
# Step 4 — .agents/compliance/awesome-copilot-gate.md
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "--- Step 4: .agents/compliance/awesome-copilot-gate.md" -ForegroundColor Cyan
Copy-IfMissing `
    -Src (Join-Path $repoRoot 'framework\templates\repo-files-templates\root\.agents\compliance\awesome-copilot-gate.md') `
    -Dst (Join-Path $repoRoot '.agents\compliance\awesome-copilot-gate.md') `
    -ForceOverwrite $Force.IsPresent

# ---------------------------------------------------------------------------
# Next steps
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "==> Bootstrap complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit PROJECT.md — fill in project name, stack, models, and §pre answers."
Write-Host "  2. In .github/agents/*.agent.md, replace every 'model: TODO' with your chosen model"
Write-Host "     (e.g. 'model: gpt-4o' or 'model: claude-3-7-sonnet')."
Write-Host "  3. Open the repo in VS Code — agents will be auto-discovered via .vscode/settings.json."
Write-Host "  4. In Copilot Chat, switch to agent mode and select 'forgent-orchestrator' to start."
Write-Host ""
