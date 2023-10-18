# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="volcengine-avatar-live",
    version="1.0.8",
    description=("SDK for Volcengine Avatar Live"),
    long_description=open("README.rst", encoding="utf-8").read(),
    author="Tingshuo Chen",
    author_email="chentingshuo@bytedance.com",
    license="Apache 2.0",
    packages=find_packages(include=["volcengine_avatar_live*"]),
    platforms=["all"],
    install_requires=[
        "requests>=2.27.1",
        "websockets>=11.0.3",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)
