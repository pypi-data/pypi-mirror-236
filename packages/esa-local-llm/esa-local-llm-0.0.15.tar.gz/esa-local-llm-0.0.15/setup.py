from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(this_directory, "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="esa-local-llm",
    version="0.0.15",
    description="ESA Local-LLM is a llama.cpp server in Docker with OpenAI Style Endpoints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Cloutier",
    author_email="michael.cloutier@experian.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=requirements,
)
