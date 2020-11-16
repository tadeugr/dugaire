from setuptools import setup

setup(
    name='dugaire',
    version='0.0.1',
    py_modules=['dugaire'],
    install_requires=[
        'docker'
    ],
    entry_points='''
        [console_scripts]
        dugaire=main:main
    '''
)