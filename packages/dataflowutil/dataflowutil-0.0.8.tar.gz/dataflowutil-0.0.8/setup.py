from setuptools import setup


with open("README.md","r",encoding="utf-8") as wa:
    long_description = wa.read()

setup(
    name = "dataflowutil",
    version = "0.0.8",
    author="Felipe Ardila (WorldArd)",
    description="",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["dataflowutil.config","dataflowutil.libs"],
    install_requires = [
        "pandas==1.5.0",
        "pandas-gbq==0.19.2",
        "google-cloud-storage==2.10.0",
        "openpyxl==3.1.2",
        "fsspec==2023.6.0",
        "gcsfs==2023.6.0",
        "levenshtein==0.21.1",
        "google-api-python-client==2.100.0",
        "ipywidgets==8.1.1",
        "google-cloud-bigquery-datatransfer==3.12.1",
        "dash==2.14.0",
        "dash_bootstrap_components==1.5.0"
    ],
)