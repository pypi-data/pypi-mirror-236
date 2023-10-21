from setuptools import setup, find_packages

setup(
    name="potatomagical",
    version="0.1",
    packages=find_packages(),
    author="Prabhu Kasinathan",
    author_email="vasuramprabhu@gmail.com",
    description="A simple magic package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="http://github.com/pkasinathan/potatomagical",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
