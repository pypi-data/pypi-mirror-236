from setuptools import setup, find_packages

setup(
    name='netix',          # Package name
    version='1.0.0',       # Package version
    author='Pawan Kumar',
    description='Your package description',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'netix = netix.__main__:main',
        ],
    },
)
