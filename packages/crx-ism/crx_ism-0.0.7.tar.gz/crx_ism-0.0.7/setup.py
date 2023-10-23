from setuptools import setup, find_packages

with open("crx_ism/README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="crx_ism",  # Replace with your own username
    version="0.0.7",
    author="ryukyungjoon",
    author_email="ryuryukj6663@gmail.com",
    description="image_sim",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['image-similarity-measures'],
    packages=find_packages(include=['crx_ism']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
