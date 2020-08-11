from setuptools import setup, find_packages

setup(
    name='miot-rf433',
    version='0.0.1',
    author='Matt Continisio',
    author_email='mrcontinisio@gmail.com',
    license='MIT',
    url='https://github.com/mattcontinisio/meat-curing-chamber',
    keywords='raspberry pi iot fridge meat curing chamber rf433',
    packages=find_packages(exclude=['doc', 'test']),
    install_requires=open("requirements.txt", "r").read().split("\n"),
    #install_requires=['paho-mqtt>=1.5.0', 'schema>=0.6.8'],
    entry_points={
        'console_scripts': [
            'miot-humidity-controller=rf433.humidity_controller:main',
            'miot-temperature-controller=rf433.temperature_controller:main',
            'miot-rf433=rf433.rf433_service:main',
        ],
    },
    zip_safe=True)
