from setuptools import setup

import swiftlogging

setup(name='swift_logging',
      version=swiftlogging.version,
      description='Middleware for swift logging system',
      license='Apache License (2.0)',
      author='a2company',
      author_email='admin@a2company.co.kr',
      packages=['swiftlogging'],
      install_requires=['swift >= 1.13.0'],
      entry_points={'paste.filter_factory':
                        ['swift_logging='
                         'swiftlogging.middleware:filter_factory']})
