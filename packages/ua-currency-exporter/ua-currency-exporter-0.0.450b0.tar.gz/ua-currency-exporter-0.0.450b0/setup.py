from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="ua-currency-exporter",
    version='v0.0.450-beta',
    author="Maxim Shaposhnikov",
    author_email="shaposhnikoff@gmail.com",
    description="Currency exporter package for Prometeus",
    url = "https://github.com/shaposhnikoff/ua-currency-exporter",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['boto3','requests', 'prometheus_client', 'pyyaml', 'python-dateutil', 'pytz', 'tzlocal', 'urllib3'],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
