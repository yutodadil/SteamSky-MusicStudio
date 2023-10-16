# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
import kivymd.icon_definitions
from pathlib import Path

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("assets/fonts/*", "assets/fonts"),
        ("assets/config/*", "assets/config"),
        ("kv/*", "kv"),
    ],
    hiddenimports=["kivymd"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

kmd_icondefs = kivymd.icon_definitions.__file__
a.datas.append((
    str(Path("kivymd").joinpath(Path(kmd_icondefs).name)),
    kmd_icondefs,
    "DATA"
))

print(a.datas)

exe = EXE(
    pyz,
    Tree("./src"),
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    [],
    name='SkyMusicStudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,    # Set this to `True` to enable console for logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
