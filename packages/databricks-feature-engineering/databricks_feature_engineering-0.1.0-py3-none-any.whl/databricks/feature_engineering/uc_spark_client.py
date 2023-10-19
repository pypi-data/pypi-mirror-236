import logging
from typing import Dict, List, Optional

from databricks.feature_engineering.utils import upgrade_utils
from databricks.feature_store.spark_client import SparkClient
from databricks.feature_store.utils.utils import (
    sanitize_identifier,
    sanitize_multi_level_name,
)

_logger = logging.getLogger(__name__)


class UcSparkClient:
    def __init__(self, spark_client: SparkClient):
        self._spark_client = spark_client

    @staticmethod
    def drop_pk_statement(full_table_name: str):
        return f"ALTER TABLE {sanitize_multi_level_name(full_table_name)} DROP PRIMARY KEY CASCADE"

    def drop_pk(self, full_table_name: str):
        self._spark_client._spark.sql(UcSparkClient.drop_pk_statement(full_table_name))

    @staticmethod
    def _default_pk_name(table_name):
        return table_name + "_pk"

    @staticmethod
    def set_pk_tk_statement(
        full_table_name: str,
        pk_cols: List[str],
        tk_col: Optional[str],
        pk_name: Optional[str] = None,
    ):
        _, _, table_name = full_table_name.split(".")
        if not pk_name:
            pk_name = UcSparkClient._default_pk_name(table_name)
        constraintStmt = ", ".join(
            sanitize_identifier(col) + " TIMESERIES"
            if tk_col and col == tk_col
            else sanitize_identifier(col)
            for col in pk_cols
        )
        return f"ALTER TABLE {sanitize_multi_level_name(full_table_name)} ADD CONSTRAINT {sanitize_identifier(pk_name)} PRIMARY KEY({constraintStmt})"

    def set_pk_tk(
        self,
        full_table_name: str,
        pk_cols: List[str],
        tk_col: Optional[str],
        pk_name: Optional[str] = None,
    ):
        if not pk_cols:
            return
        if tk_col and tk_col not in pk_cols:
            raise RuntimeError(
                f"Timeseries column {tk_col} is not included as part of primary keys {pk_cols}."
            )
        _logger.info(
            f"Setting columns {pk_cols} of table '{full_table_name}' to NOT NULL."
        )
        # Set all delta primary keys to NOT NULL
        self._spark_client.set_cols_not_null(
            full_table_name=full_table_name, cols=pk_cols
        )
        _logger.info(
            f"Setting Primary Keys constraint {pk_cols} on table '{full_table_name}'."
        )
        self._spark_client._spark.sql(
            UcSparkClient.set_pk_tk_statement(full_table_name, pk_cols, tk_col, pk_name)
        )

    def set_column_comment(self, delta_table_name, column_name, comment):
        """
        Set a column's comment. If comment is None, the column's comment will be removed.
        """
        if comment is None:
            self._spark_client._spark.sql(
                f"ALTER TABLE {sanitize_multi_level_name(delta_table_name)} ALTER COLUMN {sanitize_identifier(column_name)} COMMENT NULL"
            )
        else:
            escaped_comment = upgrade_utils.escape_sql_string(comment)
            self._spark_client._spark.sql(
                f"ALTER TABLE {sanitize_multi_level_name(delta_table_name)} ALTER COLUMN {sanitize_identifier(column_name)} COMMENT '{escaped_comment}'"
            )

    def set_column_tags(
        self, full_table_name: str, column_name: str, tags: Dict[str, str]
    ):
        """
        Set a column's tags. Noop if tags is empty.
        """
        if not tags:
            return
        formatted_pairs = []
        for key, value in tags.items():
            escaped_key = upgrade_utils.escape_sql_string(key)
            escaped_value = upgrade_utils.escape_sql_string(value)
            formatted_pairs.append(f"'{escaped_key}' = '{escaped_value}'")
        result = "(" + ", ".join(formatted_pairs) + ")"

        sql_string = f"""ALTER TABLE {sanitize_multi_level_name(full_table_name.lower())} ALTER COLUMN {sanitize_identifier(column_name)} SET TAGS {result}"""
        self._spark_client._spark.sql(sql_string)

    def set_table_tags(self, full_table_name: str, tags: Dict[str, str]):
        """
        Set a table's tags. Noop if tags is empty.
        """
        if not tags:
            return
        formatted_pairs = []
        for key, value in tags.items():
            escaped_key = upgrade_utils.escape_sql_string(key)
            escaped_value = upgrade_utils.escape_sql_string(value)
            formatted_pairs.append(f"'{escaped_key}' = '{escaped_value}'")
        result = "(" + ", ".join(formatted_pairs) + ")"
        sql_string = f"""ALTER TABLE {sanitize_multi_level_name(full_table_name.lower())} SET TAGS {result}"""
        self._spark_client._spark.sql(sql_string)

    def unset_table_tags(self, full_table_name: str, tags: List[str]):
        """
        Remove tags from table. Noop if tags is empty.
        """
        if not tags:
            return
        tags_expression = ",".join(
            f"'{upgrade_utils.escape_sql_string(tag)}'" for tag in tags
        )
        sql_string = f"""ALTER TABLE {sanitize_multi_level_name(full_table_name.lower())} UNSET TAGS ({tags_expression})"""
        self._spark_client._spark.sql(sql_string)

    def unset_column_tags(
        self, full_table_name: str, column_name: str, tags: List[str]
    ):
        """
        Remove tags from column. Noop if tags is empty.
        """
        if not tags:
            return
        tags_expression = ",".join(
            f"'{upgrade_utils.escape_sql_string(tag)}'" for tag in tags
        )
        sql_string = f"""ALTER TABLE {sanitize_multi_level_name(full_table_name.lower())} ALTER COLUMN {sanitize_identifier(column_name)} UNSET TAGS ({tags_expression})"""
        self._spark_client._spark.sql(sql_string)

    def get_all_column_tags(self, full_table_name: str) -> List[Dict[str, str]]:
        """
        Get all tags for all columns from a given table
        """
        catalog_name, schema_name, table_name = full_table_name.split(".")

        sql_string = (
            f"SELECT column_name, tag_name, tag_value FROM {sanitize_identifier(catalog_name)}.information_schema.column_tags "
            f"WHERE catalog_name = '{catalog_name}' AND schema_name = '{schema_name}' "
            f"AND table_name = '{table_name}';"
        )
        df = self._spark_client._spark.sql(sql_string)
        r_dict = [row.asDict() for row in df.collect()]
        return r_dict
