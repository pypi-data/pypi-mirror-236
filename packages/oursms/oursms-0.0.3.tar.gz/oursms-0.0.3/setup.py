import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requires = [
    "requests==2.31.0",
    "urllib3==2.0.7",
    "certifi==2023.7.22",
    "charset-normalizer==3.3.0",
    "python-dateutil==2.8.2",
    "six==1.16.0",
    "jsonpickle==3.0.2",
]

setuptools.setup(
    name="oursms",
    version="0.0.3",
    description="Oursms API client",
    author="Abdullah Alaidrous",
    author_email="abd.alaidrous@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abdroos/oursms",
    package_dir={"oursms": "oursms"},
    python_requires=">=3.6",
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
