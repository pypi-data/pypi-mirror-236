# setup.py

from setuptools import setup, find_packages

setup(
    name="aiv_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'elevenlabs',
        'Pillow',
        'openai',
    ],
)
