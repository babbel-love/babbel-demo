from setuptools import setup, find_packages

setup(
    name='babbel-core',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai',
        'pytest',
        'black',
        'isort',
        'PyQt6'
    ],
    entry_points={
        'console_scripts': [
            'babbel-run=babbel.core.engine:main'
        ]
    },
    include_package_data=True,
    zip_safe=False
)

