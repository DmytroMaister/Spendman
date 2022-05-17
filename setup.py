from setuptools import setup

APP_NAME = 'Spendman'
APP = ['app.py']
DATA_FILES = [
    ('database',['database/database.db'])
]
OPTIONS = {
    'packages': ['babel', 'pytz'],
    'iconfile': 'icon.icns',
    'argv_emulation': True,
}

setup(
    app=APP,
    name = APP_NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)