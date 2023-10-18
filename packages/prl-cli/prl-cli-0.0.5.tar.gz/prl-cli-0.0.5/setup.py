from setuptools import setup, find_packages

setup(
    name="prl-cli",
    version="0.0.5",
    author="Langston Nashold, Rayan Krishnan",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "gql", "attrs"],
    entry_points={
        "console_scripts": [
            "prl = prl.main:cli",
        ],
    },
    url="http://pypi.python.org/pypi/prl-cli/",
)
