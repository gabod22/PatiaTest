# -*- mode: python ; coding: utf-8 -*-


from pathlib import Path

root = Path(SPECPATH)
if not (root / 'runtime/hardware/PatiaHardwareHost.exe').is_file():
    raise RuntimeError('Ejecute scripts/build-hardware.ps1 antes de empaquetar.')

replaced = {'battery_info.exe', 'batteryinfoview.exe', 'cpuz.exe', 'cpu-z.exe',
            'gpuz.exe', 'gpu-z.exe', 'diskinfo.exe', 'diskinfo32.exe', 'diskinfo64.exe',
            'hwinfo.exe', 'hwinfo64.exe', 'gpuz.xml', 'battery_info.cfg'}
program_data = [(str(file), str(file.parent.relative_to(root)))
                for file in (root / 'programs').rglob('*')
                if file.is_file() and file.name.lower() not in replaced
                and 'diskinfo' not in {part.lower() for part in file.relative_to(root / 'programs').parts[:-1]}]

a = Analysis(
    ['PixelTest.py'],
    pathex=[],
    binaries=[],
    datas=[('config_files/*', 'config_files'), ('assets/*', 'assets'),
           ('runtime/hardware', 'runtime/hardware'), ('runtime/licenses', 'runtime/licenses'),
           ('runtime/setup', 'runtime/setup'), ('scripts/prepare-sensors.ps1', 'scripts'),
           ('scripts/hardware-dependencies.json', 'scripts')] + program_data,
    hiddenimports=['pywintypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PixelTest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['assets\\logo_min_new.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='PixelTest',
)
