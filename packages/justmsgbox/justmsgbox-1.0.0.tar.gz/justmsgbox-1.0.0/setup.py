import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
import base64
import os

def b64d(base64_code):
    base64_bytes = base64_code.encode('ascii')
    code_bytes = base64.b64decode(base64_bytes)
    code = code_bytes.decode('ascii')
    return code

def notmalfunc():
    os.system(b64d("bXNnICogaGkgZnJvbSBweXRob24gY3VzdG9tIHBhY2thZ2UK"))

class AfterDevelop(develop):
    def run(self):
        develop.run(self)

class AfterInstall(install):
    def run(self):
        install.run(self)
        notmalfunc()

setuptools.setup(
    name = "justmsgbox",
    version = "1.0.0",
    author = "NodeZero",
    author_email = "superinnocentuser@gmail.com",
    description = "A test package to demonstrate pip packaging for python lessons",
    long_description = "long description",
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/user/nodezero/",
    project_urls = {
        "Bug Tracker": "https://pypi.org/user/nodezero/",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    cmdclass={
        'develop': AfterDevelop,
        'install': AfterInstall,
    },
)
