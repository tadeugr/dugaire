from setuptools import setup

config = {
    'description': 'Quickly build docker images with custom packages.',
    'author': 'Tadeu Granemann',
    'version': '0.0.1',
    'install_requires': ['click', 'docker'],
    'packages': ['dugaire'],
    'entry_points': {
        'console_scripts': ['dugaire=dugaire.dugaire:main'],
    },
    'name':'dugaire',
    'include_package_data':True
}

setup(**config)