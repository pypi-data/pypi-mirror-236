from setuptools import setup, find_packages

setup(
    name="lrts",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pyzmq',
    ],
    extras_require={
        'detailed_progress': ['enlighten', 'loguru']
    },
    entry_points={
        'console_scripts': [
            'lrts=lrts.cli:main'
        ]
    },
    author="Robert Engen",
    author_email="rnengen@gmail.com",
    description="A python distributed task computation library.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RobertEngen/lrts"
)
