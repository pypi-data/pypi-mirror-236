import pathlib
from distutils.core import setup

WD = pathlib.Path(__file__).parent
README = (WD / "README.md").read_text()
setup(
    name="pyodcollect",
    version="1.1.0",
    description="Get real time odour observations from OdourCollect's Citizen Observatory",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ScienceForChange/pyodcollect",
    author="Alex Amo (OdourCollect) and Ana Álvarez (COS4CLOUD)",
    author_email="alex.amo@scienceforchange.eu",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
    ],
    packages=["pyodcollect"],
    package_dir={"pyodcollect": "src/pyodcollect"},
    include_package_data=True,
    install_requires=["requests", "pydantic", "haversine", "openpyxl"],
    entry_points={
        "console_scripts": [
            "odourcollect=pyodcollect.command_line:main",
        ]
    },
)
