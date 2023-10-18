from setuptools import setup, find_packages

setup(
    name="fcast_client",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g.
        # 'requests',
    ],
    author="cassdev",
    author_email="admin@cassdev.com",
    description="A Python client wrapper for the video streaming receiver Fcast.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/developer90210brr/fcast-wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
