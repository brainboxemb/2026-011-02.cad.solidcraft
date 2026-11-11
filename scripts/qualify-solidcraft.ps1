# Execute a Python SCPF model through the installed SolidCraft CLI.
# Run from the repository root: .\scripts\qualify-solidcraft.ps1 -Snapshot
[CmdletBinding()]
param(
    [string]$CliPath = '',
    [string]$Model = 'models/sample-plate/scpf/model.py',
    [switch]$Snapshot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = Split-Path -Parent $PSScriptRoot
$out = Join-Path $root 'output'
$scriptFile = Join-Path $out 'solidcraft-commands.json'
$nativeFile = Join-Path $out 'solidcraft-model.sc'
$stepFile = Join-Path $out 'solidcraft-model.step'
$resultsFile = Join-Path $out 'solidcraft-results.json'
$evalFile = Join-Path $out 'solidcraft-eval.json'
$pngFile = Join-Path $out 'solidcraft-model.png'

if (-not $CliPath) {
    $found = Get-Command solidcraft-cli -ErrorAction SilentlyContinue
    if ($found) { $CliPath = $found.Source }
    else {
        $fallback = Join-Path $env:ProgramFiles 'SolidCraft\solidcraft-cli.exe'
        if (Test-Path -LiteralPath $fallback) { $CliPath = $fallback }
    }
}
if (-not $CliPath -or -not (Test-Path -LiteralPath $CliPath)) {
    throw 'SolidCraft CLI not found. Install SolidCraft or supply -CliPath.'
}
New-Item -ItemType Directory -Path $out -Force | Out-Null
# SCPF is an external editable package installed by bootstrap.ps1.
# The CAD project does not set PYTHONPATH or run library-owned unit tests.
& python -m pip show scpf | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'SCPF package missing: run .\bootstrap.ps1.' }
& python -m scpf (Join-Path $root $Model) --out $scriptFile
if ($LASTEXITCODE -ne 0) { throw 'SCPF compilation failed.' }

& $CliPath --version
if ($LASTEXITCODE -ne 0) { throw 'SolidCraft version check failed.' }
& $CliPath run $scriptFile --param-check strict --results --json-out $resultsFile --save $nativeFile --out $stepFile
if ($LASTEXITCODE -ne 0) { throw 'Native SolidCraft execution failed.' }
& $CliPath eval $nativeFile --json-out $evalFile
if ($LASTEXITCODE -ne 0) { throw 'Native SolidCraft evaluation failed.' }
if ($Snapshot) {
    & $CliPath snapshot $nativeFile --out $pngFile --no-grid --no-axes
    if ($LASTEXITCODE -ne 0) { throw 'Native SolidCraft snapshot failed.' }
}
Write-Host "Native SolidCraft result: $nativeFile"
Write-Host "Generated commands: $scriptFile"
Write-Host "Measurements: $evalFile"
