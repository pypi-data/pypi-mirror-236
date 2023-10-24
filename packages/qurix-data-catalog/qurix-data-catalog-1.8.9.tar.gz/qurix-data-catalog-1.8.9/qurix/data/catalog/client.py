import logging
import os
import re
from csv import DictReader
from pathlib import Path

import numpy as np
import pandas as pd

from qurix.data.catalog.entities import CatalogDataSource
from qurix.data.catalog.exceptions import NoLocalSourcesFile

logger = logging.getLogger(__name__)


class DataCatalogClient:
    """Client to manipulate data sources and add/remove them to a datacatalog

    It uses a caching mechanism to export metadata to a local directory and reuse
    this files for further sessions
    """

    ROOT_DIR = Path(".catalog_cache")
    CACHE_DIR = ROOT_DIR / "cache"
    METADATA_DIR = ROOT_DIR / "metadata"
    EXPORT_CATALOG_FILE_NAME = "catalog.csv"
    EXPORT_CATALOG_FILE_NAME_XLSX = "catalog.xlsx"
    DESCRIBE_NUM_SUFFIX = "describe_num"
    DESCRIBE_OBJ_SUFFIX = "describe_obj"
    DESCRIBE_STRUCT_SUFFIX = "describe_struct"
    DESCRIBE_TOP10_SUFFIX = "describe_top10"
    EXPORT_METAFRAMES_SUMMARY_XLSX = "metaframes_summary.xlsx"

    def __init__(self, sources_list_path: str | None = None):
        self._sources_list_path = sources_list_path
        self._catalog: dict[str, CatalogDataSource] = {}
        self._metaframes: dict[str, pd.DataFrame] = {}
        self._dataframes: dict[str, pd.DataFrame] = {}

    def parse_from_file(self) -> dict[str, CatalogDataSource]:
        sources: dict[str, CatalogDataSource] = {}
        if self._sources_list_path:
            with open(self._sources_list_path, "r") as f:
                reader = DictReader(f)
                catalog = list(reader)
                sources = {
                    self._clean_name(item["name"]): CatalogDataSource.model_validate(item)
                    for item in catalog
                }
                return sources
        else:
            raise NoLocalSourcesFile(
                "No local sources file to read data sources from")

    @property
    def catalog(self) -> dict[str, CatalogDataSource]:
        if len(self._catalog) == 0 and self._sources_list_path:
            self._catalog = self.parse_from_file()
        return self._catalog

    @property
    def metaframes(self) -> dict[str, pd.DataFrame]:
        return self._metaframes

    def export(self, format: str = ".csv") -> None:
        if len(self._catalog) == 0 and self._sources_list_path:
            self._catalog = self.parse_from_file()

        export_content = [item.model_dump()
                          for _, item in self._catalog.items()]
        df = pd.DataFrame.from_records(export_content)
        self.METADATA_DIR.mkdir(exist_ok=True, parents=True)

        match format:
            case ".csv":
                df.to_csv(self.METADATA_DIR /
                          self.EXPORT_CATALOG_FILE_NAME, index=False)
            case ".xlsx":
                df.to_excel(self.METADATA_DIR /
                            self.EXPORT_CATALOG_FILE_NAME_XLSX, index=False)
            case _:
                raise ValueError(f"Export format {format} is not supported")

    def check_numeric_columns(self, df: pd.DataFrame) -> bool:
        numeric_columns = df.select_dtypes(include=['number']).columns
        has_num_columns = not numeric_columns.empty
        return has_num_columns

    def check_obj_columns(self, df: pd.DataFrame) -> bool:
        has_object_columns = any(df.dtypes == 'object')
        return has_object_columns

    def add(self, dc_entry: CatalogDataSource, persist_data: bool = False, cache_data: bool = False, **kwargs) -> None:
        """Adds a data source to the data catalog and eventually
        to an in memory dictionary of dataframes. It also
        offers the possibility to persist the data locally.

        Args:
            dc_entry (CatalogDataSource): a single data catalog entry
            persist_data (bool): whether the data source should be stored in
            memory
            **kwargs: more pandas specific options to load data

        Raises:
            ValueError: if the entry already exists
        """
        if dc_entry.name not in self._catalog.keys():
            # Update data catalog
            self._catalog[self._clean_name(dc_entry.name)] = dc_entry

            # Fetch data and row count
            df, row_count = self.get(dc_entry.name, **kwargs)

            dc_entry.has_num_columns = self.check_numeric_columns(df)
            dc_entry.has_obj_columns = self.check_obj_columns(df)
            dc_entry.row_count = row_count
            # dc_entry.row_count = self.get_row_count(dc_entry.name, **kwargs)
            # dc_entry.row_count = dc_entry.data_loader.get_row_count(**kwargs)
            # if str(dc_entry.data_loader) == "<PostgresDataLoader>":
            #     dc_entry.location = self.mask_credentials_postgres(dc_entry.location)
            # Update metaframes and evetually persist
            self._update_metadata(
                df, dc_entry, persist_data=persist_data, cache_data=cache_data)

            # Update datacatalog
            self.export()
        else:
            raise ValueError(f"Entry name {dc_entry.name}" " already exists")

    def update(self, dc_entry: CatalogDataSource) -> None:
        """Updates a certain data source to the data catalog"""
        self.delete(dc_entry)
        self.add(dc_entry)

    def delete(self, dc_entry: CatalogDataSource):
        """Deletes a certain data source to the data catalog"""
        if dc_entry.name not in self._catalog:
            logging.warning(
                f"Data source {dc_entry.name} does not exist in catalog. Skipping delete."
            )
        else:
            self._catalog.pop(self._clean_name(dc_entry.name))

    def get(self, source_name: str, **kwargs) -> (pd.DataFrame, int):
        """Loads a single data source from the data catalog in memory"""
        try:
            catalog_data_source: CatalogDataSource = self.catalog[self._clean_name(
                source_name)]

            if catalog_data_source.data_loader is not None:
                get_output = catalog_data_source.data_loader.load(**kwargs)
                row_count = catalog_data_source.data_loader.get_row_count(
                    **kwargs)
                return get_output, row_count
            else:
                raise ValueError(
                    f"Data Loader is not set for {catalog_data_source.name}")
        except Exception as e:
            raise KeyError(
                f"Source name {source_name} could not be found in data catalog. See {e}")

    def describe_num(self, source_name: str) -> pd.DataFrame:
        internal_name = self._clean_name(
            f"{source_name}:{self.DESCRIBE_NUM_SUFFIX}")
        return self._data_frame_lookup(self.metaframes, internal_name)

    def describe_obj(self, source_name: str) -> pd.DataFrame:
        internal_name = self._clean_name(
            f"{source_name}:{self.DESCRIBE_OBJ_SUFFIX}")
        return self._data_frame_lookup(self.metaframes, internal_name)

    def describe_struct(self, source_name: str) -> pd.DataFrame:
        internal_name = self._clean_name(
            f"{source_name}:{self.DESCRIBE_STRUCT_SUFFIX}")
        return self._data_frame_lookup(self.metaframes, internal_name)

    def describe_top10(self, source_name: str) -> pd.DataFrame:
        internal_name = self._clean_name(
            f"{source_name}:{self.DESCRIBE_TOP10_SUFFIX}")
        return self._data_frame_lookup(self.metaframes, internal_name)

    def describe(self, source_name: str, verbose: bool = True, **kwargs) -> pd.DataFrame:
        df = self._dataframes.get(self._clean_name(source_name))
        if df is None:
            df = self.get(source_name=source_name, **kwargs)
        column_names = df.columns.to_list()
        column_counts = df.count().to_list()
        column_dtypes = df.dtypes.to_list()

        INDEX = "column_name"
        description = {INDEX: column_names,
                       "count": column_counts, "data_type": column_dtypes}
        description_df = pd.DataFrame(description)
        description_df.set_index(INDEX, inplace=True)
        if verbose:
            import pprint

            pprint.pprint(description_df)
        return description_df

    def load_data(self) -> None:
        catalog_path = self.METADATA_DIR / self.EXPORT_CATALOG_FILE_NAME
        try:
            sources_df = pd.read_csv(catalog_path, index_col=False)

            for _, row in sources_df.iterrows():
                self._load_cache_dataframe(row["name"])
                self._load_metaframes(row["name"])
        except Exception as e:
            raise FileNotFoundError(
                f"Data catalog or cached meta/dataframes could not be found. See {e}"
            )

    def load_catalog(self) -> pd.DataFrame:
        """Loads the cached catalog csv as a pandas dataframe in memory"""
        catalog_path = self.METADATA_DIR / self.EXPORT_CATALOG_FILE_NAME
        try:
            catalog_df = pd.read_csv(catalog_path, index_col=False)
            return catalog_df
        except Exception as e:
            raise FileNotFoundError(
                f"Data catalog or cached meta/dataframes could not be found. See {e}"
            )

    def _is_nested_column(self, series: pd.Series):
        def is_nested(element):
            return isinstance(element, (list, dict, tuple)) and not isinstance(element, (int, float, str))

        if series.dtype == 'object':
            elements = series.dropna()
            if any(is_nested(element) for element in elements):
                return True
        return False

    @staticmethod
    def persist(self, local_dir: Path, df: pd.DataFrame, file_name: str, **kwargs) -> None:
        """Stores a datafrme in csv and parquet format

        Args:
            local_dir (Path): directory to store
            df (pd.DataFrame): data source
            file_name (str): name of the file to store

         Possible extra kwargs = {
            "coerce_timestamps": "us",
            "allow_truncated_timestamps": True,
            "engine" : "pyarrow"
            }
        """
        local_dir.mkdir(exist_ok=True, parents=True)
        df.to_csv(local_dir / f"{file_name}.csv", **kwargs)
        for column in df.columns:
            df[column] = df[column].astype("str")
        df.to_parquet(local_dir / f"{file_name}.parquet", **kwargs)

    def _load_cache_dataframe(self, source_name: str) -> None:
        internal_name = self._clean_name(source_name)
        cached_data_path = self.CACHE_DIR / f"{internal_name}.parquet"
        try:
            df = pd.read_parquet(cached_data_path)
            self._dataframes[internal_name] = df
        except Exception as e:
            raise FileNotFoundError(f"Dataframe could not be found. See {e}")

    def _load_metaframes(self, source_name: str) -> None:
        internal_name = self._clean_name(source_name)
        num_metaframe_path = self.METADATA_DIR / \
            f"{internal_name}.{self.DESCRIBE_NUM_SUFFIX}.csv"
        obj_metaframe_path = self.METADATA_DIR / \
            f"{internal_name}.{self.DESCRIBE_OBJ_SUFFIX}.csv"
        struct_metaframe_path = self.METADATA_DIR / \
            f"{internal_name}.{self.DESCRIBE_STRUCT_SUFFIX}.csv"
        top10_metaframe_path = self.METADATA_DIR / \
            f"{internal_name}.{self.DESCRIBE_TOP10_SUFFIX}.csv"

        # load local objects
        if os.path.isfile(num_metaframe_path):
            num_metaframe = pd.read_csv(num_metaframe_path, index_col=0)
            self.metaframes[f"{internal_name}:{self.DESCRIBE_NUM_SUFFIX}"] = num_metaframe
        if os.path.isfile(obj_metaframe_path):
            obj_metaframe = pd.read_csv(obj_metaframe_path, index_col=0)
            self.metaframes[f"{internal_name}:{self.DESCRIBE_OBJ_SUFFIX}"] = obj_metaframe
        struct_metaframe = pd.read_csv(struct_metaframe_path, index_col=0)
        top10_metaframe = pd.read_csv(top10_metaframe_path, index_col=0)

        self.metaframes[f"{internal_name}:{self.DESCRIBE_STRUCT_SUFFIX}"] = struct_metaframe
        self.metaframes[f"{internal_name}:{self.DESCRIBE_TOP10_SUFFIX}"] = top10_metaframe

    @staticmethod
    def _data_frame_lookup(data_frames: dict, key: str) -> pd.DataFrame:
        try:
            return data_frames[key]
        except Exception as e:
            raise KeyError(
                f"Data frame {key} can not be found in dataframes/metaframes. See {e}")

    def get_describe_struct_df(self, df: pd.DataFrame) -> pd.DataFrame:
        metaframe_struct = pd.DataFrame(df.dtypes, columns=["type"])
        metaframe_struct["type"] = metaframe_struct["type"].astype("str")
        return metaframe_struct

    def get_describe_top_n_df(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Describe top n records from a df

        Args:
            df (pd.DataFrame): Initial dataframe
            n (int, optional): How many records to consider. Defaults to 10.

        Returns:
            pd.DataFrame: Description dataframe with top n records
        """
        top_n_frequent_values = {}
        for column in df.columns:
            is_nested = self._is_nested_column(df[column])
            if not is_nested:
                value_counts = df[column].value_counts()
                top_n = value_counts.nlargest(n).index.tolist()
                top_n_frequent_values[column] = top_n

        describe_top_n_df = pd.DataFrame.from_dict(
            top_n_frequent_values, orient="index").reset_index()

        mapping = {**{"index": "column"},
                   **{x: f"top{x}" for x in range(n - 1)}}

        describe_top_n_df.rename(columns=mapping, inplace=True)
        describe_top_n_df = describe_top_n_df.astype(str)
        return describe_top_n_df

    def _update_metadata(
        self, df: pd.DataFrame, dc_entry: CatalogDataSource, persist_data: bool = False, cache_data: bool = False
    ) -> None:
        """Updates metaframes (dict[str, pd.Dataframes])

        Args:
            df (pd.DataFrame): original data source
            dc_entry (CatalogDataSource): data catalog representation
            persist_data (bool, optional): Whether data should be stored
            locally. Defaults to False.
        """
        internal_name = self._clean_name(dc_entry.name)

        if dc_entry.has_num_columns:
            metaframe_num = df.describe(include=[np.number]).transpose()
            self._metaframes[f"{internal_name}:{self.DESCRIBE_NUM_SUFFIX}"] = metaframe_num

        if dc_entry.has_obj_columns:
            metaframe_obj = df.describe(include=[object]).transpose()
            self._metaframes[f"{internal_name}:{self.DESCRIBE_OBJ_SUFFIX}"] = metaframe_obj

        metaframe_struct = self.get_describe_struct_df(df)
        self._metaframes[f"{internal_name}:{self.DESCRIBE_STRUCT_SUFFIX}"] = metaframe_struct

        metaframe_top10 = self.get_describe_top_n_df(df, n=10)
        self._metaframes[f"{internal_name}:{self.DESCRIBE_TOP10_SUFFIX}"] = metaframe_top10

        # Store dataframe
        self._dataframes[f"{internal_name}"] = df

        if persist_data:
            if dc_entry.has_num_columns:
                self.persist(
                    self, self.METADATA_DIR, metaframe_num, f"{internal_name}.{self.DESCRIBE_NUM_SUFFIX}"
                )
            if dc_entry.has_obj_columns:
                self.persist(
                    self, self.METADATA_DIR, metaframe_obj, f"{internal_name}.{self.DESCRIBE_OBJ_SUFFIX}"
                )
            self.persist(
                self, self.METADATA_DIR, metaframe_struct, f"{internal_name}.{self.DESCRIBE_STRUCT_SUFFIX}"
            )
            self.persist(
                self, self.METADATA_DIR, metaframe_top10, f"{internal_name}.{self.DESCRIBE_TOP10_SUFFIX}"
            )
        if cache_data:
            self.persist(self, self.CACHE_DIR, df, internal_name, index=False)

    def export_metaframes_summary_excel(
            self, target_path, file_prefix) -> None:
        sources_list = list(self._catalog.keys())
        # define columns
        columns_struct_df = ["source", "db_type",
                             "database", "schema", "table", "column", "type"]
        columns_desc_num_df = ["source", "db_type", "database", "schema", "table",
                               "column", "count", "mean", "std", "min", "25%", "50%", "75%", "max"]
        columns_desc_obj_df = ["source", "db_type", "database",
                               "schema", "table", "column", "count", "unique", "top", "freq"]
        columns_desc_top10_df = ["source", "db_type", "database", "schema", "table", "column",
                                 "top1", "top2", "top3", "top4", "top5", "top6", "top7", "top8", "top9", "top10"]
        # initialize summary dataframes
        struct_df_summary = pd.DataFrame(columns=columns_struct_df)
        desc_num_df_summary = pd.DataFrame(columns=columns_desc_num_df)
        desc_obj_df_summary = pd.DataFrame(columns=columns_desc_obj_df)
        desc_top10_df_summary = pd.DataFrame(columns=columns_desc_top10_df)

        for source in sources_list:
            database = self._catalog[source].location.split('/')[-1]
            schema = self._catalog[source].table_schema
            table = self._catalog[source].table
            has_num_columns = self._catalog[source].has_num_columns
            has_obj_columns = self._catalog[source].has_obj_columns
            strdataloader = str(self._catalog[source].data_loader)
            db_type = re.search(r"<(.+?)DataLoader>", strdataloader).group(1)
            print(schema, table, db_type, database)
            # struct df
            struct_df = self.describe_struct(source).reset_index()
            struct_df.rename(columns={"index": "column"}, inplace=True)
            struct_df.insert(loc=0, column="source", value=source)
            struct_df.insert(loc=1, column="db_type", value=db_type)
            struct_df.insert(loc=2, column="database", value=database)
            struct_df.insert(loc=3, column="schema", value=schema)
            struct_df.insert(loc=4, column="table", value=table)
            struct_df_summary = pd.concat(
                [struct_df_summary, struct_df], ignore_index=True)
            # desc num df
            if has_num_columns:
                desc_num_df = self.describe_num(source).reset_index()
                desc_num_df.rename(columns={"index": "column"}, inplace=True)
                desc_num_df["source"] = source
                desc_num_df["db_type"] = db_type
                desc_num_df["database"] = database
                desc_num_df["schema"] = schema
                desc_num_df["table"] = table
                desc_num_df = desc_num_df[columns_desc_num_df]
                desc_num_df_summary = pd.concat(
                    [desc_num_df_summary, desc_num_df], ignore_index=True)
            # desc obj df
            if has_obj_columns:
                desc_obj_df = self.describe_obj(source).reset_index()
                desc_obj_df.rename(columns={"index": "column"}, inplace=True)
                desc_obj_df["source"] = source
                desc_obj_df["db_type"] = db_type
                desc_obj_df["database"] = database
                desc_obj_df["schema"] = schema
                desc_obj_df["table"] = table
                desc_obj_df = desc_obj_df[columns_desc_obj_df]
                desc_obj_df_summary = pd.concat(
                    [desc_obj_df_summary, desc_obj_df], ignore_index=True)
            # desc top10 df
            desc_top10_df = self.describe_top10(source).reset_index()
            desc_top10_df.insert(loc=0, column="source", value=source)
            desc_top10_df.insert(loc=1, column="db_type", value=db_type)
            desc_top10_df.insert(loc=2, column="database", value=database)
            desc_top10_df.insert(loc=3, column="schema", value=schema)
            desc_top10_df.insert(loc=4, column="table", value=table)
            desc_top10_df_summary = pd.concat(
                [desc_top10_df_summary, desc_top10_df], ignore_index=True)
            desc_top10_df_summary.drop(["index"], axis=1, inplace=True)

        target_full_path = f"{target_path}/{file_prefix}_{self.EXPORT_METAFRAMES_SUMMARY_XLSX}"

        with pd.ExcelWriter(target_full_path, engine='xlsxwriter') as writer:
            # Write each DataFrame to a different worksheet
            catalog_df = self.load_catalog()
            catalog_df.to_excel(writer, sheet_name='catalog', index=False)
            struct_df_summary.to_excel(
                writer, sheet_name='describe_struct_summary', index=False)
            desc_num_df_summary.to_excel(
                writer, sheet_name='describe_num_summary', index=False)
            desc_obj_df_summary.to_excel(
                writer, sheet_name='describe_obj_summary', index=False)
            desc_top10_df_summary.to_excel(
                writer, sheet_name='describe_top10_summary', index=False)
            print(f"DataFrames exported to {target_full_path}")

    @staticmethod
    def _clean_name(file_name: str) -> str:
        return file_name.replace(" ", "_")
