from setuptools import setup, find_packages

VNU = 1
VERSION = f'0.0.{VNU}'
README = ''
with open("README.md", "r", encoding="utf-8") as fh:
    README = fh.read()

setup(name="pywlf",
      version=VERSION,
      keywords=["log", "file", "date", "ssh", "core", "influxdb", "mysql", "redis", "minio", "kafka", "http"],
      description="Common utils for python3.",
      long_description=README,
      long_description_content_type="text/markdown",
      license="MIT Licence",
      url="https://github.com/waisaa/tools-python3-wlf",
      author="waisaa",
      author_email="waisaa@qq.com",
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      python_requires='>=3.7',
      install_requires=['colorlog==6.6.0', 'influxdb==5.3.1', 'PyMySQL==1.0.2', 'paramiko==2.11.0', 'minio==7.1.9', 'redis==3.2.0'])
