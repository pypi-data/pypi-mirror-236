from setuptools import setup, find_packages

setup(
    name='ExpertOptionAPI',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # list your package dependencies here
        "urllib",
        "websocket",
        "simplejson"
    ],
)
