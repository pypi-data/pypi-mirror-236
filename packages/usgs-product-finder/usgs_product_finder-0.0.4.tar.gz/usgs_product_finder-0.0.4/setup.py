from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# get version from env var called TAG_NAME
VERSION = os.environ.get("TAG_NAME", "0.0.3")
DESCRIPTION = 'USGS Finder Utility that finds USGS datasets based on a user input'
LONG_DESCRIPTION = 'USGS Finder Utility that finds USGS datasets based on a user input'

# Setting up
setup(
    name="usgs_product_finder",
    version=VERSION,
    author="Ivica Matic",
    author_email="<ivica.matic@spatialdays.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={'usgs_product_finder': ['files/*.geojson']},
    install_requires=["requests==2.31.0",
                      "shapely==2.0.2",
                      "pandas==2.1.1",
                      "geopandas==0.14.0"
                      ],
    keywords=['usgs', 'landsat', 'satellite'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
