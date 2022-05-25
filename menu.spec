# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
venv=r'D:\python\envs\k-4-25-1\Lib'

a = Analysis(['menu.py'],
             pathex=[],
             binaries=[],
             datas=[
             (r'.\gui\ui_svg','./gui/ui_svg'),
             
             (venv+r'\site-packages\librosa\util\example_data\index.json',
      './librosa/util/example_data'),

     (venv+r'\site-packages\librosa\util\example_data\registry.txt',
      './librosa/util/example_data'),

      (venv+r'\site-packages\tqdm-4.64.0.dist-info',
      './tqdm-4.64.0.dist-info'),
      
      (venv+r'\site-packages\regex-2022.4.24.dist-info',
      './regex-2022.4.24.dist-info'),
      
      (venv+r'\site-packages\sacremoses-0.0.49.dist-info',
      './sacremoses-0.0.49.dist-info'),
      
      (venv+r'\site-packages\requests-2.27.1.dist-info',
      './requests-2.27.1.dist-info'),
      
      (venv+r'\site-packages\packaging-21.3.dist-info',
      './packaging-21.3.dist-info'),
      
      (venv+r'\site-packages\filelock-3.6.0.dist-info',
      './filelock-3.6.0.dist-info'),
      
      (venv+r'\site-packages\numpy-1.21.6.dist-info',
      './numpy-1.21.6.dist-info'),
      
      (venv+r'\site-packages\tokenizers-0.12.1.dist-info',
      './tokenizers-0.12.1.dist-info'),

      (venv+r'\site-packages\transformers',
      './transformers'),

      (venv+r'\site-packages\vosk',
       './vosk'),

      ],
             hiddenimports=['sklearn.utils._typedefs','sklearn.neighbors._partition_nodes','pyannote.audio.models','pyannote.audio.models.segmentation',' importlib._bootstrap'],
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
          name='menu',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon = r'.\create\logo.ico',
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
               name='menu')
