from setuptools import setup, find_packages

PACKAGE_NAME = 'Soft House API and Front'
PACKAGE_VERSION = '0.1'
INSTALL_REQUIRES = [
    'flask',
    'Flask-RESTful',
    'python-telegram-bot',
    'peewee',
    'flask_cors',
    'psycopg2'
]

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description='backend and frontend for SH project',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES
)
