import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="MapleStoryPython",
    version="2.0.0",
    author="skyAllen",
    author_email="894982165@qq.com",
    description="No description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a405457747/MapleStoryPython",
    packages=setuptools.find_packages(),
    install_requires=[''],
    extras_require={
        #'ocr': ['cnocr>=2.2.2.1']
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
