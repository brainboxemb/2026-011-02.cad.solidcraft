<#
.SYNOPSIS
    Prepare the pinned CAD Python libraries and tool.cad.ci checkout.
.DESCRIPTION
    Read exact Git commits from dependencies.repos. SCPF and SCPC are checked
    out under ext/ and installed editable into the active Python environment.
    tool.cad.ci is checked out under ext/cad-ci but is deliberately not
    installed: the CAD repository already owns scripts/ci/cad_ci.py, so the
    external tool is invoked through ext/cad-ci/cad-ci.py instead of importing
    another cad_ci module.
#>
[CmdletBinding()]
param([string]$CondaExe) # Old optional argument accepted for compatibility.
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot

$manifest = Join-Path $root 'dependencies.repos'
$ext = Join-Path $root 'ext'
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
    throw "Missing $manifest"
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required.'
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Activate the Python or Conda environment before running bootstrap.'
}
$source = Get-Content -LiteralPath $manifest -Raw
New-Item -ItemType Directory -Path $ext -Force | Out-Null

foreach ($name in @('scpf', 'scpc')) {
    # SCPF and SCPC are Python libraries, so bootstrap installs these two.
    $part = [regex]::Match($source, "(?ms)^  ${name}:\s*\r?\n(.*?)(?=^  [\w-]+:|\z)")
    if (-not $part.Success) { throw "Missing $name entry in dependencies.repos" }
    $urlMatch = [regex]::Match($part.Groups[1].Value, '(?m)^    url:\s*(\S+)\s*$')
    $shaMatch = [regex]::Match($part.Groups[1].Value, '(?m)^    version:\s*([0-9a-f]{40})\s*$')
    if (-not $urlMatch.Success -or -not $shaMatch.Success) {
        throw "Missing Git URL or exact revision for $name"
    }
    $url = $urlMatch.Groups[1].Value.Trim()
    $wanted = $shaMatch.Groups[1].Value
    $target = Join-Path $ext $name

    if (Test-Path -LiteralPath (Join-Path $target '.git')) {
        $current = (& git -C $target rev-parse HEAD).Trim()
        if ($LASTEXITCODE -ne 0) { throw "Cannot inspect $target" }
        if ($current -ne $wanted) {
            $dirty = & git -C $target status --porcelain --untracked-files=no
            if ($LASTEXITCODE -ne 0 -or $dirty) {
                throw "$name has local tracked changes; preserve them before updating."
            }
            & git -C $target remote set-url origin $url
            if ($LASTEXITCODE -ne 0) { throw "Cannot update origin for $name" }
            & git -C $target fetch origin $wanted
            if ($LASTEXITCODE -ne 0) { throw "Cannot fetch $name revision $wanted" }
            & git -C $target -c advice.detachedHead=false checkout --detach $wanted
            if ($LASTEXITCODE -ne 0) { throw "Cannot check out $name revision $wanted" }
        }
    } else {
        if (Test-Path -LiteralPath $target) {
            throw "$target exists but is not a Git checkout; move it aside first."
        }
        & git clone --quiet --no-checkout -- $url $target
        if ($LASTEXITCODE -ne 0) { throw "Cannot clone $url" }
        & git -C $target -c advice.detachedHead=false checkout --detach $wanted
        if ($LASTEXITCODE -ne 0) { throw "Cannot check out $name revision $wanted" }
    }
    $actual = (& git -C $target rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $actual -ne $wanted) {
        throw "$name revision mismatch: expected $wanted, found $actual"
    }
    $package = if ($name -eq 'scpf') { Join-Path $target 'scpf' } else { $target }
    if (-not (Test-Path -LiteralPath (Join-Path $package 'pyproject.toml'))) {
        throw "Missing package pyproject.toml at $package"
    }
    & python -m pip install -e $package
    if ($LASTEXITCODE -ne 0) { throw "Editable pip install failed for $name" }
    Write-Host "Ready: $name at $actual"
}

# tool.cad.ci remains executable repository tooling, not an installed package.
& python (Join-Path $root 'scripts/ci/bootstrap_cad_ci.py')
if ($LASTEXITCODE -ne 0) {
    throw 'tool.cad.ci bootstrap failed.'
}
