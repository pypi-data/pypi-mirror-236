from distutils.core import  setup
import setuptools
packages = ['cyf-sendemail']               # 唯一的包名，自己取名
setup(name='cyf-sendemail',
	version='1.0',
	author='CYF',
    packages=packages, 
    package_dir={'requests': 'requests'},)