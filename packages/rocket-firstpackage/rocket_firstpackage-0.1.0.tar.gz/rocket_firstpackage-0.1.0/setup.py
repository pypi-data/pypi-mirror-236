from setuptools import setup

setup(
 name='rocket_firstpackage',
 version='0.1.0',
 author='SENKADI Khawla',
 author_email='k.senkadi@esi-sba.dz',
 packages=['rocket_firstpackage', 'rocket_firstpackage'],
 url='http://pypi.python.org/pypi/rocket_firstpackage/',
 license='LICENSE.txt',
 description='An awesome package that does something',
 long_description=open( 'README.md').read(),
 install_requires=[
     "pandas == 0.20.3",
     "pytest",
 ],
)
