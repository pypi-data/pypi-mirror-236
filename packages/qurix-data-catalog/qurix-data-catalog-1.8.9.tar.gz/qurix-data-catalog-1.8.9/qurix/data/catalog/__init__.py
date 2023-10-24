from qurix.data.catalog.__version__ import VERSION
from qurix.data.catalog.client import DataCatalogClient
from qurix.data.catalog.entities import CatalogDataSource


__version__ = VERSION

__all__ = ["DataCatalogClient", "CatalogDataSource"]
