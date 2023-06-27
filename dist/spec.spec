# -*- mode: python -*-

block_cipher = None


a = Analysis(['GCE_downloader_ver1.05.pyw'],
             pathex=['C:/Users/13931/AppData/Local/Programs/Python/Python39/Scripts/dist'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('icon.ico','C:/Users/13931/AppData/Local/Programs/Python/Python39/Scripts/dist/icon.ico', "DATA"),
            ('eegg.png', 'C:/Users/13931/AppData/Local/Programs/Python/Python39/Scripts/dist/eegg.png', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GCE downloader gui',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          version='version.rc',
          icon='C:/Users/13931/AppData/Local/Programs/Python/Python39/Scripts/dist/icon.ico')