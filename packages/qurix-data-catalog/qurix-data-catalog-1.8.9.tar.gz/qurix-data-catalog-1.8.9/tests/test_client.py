from csv import DictReader

import pandas as pd
import pytest

from qurix.data.catalog.client import DataCatalogClient
from qurix.data.catalog.entities import CatalogDataSource
from qurix.data.catalog.exceptions import UnsupportedDataLoaderException
from tests.utils import TEST_RESOURCES_PATH


@pytest.fixture
def empty_catalog_client() -> DataCatalogClient:
    return DataCatalogClient()


@pytest.fixture
def client_csv() -> DataCatalogClient:
    return DataCatalogClient(sources_list_path=TEST_RESOURCES_PATH / "sources.csv")


@pytest.fixture
def data_catalog_entry() -> CatalogDataSource:
    return CatalogDataSource(name="source a",
                             location=str(TEST_RESOURCES_PATH /
                                          "source_a.csv"))


@pytest.fixture
def data_catalog_entry_parquet() -> CatalogDataSource:
    return CatalogDataSource(name="source d",
                             location=str(TEST_RESOURCES_PATH /
                                          "source_d.parquet"))


@pytest.fixture
def data_catalog_entry_xlsx() -> CatalogDataSource:
    return CatalogDataSource(name="source e",
                             location=str(TEST_RESOURCES_PATH /
                                          "source_e.xlsx"),
                             business_partner="some partner")


@pytest.fixture
def data_catalog_entry_postgres() -> CatalogDataSource:
    return CatalogDataSource(name="source f",
                             location="postgresql://postgres:postgres@localhost:5432/hichemchakroun",
                             business_partner="some partner",
                             table_schema="public",
                             table="contacts")


@pytest.fixture
def data_catalog_entry_sqlite() -> CatalogDataSource:
    return CatalogDataSource(name="source g",
                             location="tests/resources/source_g.db",
                             business_partner="some partner",
                             table="users")


def test_parse(client_csv: DataCatalogClient):
    result: dict[str, CatalogDataSource] = client_csv.parse_from_file()
    result = {k: {"name": v.name, "location": v.location}
              for k, v in result.items()}
    expected = {
        "source_a": {"name": "source a",
                     "location": str(TEST_RESOURCES_PATH / "source_a.csv")},
        "source_b": {"name": "source b",
                     "location": str(TEST_RESOURCES_PATH / "source_b.csv")},
    }
    assert result == expected


def test_fail_data_loader():
    not_supported_data_loc = "some_data_location.xml"
    with pytest.raises(UnsupportedDataLoaderException,
                       match=f"{not_supported_data_loc} is not supported"):
        data_source = CatalogDataSource(name="example",
                                        location=not_supported_data_loc)
        assert data_source is None


def test_property_catalog_dataframes(client_csv: DataCatalogClient):
    result = client_csv.catalog
    assert len(result) == 2


def test_export(client_csv: DataCatalogClient):
    client_csv.export()
    with open(client_csv.METADATA_DIR / client_csv.EXPORT_CATALOG_FILE_NAME) as f:
        reader = DictReader(f)
        export = list(reader)
    assert len(export) == 2


def test_get_csv(client_csv: DataCatalogClient):
    client_csv.parse_from_file()
    result_a = client_csv.get("source a", sep=";")[0]
    assert len(result_a) == 5

    result_b, row_count_b = client_csv.get("source b")
    assert len(result_b) == 10000


def test_empty_catalog(empty_catalog_client: DataCatalogClient):
    catalog = empty_catalog_client.catalog
    assert catalog == {}


def test_add(empty_catalog_client: DataCatalogClient, data_catalog_entry: CatalogDataSource):

    # Test kwargs load logic
    empty_catalog_client.add(dc_entry=data_catalog_entry,
                             # read_csv extra kwargs
                             sep=";",
                             index_col=None)
    catalog = empty_catalog_client.catalog
    assert len(catalog) == 1

    # Test metadata generation
    metaframe_num = empty_catalog_client.metaframes[
        f"{data_catalog_entry.name.replace(' ', '_')}:{empty_catalog_client.DESCRIBE_NUM_SUFFIX}"]
    metaframe_obj = empty_catalog_client.metaframes[
        f"{data_catalog_entry.name.replace(' ', '_')}:{empty_catalog_client.DESCRIBE_OBJ_SUFFIX}"]

    assert len(metaframe_num) == 1
    assert len(metaframe_obj) == 7

    # Test metadata
    assert metaframe_obj.loc["Username"]["count"] == 5
    assert metaframe_obj.loc["Username"]["top"] == "booker12"


