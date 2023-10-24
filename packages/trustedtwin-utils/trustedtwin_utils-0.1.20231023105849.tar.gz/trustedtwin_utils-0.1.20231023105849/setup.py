"""Create pypi package"""
import os

from setuptools import setup, find_packages

version = os.getenv('TRUSTED_TWIN_UTILS_VER')
if not version:
    raise AttributeError('Please export "TRUSTED_TWIN_UTILS_VER" environ.')


def _read_requirements():
    """Read requirements"""
    with open("requirements.txt", 'r') as f:
        return f.read().split()


setup(
    name='trustedtwin_utils',
    version=version,
    url='https://gitlab.com/trustedtwinpublic/trusted-twin-utils',
    long_description_content_type="text/markdown",
    license='MIT',
    author='Trusted Twin',
    description='Trusted Twin utils library',
    packages=find_packages(),
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=_read_requirements(),
    python_requires='>=3.9',
)
