from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="aifast",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.8",
    author="Rohit Bhattacharjee",
    author_email="rohitb7uw@gmail.com",
    description="A fast and flexible AI interface library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
