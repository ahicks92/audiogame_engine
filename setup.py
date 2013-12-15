from setuptools import setup, find_packages
from glob import glob

__version__ = 0.1

setup(
 name = 'game_engine',
 version = __version__,
 description = """A basic game event loop and window""",
 package_dir = {'game_engine': 'game_engine'},
 packages = find_packages(),
)