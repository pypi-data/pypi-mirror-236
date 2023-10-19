from distutils.core import setup

setup(name='ActivityStream',
      version='0.4.1',
      url='http://sf.net/p/activitystream',
      packages=['activitystream', 'activitystream.storage'],
      install_requires=['pymongo>=2.8'],
      python_requires='>=3.8',
      license='Apache License, http://www.apache.org/licenses/LICENSE-2.0',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'License :: OSI Approved :: Apache Software License',
          ],
      )
