import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wzmlx-dl",
    version="1.0.14",
    author="weebzone",
    author_email="doc.adhikari@gmail.com",
    description="ZORO-DL - Download DUAL-AUDIO Multi SUBS Anime from ZORO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests", "beautifulsoup4", "tenacity", "yt-dlp",
    ],
    packages=setuptools.find_packages(),
    package_data={'wzmlx_dl': ['static/*']},
    python_requires=">=3.6",
)
