<#
.SYNOPSIS
    Fetch pinned external SCPF package and install it in the active Python environment.
.DESCRIPTION
    vcs2l checks out dependencies.repos into ext/; never changes the pin.
    Uses vcs from PATH or the shared brainboxemb-dev-tools Conda environment.
    Safe to rerun; fails fast on missing tooling, wrong commit or failed pip install.
#>
[CmdletBinding()]
param([string]$CondaExe)
$ErrorActionPreference = 'Stop'
$repoRoot = $PSScriptRoot
$manifest = Join-Path $repoRoot 'dependencies.repos'
$ext = Join-Path $repoRoot 'ext'
$package = Join-Path $ext 'scpf/scpf/pyproject.toml'
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) { throw "Missing $manifest" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required.' }
New-Item -ItemType Directory -Path $ext -Force | Out-Null
$target = Join-Path $ext 'scpf'
$wanted = (Select-String -LiteralPath $manifest -Pattern '^\s*version:\s*([0-9a-f]{40})\s*$').Matches.Groups[1].Value
if (-not $wanted) { throw 'Expected an exact 40-character SCPF Git SHA in dependencies.repos.' }
Push-Location $repoRoot
try {
    if (Test-Path -LiteralPath (Join-Path $target '.git')) {
        # "vcs import" does not upgrade an existing checkout. On a pin
        # change, update only a checkout without TRACKED modifications. Untracked
        # pip editable-install metadata is not discarded.
        $current = (& git -C $target rev-parse HEAD).Trim()
        if ($LASTEXITCODE -ne 0) { throw "Invalid existing SCPF checkout at $target" }
        if ($current -ne $wanted) {
            $dirty = & git -C $target status --porcelain --untracked-files=no
            if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect the existing SCPF checkout.' }
            if ($dirty) {
                throw "SCPF ext/scpf has local changes; preserve them before updating from $current to $wanted."
            }
            Write-Host "Updating external SCPF from $current to $wanted"
            & git -C $target fetch origin $wanted
            if ($LASTEXITCODE -ne 0) { throw "Fetching pinned SCPF commit $wanted failed." }
            & git -C $target -c advice.detachedHead=false checkout --detach $wanted
            if ($LASTEXITCODE -ne 0) { throw "Checking out SCPF revision $wanted failed." }
        }
    } else {
        if (Test-Path -LiteralPath $target) {
            throw "Existing $target is not a Git checkout; move it aside before bootstrap."
        }
        # First installation uses vcs2l and the declarative manifest.
        $vcs = Get-Command vcs -CommandType Application -ErrorAction SilentlyContinue
        if ($vcs) {
            & $vcs.Source import --input dependencies.repos ext
        } else {
            $condaCmd = Get-Command conda.exe -CommandType Application -ErrorAction SilentlyContinue
            $candidates = @($CondaExe, $env:CONDA_EXE, $(if ($condaCmd) {$condaCmd.Source}), 'C:\tools\miniconda3\Scripts\conda.exe', $(if ($env:USERPROFILE) {Join-Path $env:USERPROFILE 'miniconda3\Scripts\conda.exe'}))
            $conda = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) } | Select-Object -First 1
            if (-not $conda) { throw 'vcs2l not found; activate brainboxemb-dev-tools or install vcs2l.' }
            & $conda run --no-capture-output --name brainboxemb-dev-tools vcs import --input dependencies.repos ext
        }
        if ($LASTEXITCODE -ne 0) { throw 'vcs import failed.' }
    }
    if (-not (Test-Path -LiteralPath $package -PathType Leaf)) { throw "Missing SCPF package: $package" }
    $actual = (& git -C $target rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $actual -ne $wanted) { throw "Wrong SCPF revision: expected $wanted, found $actual" }
    & python -m pip install -e ./ext/scpf/scpf
    if ($LASTEXITCODE -ne 0) { throw 'SCPF editable installation failed.' }
    Write-Host "Ready: SCPF library at $actual"
} finally { Pop-Location }
