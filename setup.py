from pathlib import Path
from setuptools import setup

long_description = (Path(__file__).parent / 'README.md').read_text('utf-8') #.split('# Installation')[0]

setup(
    name='discord-to-postgresql',
    version='0.1.2',
    description='Imports Discord messages archive to PostgreSQL database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/carlaraya/discord-to-postgresql',
    author='Carl Araya',
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    packages=['discord_to_postgresql'],
    include_package_data=True,
    install_requires=[
        'fire',
        'numpy',
        'pandas',
        'sqlalchemy',
        'psycopg2-binary'
    ],
    entry_points={
        'console_scripts': [
            'discord_to_postgresql=discord_to_postgresql.__main__:main',
        ]
    },
)
