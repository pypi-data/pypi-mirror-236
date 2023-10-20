from distutils.core import  setup
import setuptools
packages = ['add_ab']# 唯一的包名，自己取名
setup(name='senemail',
	version='1.0',
	author='CYF',
    packages=packages, 
    package_dir={'requests': 'requests'},)