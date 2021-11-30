# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['practice.py'],
             pathex=[],
             binaries=[],
             datas=[('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\Game_Pictures','Game_Pictures'),
             ('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\game_sound','game_sound'),
             ('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\saved_files','saved_files'),
             ('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\Speech_EN','Speech_EN'),
             ('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\words_pool','words_pool'),
             ('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\Fonts','Fonts'),
             ('C:\\Users\\srymkr\\PycharmProjects\\snake_game\\Words_phonetic','Words_phonetic')],
             hiddenimports=['Other_library', 'Snake_body_library', 'Snake_food_library', 'Snake_head_library', 'words_handling_library', 'word_phonetic_library', 'English_Vocabulary_Review', 'game_introducation'],
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
          name='practice',
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
               name='practice')
