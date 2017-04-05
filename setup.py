from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='smartinput',
      version='0.1',
      description='smart input of user data in cmd interfaces, like raw_input only smarter',
      long_description=readme(),
      url='',
      author='Vinzenz G Eck',
      author_email='vinzenz.g.eck@ntnu.no',
      classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      license='MIT',
      packages=['smartinput'],
      install_requires=[], # add dependencies
      include_package_data=True,
      zip_safe=False)

