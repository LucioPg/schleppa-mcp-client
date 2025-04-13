from setuptools import setup, find_packages


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "Pypi-README.md").read_text()


setup(
    name="python-mcp-client",
    version="0.1.2",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "mcp>=0.0.1",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.1",
        "langchain-mcp-adapters>=0.0.1",
        "langgraph>=0.0.1",
        "flask>=2.0.0",
    ],
)

