<#
.SYNOPSIS
    Install the exact Forge revision pinned by this CAD repository.
.DESCRIPTION
    Reads dependencies.forge.version, dependencies.forge.commit and
    dependencies.solidcraft.version from ci.yml. Local development and CI use
    the same exact Forge revision.
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
$commit = Read-ForgeValue 'commit'

if ($version -notmatch '^\d+\.\d+\.\d+

& python -m pip install --disable-pip-version-check --no-deps --upgrade --force-reinstall $install
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Forge $version at $commit"
}

$expectedPackageVersion = $version
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

Write-Host "Ready: Forge $version @ $commit (SCPF $actualPackageVersion)"
Write-Host "Qualified SolidCraft: $qualifiedSolidCraft"
) {
    throw "Forge package version must be semantic X.Y.Z; found $version"
}
if ($commit -notmatch '^[0-9a-f]{40}

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
) {
    throw "Forge commit must be an exact 40-character SHA; found $commit"
}

$remote = "https://github.com/$repository.git"
$install = "git+$remote@$commit#subdirectory=cadlib"

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
