$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $projectRoot
try {
    & (Join-Path $PSScriptRoot 'build-hardware.ps1')
    if ($LASTEXITCODE -ne 0) { throw 'Falló la preparación de hardware.' }
    pyside6-uic -o ui/hardware_ui.py ui/hardware.ui
    if ($LASTEXITCODE -ne 0) { throw 'Falló la generación de hardware.ui.' }
    pyside6-uic -o ui/mainwindow_ui.py ui/mainwindow.ui
    if ($LASTEXITCODE -ne 0) { throw 'Falló la generación de mainwindow.ui.' }
    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Fallaron las pruebas de Python.' }
    & (Join-Path $projectRoot 'runtime/hardware/PatiaHardwareHost.exe') --self-test
    if ($LASTEXITCODE -ne 0) { throw 'Fallaron las pruebas nativas.' }
    python -m PyInstaller --noconfirm PixelTest.spec
    if ($LASTEXITCODE -ne 0) { throw 'Falló la creación del paquete portable.' }
} finally {
    Pop-Location
}
