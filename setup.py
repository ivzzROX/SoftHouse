from setuptools import setup, find_packages

PACKAGE_NAME = 'server'
PACKAGE_VERSION = '0.1'
INSTALL_REQUIRES = [
    'flask',
    'Flask-RESTful',
    'python-telegram-bot'
]

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=('Bot for light control',),
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES
)
