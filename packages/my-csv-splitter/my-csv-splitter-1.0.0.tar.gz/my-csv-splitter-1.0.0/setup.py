from setuptools import setup

setup(
    name="my-csv-splitter",
    version="1.0.0",
    author="Your Name",
    description="A tool to split CSV files",
    py_modules=["main"],
    install_requires=[
        'click',
    ],
    entry_points={
        "console_scripts": [
            "csv-splitter = main:split_csv",
        ],
    },
)
