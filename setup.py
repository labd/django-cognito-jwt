from setuptools import find_packages, setup

install_requires = [
    "Django>=4.2",
    "cryptography",
    "djangorestframework",
    "pyjwt",
    "requests",
]

docs_require = [
    "sphinx>=1.4.0",
]

tests_require = [
    "coverage[toml]>=7.6",
    "pytest>=8.3",
    "pytest-django>=4.9",
    "pytest-cov>=6.0",
    "pytest-responses>=0.5.1",
    # Linting
    "ruff",
]

setup(
    name="django-cognito-jwt",
    version="0.0.4",
    description="Django backends for AWS Cognito JWT",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/LabD/django-cognito-jwt",
    author="Michael van Tellingen",
    author_email="m.vantellingen@labdigital.nl",
    python_requires=">=3.11",
    install_requires=install_requires,
    extras_require={"docs": docs_require, "test": tests_require,},
    use_scm_version=True,
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    zip_safe=False,
)
