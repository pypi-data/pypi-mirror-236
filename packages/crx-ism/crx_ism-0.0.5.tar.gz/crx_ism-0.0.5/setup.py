from setuptools import setup, find_packages

# setup(
#     name='crx_ism',
#     version='0.0.1',
#     install_requires=['numpy', 'scikit-image', 'opencv-python', 'phasepack', 'image-similarity-measures'],
#     packages=find_packages(exclude=[]),
#     python_requires='>=3.6',
#     zip_safe=True,
#     classifiers=[
#         'Programming Language :: Python :: 3.9',
#     ],
# )

with open("crx_ism/README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="crx_ism",  # Replace with your own username
    version="0.0.5",
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
