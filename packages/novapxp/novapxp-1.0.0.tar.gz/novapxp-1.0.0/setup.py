
from setuptools import setup, find_packages
with open("README.md", "r") as f:
    long_description = f.read()

# Some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
]

# Calling the setup function
setup(
    name='novapxp',
    version='1.0.0',
    description='new calculator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='xodevog135',
    author_email='xodevog135@vinthao.com',
    license='MIT',
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    keywords='your, keywords, here',
    scripts=['novapxp.py'],
)
