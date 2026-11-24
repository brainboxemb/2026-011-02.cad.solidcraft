<#
.SYNOPSIS
    Install the Forge release pinned by this CAD repository.
.DESCRIPTION
    Reads dependencies.forge.version and dependencies.solidcraft.version from
    ci.yml. The Forge version is the released Git tag used by both local
    development and CI.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$configPath = Join-Path $root 'ci.yml'

if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    throw "Missing $configPath"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python must be available in the active environment.'
}

$source = Get-Content -LiteralPath $configPath -Raw
$forgeMatch = [regex]::Match(
    $source,
    '(?ms)^  forge:\s*\r?\n(?<body>.*?)(?=^  solidcraft:)'
)
if (-not $forgeMatch.Success) {
    throw 'Missing dependencies.forge in ci.yml'
}
$forge = $forgeMatch.Groups['body'].Value

function Read-ForgeValue([string]$Name) {
    $match = [regex]::Match(
        $forge,
        "(?m)^    $([regex]::Escape($Name)):\s*(\S+)\s*$"
    )
    if (-not $match.Success) {
        throw "Missing dependencies.forge.$Name in ci.yml"
    }
    return $match.Groups[1].Value.Trim()
}

$repository = Read-ForgeValue 'repository'
$version = Read-ForgeValue 'version'

if ($version -notmatch '^v\d+\.\d+\.\d+$') {
    throw "Forge version must be a v-prefixed release tag; found $version"
}

$remote = "https://github.com/$repository.git"
$install = "git+$remote@$version#subdirectory=scpf"

& python -m pip install --disable-pip-version-check --no-deps --upgrade --force-reinstall $install
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Forge $version"
}

$expectedPackageVersion = $version.Substring(1)
$actualPackageVersion = (& python -c "from importlib.metadata import version; print(version('scpf'))").Trim()
if ($LASTEXITCODE -ne 0 -or $actualPackageVersion -ne $expectedPackageVersion) {
    throw "SCPF version mismatch: expected $expectedPackageVersion, found $actualPackageVersion"
}

$solidcraftMatch = [regex]::Match(
    $source,
    '(?ms)^  solidcraft:\s*\r?\n(?<body>.*?)(?=^\S|\z)'
)
if (-not $solidcraftMatch.Success) {
    throw 'Missing dependencies.solidcraft in ci.yml'
}
$scVersionMatch = [regex]::Match(
    $solidcraftMatch.Groups['body'].Value,
    '(?m)^    version:\s*(\S+)\s*$'
)
if (-not $scVersionMatch.Success) {
    throw 'Missing dependencies.solidcraft.version in ci.yml'
}
$expectedSolidCraft = $scVersionMatch.Groups[1].Value.Trim()
$qualifiedSolidCraft = (& python -c "from scpf.version import TESTED_SOLIDCRAFT_VERSION; print(TESTED_SOLIDCRAFT_VERSION)").Trim()
if ($LASTEXITCODE -ne 0 -or $qualifiedSolidCraft -ne $expectedSolidCraft) {
    throw "Forge $version qualifies SolidCraft $qualifiedSolidCraft, but ci.yml pins $expectedSolidCraft"
}

Write-Host "Ready: Forge $version (SCPF $actualPackageVersion)"
Write-Host "Qualified SolidCraft: $qualifiedSolidCraft"
