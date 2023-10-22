from setuptools import setup, find_packages

setup(
    name="uvatradier",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "dotenv",
        "requests",
        "numpy",
        "pandas",
        "schedule"
    ],
    author="Tom Hammons",
    author_email="qje5vf@virginia.edu",
    description="wahoowah",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/thammo4/uvatradier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
