from setuptools import setup, find_packages


setup(
    name="dj_loguru",
    version="0.1.0",
    description="Use loguru in Django.",
    author="Stephen Ling",
    author_email="shiyun.ling@flexiv.com",
    keywords=["Django", "loguru"],
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["loguru>=0.5.3", "Django>=3.2"],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Django Web Developers",
        "Topic :: Software Development :: Logging",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
