# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['SpeechSplit.py'],
             pathex=[],
             binaries=[],
             datas=[('D:\\python\\envs\\ASR-3-14-2\\Lib\\site-packages\\librosa\\util\\example_data\\index.json',
      './librosa/util/example_data'),
     ('D:\\python\\envs\\ASR-3-14-2\\Lib\\site-packages\\librosa\\util\\example_data\\registry.txt',
      './librosa/util/example_data')],
             hiddenimports=['sklearn.utils._typedefs','sklearn.neighbors._partition_nodes','pyannote.audio.models','pyannote.audio.models.segmentation'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='SpeechSplit',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SpeechSplit')
