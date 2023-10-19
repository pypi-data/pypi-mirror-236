import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nginx-updater",
    version="1.0.5",
    author="Pradish Bijukchhe",
    author_email="pradishbijukchhe@gmail.com",
    description="Python module updater that uses nginx as backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pradishb/nginx-updater",
    project_urls={
        "Bug Tracker": "https://github.com/pradishb/nginx-updater/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    package_dir={"nginx_updater": "nginx_updater"},
    python_requires=">=3",
    install_requires=["requests"],
)
