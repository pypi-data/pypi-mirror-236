from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('LICENSE', 'r', encoding='utf-8') as f:
    license_text = f.read()

setup(
    name='netix',
    version='1.11',
    description="Netix is a high-performance ASGI (Asynchronous Server Gateway Interface) server designed for efficiently serving ASGI web applications and APIs. It offers a robust, customizable, and easy-to-use platform for deploying your ASGI applications.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pawan kumar',
    author_email='embrakeproject@gmail.com',
    url='https://github.com/embrake/netix/',
    packages=find_packages(),
    keywords='ASGI Server user-friendly high concurrancy',
    license='MIT',
    install_requires=['psutil', 'schedule'],  
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    entry_points={
        'console_scripts': [
            'netix = netix.script:main',
        ],
    },
)