from setuptools import setup

setup(
    name='eleksdrawpy',
    version='0.1',
    description='Library for working with the EleksDraw plotter.',
    packages=['eleksdrawpy'],
    install_requires=['pyserial', 'shapely', 'pyhull', 'cairocffi'],
    license='MIT'
)

