# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Patiatest.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\brian\\Proyectos\\patiatest\\config_files', 'config_files'), ('C:\\Users\\brian\\Proyectos\\patiatest\\programs', 'programs'), ('C:\\Users\\brian\\Proyectos\\patiatest\\assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Patiatest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['C:\\Users\\brian\\Proyectos\\patiatest\\assets\\logo_min.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Patiatest',
)
