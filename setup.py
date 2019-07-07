from setuptools import setup

# Credit to qwertyquerty for this setup file.
with open('README.md') as f:
    long_description = f.read()

# https://setuptools.readthedocs.io/en/latest/setuptools.html
setup(name='DiscordRPC.py',
      author='LBots',
      url='https://github.com/lbots/DiscordRPC.py',
      version='1.0.0',
      packages=['discordrpc'],
      python_requires='>=3.5',
      platforms=['Windows', 'Linux', 'OSX'],
      zip_safe=True,
      license='MIT',
      description='Complete Discord RPC interface written in Python',
      long_description=long_description,
      # PEP 566, PyPI Warehouse, setuptools>=38.6.0 make markdown possible
      long_description_content_type='text/markdown',
      keywords='discord rich presence discordrpc discordrpc.py rpc api interface richpresence irc',

      # Used by PyPI to classify the project and make it searchable
      # Full list: https://pypi.org/pypi?%3Aaction=list_classifiers
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: MIT License',

            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',

            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: Implementation :: CPython',

            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: Communications :: Chat',
            'Framework :: AsyncIO',
      ]
)
