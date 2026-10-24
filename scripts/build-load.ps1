param([switch]$SkipAssets)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectFile = Join-Path $projectRoot 'native/PatiaLoadHost/PatiaLoadHost.csproj'
dotnet restore $projectFile --locked-mode --packages (Join-Path $projectRoot 'build/nuget') --configfile (Join-Path $projectRoot 'native/PatiaHardwareHost/NuGet.Config') -p:SelfContained=true
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron restaurar las dependencias de carga fijadas.' }
dotnet publish $projectFile -c Release -r win-x64 --self-contained true --no-restore -p:PublishSingleFile=false -p:PublishTrimmed=false -o (Join-Path $projectRoot 'runtime/load')
if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar PatiaLoadHost.' }
if (-not $SkipAssets) {
    python (Join-Path $PSScriptRoot 'vendor-hardware-assets.py')
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron preparar las licencias.' }
}
Write-Output 'Motor de carga portable preparado en runtime/load.'
