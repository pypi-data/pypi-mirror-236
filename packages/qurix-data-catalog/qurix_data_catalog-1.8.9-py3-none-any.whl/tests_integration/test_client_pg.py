import subprocess

import pytest

from qurix.data.catalog.client import DataCatalogClient
from qurix.data.catalog.entities import CatalogDataSource

PG_PASS = "Welcome4$"
PG_USER = "pgsqldev"
PG_IMAGE = "postgres:latest"
PG_DB = "postgres"
CONTAINER_NAME = "postgressql"


@pytest.fixture
def empty_catalog_client() -> DataCatalogClient:
    return DataCatalogClient()


@pytest.fixture
def data_catalog_entry_postgres() -> CatalogDataSource:
    return CatalogDataSource(name="source f",
                             location="postgresql://pgsqldev:Welcome4$@localhost:5432/testdb",
                             business_partner="some partner",
                             table_schema="public",
                             table="dummy_data")


def test_load_postgres(empty_catalog_client: DataCatalogClient, data_catalog_entry_postgres: CatalogDataSource):
    subprocess.call("tests_integration/scripts/tearup_db.sh")
    empty_catalog_client.add(dc_entry=data_catalog_entry_postgres,
                             persist_data=True)
    new_data_catalog = DataCatalogClient()
    new_data_catalog.load_data()
    result = new_data_catalog.describe_obj("source_f")
    count_list = ([item for item in result["count"].to_list()])
    expected_list = [10, 10, 10]
    assert count_list == expected_list
    subprocess.call("tests_integration/scripts/teardown_db.sh")
