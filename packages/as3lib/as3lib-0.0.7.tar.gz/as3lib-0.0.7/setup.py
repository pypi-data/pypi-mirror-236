from setuptools import setup, find_packages

with open("README.md", "r") as ld:
      long_desc = ld.read()

setup(name="as3lib",
      version="0.0.7",
      author="ajdelguidice",
      author_email="ajdelguidice@gmail.com",
      url="https://github.com/ajdelguidice/python-as3lib",
      description="Python implementation of ActionScript3",
      long_description=long_desc,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.10",
            "Topic :: Utilities",
            ],
      python_requires=">=3.10",
      install_requires=["numpy","tkhtmlview","Pillow"],
      )
