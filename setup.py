from setuptools import setup, find_packages
import re

VERSIONFILE="duckysvc/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
	# Application name:
	name="duckysvc",

	# Version number (initial):
	version=verstr,

	# Application author details:
	author="Tamas Jos",
	author_email="info@skelsecprojects.com",

	# Packages
	packages=find_packages(),

	# Include additional files into the package
	include_package_data=True,


	# Details
	url="https://github.com/skelsec/duckysvc",

	zip_safe = False,
	#
	# license="LICENSE.txt",
	description="WS service for rubberducky scripts to usb keyboard",
	long_description="WS service for rubberducky scripts to usb keyboard",

	# long_description=open("README.txt").read(),
	python_requires='>=3.7',
	classifiers=(
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	),
	install_requires=[
		'websockets',
		# duckencoder would be here if it had a pip package
	],
	entry_points={
		'console_scripts': [
			'duckysvc = duckysvc.__main__:main',
		],
	}
)