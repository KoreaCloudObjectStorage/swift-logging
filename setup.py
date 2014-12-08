from setuptools import setup

import swiftelklogging

setup(name='swift_elk_logging',
      version=swiftelklogging.version,
      description='Middleware for logging to elk system',
      license='Apache License (2.0)',
      author='a2company',
      author_email='admin@a2company.co.kr',
      packages=['swiftelklogging'],
      install_requires=['swift >= 1.13.0'],
      entry_points={'paste.filter_factory':
                        ['swift_elk_logging='
                         'swiftelklogging.middleware:filter_factory']})
