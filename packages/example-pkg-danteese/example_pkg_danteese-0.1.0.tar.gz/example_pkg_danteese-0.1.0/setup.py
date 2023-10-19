from setuptools import find_packages
from setuptools import setup
setup(
    name="example_pkg_danteese",
    version="0.1.0",
    description="A example Python package",
    url="https://github.com/danteese/example-package",
    author="Dante B",
    author_email="dalnte@me.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: BSD/OS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.9",
    ],
)
