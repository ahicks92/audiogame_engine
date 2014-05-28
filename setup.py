from setuptools import setup, find_packages
from glob import glob

__version__ = 0.1

setup(
	name = 'audiogame_engine',
	version = __version__,
	description = """A basic game event loop and window""",
	author = "Austin Hicks and Christopher Toth",
	license = "BSD",
	package_dir = {'audiogame_engine': 'audiogame_engine'},
	packages = find_packages(),
	zip_safe = False,
	package_data = {
		'audiogame_engine' : ['dlls/*.dll']
	},
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Topic :: Games/Entertainment',
	]
)
