# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['..\\AutoDebugTool.py'],
    pathex=[
        '..\\Config',
        '..\\JsCreator',
        '..\\Libs',
        '..\\Licenses',
        '..\\Logger',
        '..\\Monitor',
        '..\\Opt',
        '..\\RootManage',
        '..\\suitetest'
    ],
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
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AutoDebugTool_v1.2.7(License to 2025-01-01)',
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
    icon=['D:\\WorkSpace\\ScriptToolsWorkSpace\\PyWorkSpace\\My_project\\ICO\\slack.ico'],
)
