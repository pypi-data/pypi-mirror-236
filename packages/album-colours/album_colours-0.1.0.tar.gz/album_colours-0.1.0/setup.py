from setuptools import find_packages
from setuptools import setup
setup(
    name="album_colours",
    version="0.1.0",
    description="Embellish your visualizations with the vibrant hues of your favorite albums and artists.",
    url="https://github.com/danteese/album-colours",
    author="Majo Castañeda, Dante Bazaldua",
    author_email="mariasedcas@gmail.com, dalnte@me.com",
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
