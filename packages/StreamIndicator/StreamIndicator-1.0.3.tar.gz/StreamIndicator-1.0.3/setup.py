from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="StreamIndicator",
    version="1.0.3",
    author="Derek Evans",
    author_email="derek.evans@deinfoservice.com",
    description="Plotly Indicator Gauge Chart",
    long_description="Streamlit component for quickly deploying Plotly indicator gauge charts.",
    long_description_content_type="text/markdown",
    url="https://github.com/REPNOT/StreamIndicator",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
        "plotly==5.17.0"
    ],
    extras_require={
        "devel": [
            "wheel",
            "pytest==7.4.0",
            "playwright==1.36.0",
            "requests==2.31.0",
            "pytest-playwright-snapshot==1.0",
            "pytest-rerunfailures==12.0",
            "plotly==5.17.0"
        ]
    }
)
