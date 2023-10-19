from setuptools import setup
from geeznum import __version__


setup(
	name="geeznum",
	author="Natanim Negash",
	author_email="natanimn@yahoo.com",
	url="https://github.com/natanimn/GeezNumber",
	description="A python package that converts arabic number to geez number",
	long_description="\n"+open("README.md", encoding="utf-8").read(),
	version=__version__,
	long_description_content_type='text/markdown',
	keywords=["number", "geez number", "number convertor", "python number", 'geez'],
	license="MIT"
)