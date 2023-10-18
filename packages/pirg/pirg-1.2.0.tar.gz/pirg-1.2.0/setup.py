from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="pirg",
    version="1.2.0",
    packages=find_packages(),
    description="command-line tool that simplifies the management of project's `requirements.txt` file",
    long_description_content_type="text/markdown",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    url="https://github.com/kokoteen/pirg",
    author="kokotin",
    entry_points={
        "console_scripts": [
            "pirg = pirg.pirg:main",
        ],
    },
    install_requires=["typer[all]==0.9.0", "requests==2.31.0", "packaging==23.2"],
    python_requires=">=3.8",
)
