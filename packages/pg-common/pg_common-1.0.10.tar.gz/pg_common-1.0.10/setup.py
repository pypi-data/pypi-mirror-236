from setuptools import setup
from pg_common import VERSION

DIST_NAME = "pg_common"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=VERSION,
	description="python game: common lib",
	packages=['pg_common'],
	author=__author__,
	python_requires='>=3.5',
	install_requires=[
		'pycrypto==2.6.1',
		'pydantic==1.10.11',
		'sshtunnel==0.4.0',
        'redis>=4.6.0',
		'prettytable==3.9.0',
	]
)
