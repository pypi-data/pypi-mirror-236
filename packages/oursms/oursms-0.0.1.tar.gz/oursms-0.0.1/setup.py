import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setuptools.setup(
    name="oursms",
    version="0.0.1",
    description="Oursms API client",
    author="Abdullah Alaidrous",
    author_email="abd.alaidrous@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abdroos/oursms",
    package_dir={"": "oursms"},
    python_requires=">=3.6",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
