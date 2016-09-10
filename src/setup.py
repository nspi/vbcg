from distutils.core import setup
import defines

setup(
    name='vbcg',
    version=defines.__version__,
    packages=[''],
    url=defines.__url__,
    license=defines.__license__,
    author=defines.__author__,
    author_email=defines.__email__,
    description=defines.__description__,
    install_requires=['scipy>=0.13.3',
                      'numpy>=1.8.2',
                      'matplotlib>=1.3.1',
                      'Pillow>=2.3.0',
                      'pyserial>=2.6'
                      ],

)
