param([switch]$SkipAssets)
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$projectFile = Join-Path $projectRoot 'native/PatiaHardwareHost/PatiaHardwareHost.csproj'
$packages = Join-Path $projectRoot 'build/nuget'
$output = Join-Path $projectRoot 'runtime/hardware'
dotnet restore $projectFile --locked-mode --packages $packages --configfile (Join-Path $projectRoot 'native/PatiaHardwareHost/NuGet.Config') -p:SelfContained=true
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron restaurar las dependencias fijadas.' }
dotnet publish $projectFile -c Release -r win-x64 --self-contained true --no-restore -p:PublishSingleFile=false -p:PublishTrimmed=false -o $output
if ($LASTEXITCODE -ne 0) { throw 'No se pudo compilar PatiaHardwareHost.' }
if (-not $SkipAssets) {
    python (Join-Path $PSScriptRoot 'vendor-hardware-assets.py')
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron preparar las licencias y el instalador firmado.' }
    $installer = Join-Path $projectRoot 'runtime/setup/PawnIO_setup.exe'
    $signature = Get-AuthenticodeSignature -LiteralPath $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notlike '*CN=namazso.eu*') {
        throw 'La firma del instalador PawnIO no es válida.'
    }
}
Write-Output "Componente portable preparado en $output"
