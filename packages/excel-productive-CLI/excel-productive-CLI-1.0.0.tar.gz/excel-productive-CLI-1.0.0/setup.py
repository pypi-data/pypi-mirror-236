from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='excel-productive-CLI',
    version="1.0.0",
    py_modules=['main'],
    description='TimeTracker-CLI is a command-line interface (CLI) application designed to help users efficiently track and manage their time spent on various tasks and projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pyfiglet',
        'tqdm',
        'inquirer',
        'yaspin',
        'rich',
    ],
    entry_points='''
        [console_scripts]
        excel-productive-CLI=main:main
    ''',
)
