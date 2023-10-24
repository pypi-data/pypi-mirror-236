from pathlib import Path

from setuptools import find_namespace_packages, setup

actual_path = Path(__file__).parent.resolve()

long_description = (actual_path / "README.md").read_text(encoding="utf-8")

main_ns = {}
with open("qurix/data/catalog/__version__.py", "r") as file_handler:
    exec(file_handler.read(), main_ns)

setup(
    name="qurix-data-catalog",
    version=main_ns["VERSION"],
    author="qurix Technology",
    license_files=("LICENSE"),
    description="qurix Data catalog client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qurixtechnology/qurix-data-catalog",
    packages=find_namespace_packages(),
    install_requires=[
        "Cython",
        "pandas",
        "annotated-types==0.5.0",
        "autopep8==2.0.2",
        "connectorx==0.3.2",
        "et-xmlfile==1.1.0",
        "iniconfig==2.0.0",
        "numpy==1.25.2",
        "openpyxl==3.1.2",
        "packaging==23.1",
        "pluggy==1.2.0",
        "pyarrow==12.0.1",
        "pycodestyle==2.11.0",
        "pydantic==2.1.1",
        "pydantic_core==2.4.0",
        "pytest==7.4.0",
        "python-dateutil==2.8.2",
        "pytz==2023.3",
        "six==1.16.0",
        "typing_extensions==4.7.1",
        "tzdata==2023.3",
        "XlsxWriter",
        "python-dotenv",
        "sqlalchemy",
        "ibm_db_sa"
    ],
    extras_require=dict(
        dev=[
            "pytest==7.3.1",
            "flake8==6.0.0",
            "pytest-flake8==1.1.1",
            "pytest-cov==4.0.0",
            "wheel==0.40.0",
            "twine==4.0.2",
        ]
    ),
    python_requires=">=3.10, <4",
    keywords=["python"],
)
