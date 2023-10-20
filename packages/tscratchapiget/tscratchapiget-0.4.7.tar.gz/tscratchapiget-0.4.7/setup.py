from setuptools import setup, find_packages

VERSION = '0.4.7'
DESCRIPTION = "A library can get scratch's api"

# Setting up
setup(
    name="tscratchapiget",
    version=VERSION,
    author="Tony",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=["json", "requests", "webbrowser"],
    keywords=['scratchapi', 'scratchapiget', 'scratch', 'tscratchapiget', 'api'],
    url='https://github.com/Tony14261/tscratchapiget',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)