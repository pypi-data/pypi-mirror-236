from setuptools import setup

version = '1.0.3'
long_dcs = '''Это модуль для взаимодействия с API WDonate'''

setup(
    name = 'wdonate',
    version=version,
    author='Hleb2702',
    author_email='glebstetko2@gmail.com',

    description=long_dcs,
    long_description=long_dcs,
    url='https://github.com/hleb2702/wdonate_python.git',

    download_url=f'https://github.com/hleb2702/wdonate_python/archive/refs/tags/wdonate.zip',

    license='Apache License, Version 2.0, see LICENSE file',
    packages=['wdonate'],
    requires=['requests', 'random']
)

