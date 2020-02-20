from setuptools import setup, find_packages

setup(
    name='miot-dht',
    version='0.0.1',
    author='Matt Continisio',
    author_email='mrcontinisio@gmail.com',
    license='MIT',
    url='https://github.com/mattcontinisio/meat-curing-chamber',
    keywords='raspberry pi iot fridge meat curing chamber dht sensor',
    packages=find_packages(exclude=['doc', 'test']),
    install_requires=open("requirements.txt", "r").read().split("\n"),
    #install_requires=['paho-mqtt>=1.5.0', 'schema>=0.6.8'],
    entry_points={
        'console_scripts': ['miot-dht=dht.dht:main'],
    },
    zip_safe=True)
