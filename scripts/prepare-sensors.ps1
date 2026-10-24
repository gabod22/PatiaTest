param([string]$PackageRoot = (Join-Path $PSScriptRoot '..'))
$ErrorActionPreference = 'Stop'
try {
    $packagePath = (Resolve-Path -LiteralPath $PackageRoot).Path
    $manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'hardware-dependencies.json') -Raw | ConvertFrom-Json
    $installer = Join-Path $packagePath 'runtime/setup/PawnIO_setup.exe'
    if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) {
        throw 'Falta el instalador PawnIO en este paquete. Ejecute scripts/build-hardware.ps1 al preparar la distribución.'
    }
    if ((Get-FileHash -LiteralPath $installer -Algorithm SHA256).Hash -ne $manifest.pawnio.sha256) {
        throw 'El instalador PawnIO no coincide con la versión verificada.'
    }
    $signature = Get-AuthenticodeSignature -LiteralPath $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notlike "*$($manifest.pawnio.signer)*") {
        throw 'No se pudo verificar la firma del instalador PawnIO.'
    }
    # This is the official interactive setup: the user chooses installation and sees UAC.
    # No unrestricted/unsigned edition, silent installation or security setting changes.
    $setup = Start-Process -FilePath $installer -Verb RunAs -Wait -PassThru
    if ($setup.ExitCode -notin @(0, 3010)) { throw "PawnIO terminó con código $($setup.ExitCode)." }
    $installed = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\PawnIO' -ErrorAction SilentlyContinue
    if (-not $installed -or [version]$installed.DisplayVersion -lt [version]$manifest.pawnio.version) {
        throw 'La instalación no se completó o necesita reiniciar Windows.'
    }
    exit 0
} catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
