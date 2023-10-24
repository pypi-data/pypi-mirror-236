from enum import Enum

from qurix.data.catalog.dataloader import (CsvDataLoader, DB2DataLoader,
                                           ParquetDataLoader,
                                           PostgresDataLoader,
                                           SQLiteDataLoader, XlsxDataLoader)
from qurix.data.catalog.exceptions import UnsupportedDataLoaderException

SupportedDataLoader = (
    SQLiteDataLoader | PostgresDataLoader | CsvDataLoader | XlsxDataLoader | ParquetDataLoader | DB2DataLoader
)


class ConnectorPattern(str, Enum):
    POSTGRESSQL = "postgresql://"
    DB2 = "ibm_db_sa://"
    SQLITE = ".db"
    CSV = ".csv"
    XLSX = ".xlsx"
    PARQUET = ".parquet"


def get_data_loader(dc_location: str, dc_schema: str, dc_table: str) -> SupportedDataLoader | None:
    """Infers a data loader class based on the data location string.
        Similar to a connector factory.

    Args:
        data_loc (str): string representation of a connection string or
        file path.

    Raises:
        UnsupportedDataLoader: when a data loader could not be found for
        the data_loc

    Returns:
        SupportedDataLoader: a union type of all the current supported
        loader classes
    """
    match dc_location:
        case _ if (ConnectorPattern.POSTGRESSQL in dc_location):
            return PostgresDataLoader(catalog_source_location=dc_location,
                                      source_table=dc_table,
                                      source_schema=dc_schema
                                      )

        case _ if (ConnectorPattern.DB2 in dc_location):
            return DB2DataLoader(catalog_source_location=dc_location,
                                 source_table=dc_table,
                                 source_schema=dc_schema)

        case _ if dc_location.endswith(ConnectorPattern.SQLITE):
            return SQLiteDataLoader(catalog_source_location=dc_location,
                                    source_table=dc_table)

        case _ if dc_location.endswith(ConnectorPattern.CSV):
            return CsvDataLoader(catalog_source_location=dc_location)

        case _ if dc_location.endswith(ConnectorPattern.XLSX):
            return XlsxDataLoader(catalog_source_location=dc_location)

        case _ if dc_location.endswith(ConnectorPattern.PARQUET):
            return ParquetDataLoader(catalog_source_location=dc_location)
        case _:
            raise UnsupportedDataLoaderException(
                f"{dc_location} is" " not supported")
    return None
