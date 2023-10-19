from setuptools import setup

setup(
    name='intra42',
    version='0.2',
    description='Intra 42 public and private api interface',
    url='https://github.com/Xentiie/intra42',
    author='Rémi Claire',
    author_email='reclaire@student.42mulhouse.fr',
    license='BSD 2-clause',
    packages=['intra42'],
    install_requires=['requests',
                      'bs4',],
    classifiers=[],
)
