from setuptools import setup, find_packages
import os

VERSION = '0.0.6'
DESCRIPTION = 'Easily cut the video by moviepy'

setup(
    name="qianqiuvideo",
    version=VERSION,
    author="chunlei li",
    author_email="li_cl@foxmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    url="https://github.com/chunleili/cut_video",
    scripts=['qianqiuvideo/test.py'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)