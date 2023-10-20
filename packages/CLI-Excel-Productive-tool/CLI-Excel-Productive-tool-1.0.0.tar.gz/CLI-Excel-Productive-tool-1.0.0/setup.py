from setuptools import setup

setup(
    name='CLI-Excel-Productive-tool',
    version='1.0.0',
    py_modules=['main'],
    install_requires=[
        'pyfiglet',
        'tqdm',
        'inquirer',
        'yaspin',
        'rich',
    ],
    entry_points='''
        [console_scripts]
        CLI-Excel-Productive-tool=main:main
    ''',
)
