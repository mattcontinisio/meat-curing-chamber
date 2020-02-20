from setuptools import setup, find_packages

setup(name='miot-csv-writer',
      version='0.0.1',
      author='Matt Continisio',
      author_email='mrcontinisio@gmail.com',
      license='MIT',
      url='https://github.com/mattcontinisio/meat-curing-chamber',
      keywords='raspberry pi iot fridge meat curing chamber csv',
      packages=find_packages(exclude=['doc', 'test']),
      install_requires=open("requirements.txt", "r").read().split("\n"),
      entry_points={
          'console_scripts': ['miot-csv-writer=csv_writer.csv_writer:main'],
      },
      zip_safe=True)
