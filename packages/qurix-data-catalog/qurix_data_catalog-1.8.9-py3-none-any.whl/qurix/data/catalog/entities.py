from pathlib import Path

from pydantic import BaseModel, ConfigDict

from qurix.data.catalog.dataloader import DataLoader
from qurix.data.catalog.utils import get_data_loader


class CatalogDataSource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    location: str | Path
    table_schema: str | None = None
    table: str | None = None
    data_loader: DataLoader | None = None
    has_obj_columns: bool = True
    has_num_columns: bool = True
    row_count: int = 0

    def model_post_init(self, kwargs) -> None:
        values = self.model_dump()
        self.data_loader = get_data_loader(
            dc_location=values["location"],
            dc_schema=values["table_schema"],
            dc_table=values["table"],
        )