def test_add_and_persist(empty_catalog_client: DataCatalogClient, data_catalog_entry: CatalogDataSource):

    empty_catalog_client.add(dc_entry=data_catalog_entry,
                             persist_data=True,
                             cache_data=True,
                             # read_csv extra kwargs
                             sep=";",
                             index_col=None)

    # read persisted meta data
    persisted_data = data_catalog_entry.name.replace(' ', '_') + "." +\
        f"{empty_catalog_client.DESCRIBE_OBJ_SUFFIX}"

    persisted_data_parquet = persisted_data + ".parquet"
    persisted_data_csv = persisted_data + ".csv"

    # Parquet files should maintain pandas properties
    result_parquet = pd.read_parquet(
        empty_catalog_client.METADATA_DIR / persisted_data_parquet)

    assert len(result_parquet) == 7
    assert result_parquet.loc["Last name"]["top"] == "Booker"
    assert result_parquet.loc["Location"]["count"] == '5'

    result_csv = pd.read_csv(
        empty_catalog_client.METADATA_DIR / persisted_data_csv,
        index_col=0
    )
    # Test that serialization to text works
    assert len(result_csv) == 7
    assert result_csv.loc["Last name"]["top"] == "Booker"
    assert result_csv.loc["Location"]["count"] == 5


def test_describe(empty_catalog_client: DataCatalogClient, data_catalog_entry: CatalogDataSource):
    empty_catalog_client.add(dc_entry=data_catalog_entry,
                             persist_data=True,
                             # read_csv extra kwargs
                             sep=";",
                             index_col=None)

    result = empty_catalog_client.describe("source a")

    assert len(result) == 8
    assert all([item == 5 for item in result["count"].to_list()])


def test_load_csv(empty_catalog_client: DataCatalogClient, data_catalog_entry: CatalogDataSource):
    # Persists a session
    empty_catalog_client.add(dc_entry=data_catalog_entry,
                             persist_data=True,
                             cache_data=True,
                             # read_csv extra kwargs
                             sep=";",
                             index_col=None)

    # Create a new data catalog
    new_data_catalog = DataCatalogClient()
    new_data_catalog.load_data()
    result = new_data_catalog.describe_obj("source_a")
    assert len(result) == 7
    assert result.loc["Username"]["top"] == "booker12"


def test_load_parquet(empty_catalog_client: DataCatalogClient, data_catalog_entry_parquet: CatalogDataSource):
    # Persists a session
    empty_catalog_client.add(dc_entry=data_catalog_entry_parquet,
                             persist_data=True,
                             cache_data=True
                             )
    # Create a new data catalog
    new_data_catalog = DataCatalogClient()
    new_data_catalog.load_data()
    result = new_data_catalog.describe_obj("source_d")
    assert all([item == 308854 for item in result["count"].to_list()])


def test_load_excel(empty_catalog_client: DataCatalogClient, data_catalog_entry_xlsx: CatalogDataSource):
    empty_catalog_client.add(dc_entry=data_catalog_entry_xlsx,
                             persist_data=True,
                             cache_data=True,
                             # read_csv extra kwargs
                             index_col=None)
    # Create a new data catalog
    new_data_catalog = DataCatalogClient()
    new_data_catalog.load_data()
    result = new_data_catalog.describe_obj("source_e")
    count_list = ([item for item in result["count"].to_list()])
    expected_couts_list = [105, 105, 103, 105, 105, 105, 105, 103]
    assert count_list == expected_couts_list


def test_load_sqlite(empty_catalog_client: DataCatalogClient, data_catalog_entry_sqlite: CatalogDataSource):
    empty_catalog_client.add(dc_entry=data_catalog_entry_sqlite,
                             persist_data=True,
                             cache_data=True)
    new_data_catalog = DataCatalogClient()
    new_data_catalog.load_data()
    result = new_data_catalog.describe_obj("source_g")
    print(result)
    count_list = ([item for item in result["count"].to_list()])
    expected_list = [5]
    assert count_list == expected_list
    expected_list = [5]
    assert count_list == expected_list
