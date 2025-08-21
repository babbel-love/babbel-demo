from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['babbel_core'],
    'includes': ['PyQt6'],
    'iconfile': None,
    'plist': {
        'CFBundleName': 'Babbel',
        'CFBundleDisplayName': 'Babbel',
        'CFBundleIdentifier': 'com.babbel.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '11.0',
        'NSHighResolutionCapable': True,
    },
}

setup(
    app=APP,
    name='Babbel',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
