from setuptools import setup, find_packages

setup(
    name="django_print_models",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.0",
    ],
    author="Mitchel Humpherys",
    author_email="mitch.special@gmail.com",
    description="A Django package to print trimmed down models for easier sharing.",
    keywords="django models print",
    url="https://github.com/mgalgs/django_print_models",
)
