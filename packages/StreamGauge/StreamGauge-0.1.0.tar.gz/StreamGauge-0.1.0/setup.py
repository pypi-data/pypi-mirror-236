from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="StreamGauge",
    version="0.1.0",
    author="Derek Evans",
    author_email="derek.evans@deinfoservice.com",
    description="Gauge Chart",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.techbyderek.com/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 0.63",
        "plotly",
        "pathlib",
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest",
            "playwright",
            "requests",
        ]
    }
)
