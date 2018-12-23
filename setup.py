from setuptools import setup

setup(
    name='xy',
    version='0.1',
    description='Library for working with the EleksDraw plotter.',
    packages=['xy'],
    install_requires=['pyserial', 'shapely', 'pyhull', 'cairocffi'],
    license='MIT'
)

