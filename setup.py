from setuptools import setup

setup(
    name='hito-koto-diary',
    description="ヒトコト日記 - Google Spreadsheet に対しての読み込み、書き込み操作を行う",
    version='1.0.0',
    install_requires=['httplib2', 'google-api-python-client', 'oauth2client'],
    packages=['hitokoto', 'hitokoto.google', 'hitokoto.config', 'hitokoto.credentials'],
    entry_points={
        'console_scripts': [
            'hitokoto=hitokoto.hito_koto_diary:main',
        ],
    }
)
