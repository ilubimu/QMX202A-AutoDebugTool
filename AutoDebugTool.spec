# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['AutoDebugTool.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\ProgramData\\anaconda3\\Lib\\site-packages\\BeautifulReport\\template\\template.html', '.\\BeautifulReport\\template'),
        ('C:\\ProgramData\\anaconda3\\Lib\\site-packages\\BeautifulReport\\template\\theme_default.json', '.\\BeautifulReport\\template')
    ],
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
    a.binaries,
    a.datas,
    [],
    name='AutoDebugTool_v1.2.6',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\WorkSpace\\ScriptToolsWorkSpace\\PyWorkSpace\\My_project\\ICO\\brands_designer.ico'],
)
