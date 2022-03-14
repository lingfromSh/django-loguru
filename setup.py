from setuptools import setup, find_packages

setup(
    name="dj_loguru",
    version="0.2.1",
    description="Use loguru in Django.",
    author="Stephen Ling",
    author_email="lingfromsh@163.com",
    url="https://github.com/lingfromSh/django-loguru",
    keywords=["Django", "loguru"],
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["loguru>=0.5.3", "Django>=3.2"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
