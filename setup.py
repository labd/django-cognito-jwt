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
    "coverage[toml]==7.8.2",
    "pytest==8.4.0",
    "pytest-django==4.11.1",
    "pytest-cov==6.1.1",
    "pytest-responses==0.5.1",
    # Linting
    "isort[pyproject]==4.3.21",
    "flake8==3.7.9",
    "flake8-imports==0.1.1",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==3.1.0",
]

setup(
    name="django-cognito-jwt",
    version="0.0.4",
    description="Django backends for AWS Cognito JWT",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/LabD/django-cognito-jwt",
    author="Michael van Tellingen",
    author_email="m.vantellingen@labdigital.nl",
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
        "Framework :: Django :: 1.11",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
