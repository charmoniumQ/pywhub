# Copyright (c) 2022 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path

from setuptools import setup

from whub.version import VERSION

THIS_DIR = Path(__file__).absolute().parent

setup(
    name="pywhub",
    version=VERSION,
    url="https://github.com/crs4/pywhub",
    description="Interaction with the WorkflowHub API",
    long_description=(THIS_DIR / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Simone Leo",
    author_email="<simone.leo@crs4.it>",
    license="MIT",
    platforms=["Linux"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
    ],
    packages=["whub"],
    python_requires=">=3.6, <4",
    install_requires=["requests"],
    zip_safe=True,
)
