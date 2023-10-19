from setuptools import setup
from pg_environment import VERSION

DIST_NAME = "pg_environment"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=VERSION,
	description="python game: environment",
	packages=['pg_environment'],
	author=__author__,
	python_requires='>=3.5',
	install_requires=[
		'pg-common>=0'
	],
)
