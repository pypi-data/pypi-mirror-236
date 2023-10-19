from typing import Any, Dict, List

from databricks.feature_store.entities.data_type import DataType


# strings containing \ or ' can break sql statements, so escape them.
def escape_sql_string(input_str: str) -> str:
    return input_str.replace("\\", "\\\\").replace("'", "\\'")


def target_table_source_table_mismatch_msg(
    property: str, source_workspace_table_value: Any, target_uc_table_value: Any
):
    msg = (
        f"{property} from source workspace table does not match with target uc table. "
        f"Source workspace table is '{source_workspace_table_value}' while target uc table "
        f"is '{target_uc_table_value}'."
    )
    return msg


def raise_target_table_not_match_source_table_error(
    property: str, source_workspace_table_value: Any, target_uc_table_value: Any
):
    msg = (
        f"{target_table_source_table_mismatch_msg(property, source_workspace_table_value, target_uc_table_value)} "
        f"If you want to overwrite the existing value on target uc table, "
        f"call this method with overwrite = True."
    )
    raise RuntimeError(msg)


def raise_source_table_not_match_target_table_schema_error(
    source_table_features, target_table_schema
):
    catalog_schema = {
        feature.name: feature.data_type for feature in source_table_features
    }
    delta_schema = {
        feature.name: DataType.spark_type_to_string(feature.dataType)
        for feature in target_table_schema
    }
    msg = (
        f"The source table and target table schemas are not identical. "
        f"Source workspace table schema is '{catalog_schema}' while target uc table's schema "
        f"is '{delta_schema}'. Please reconcile the differences and call this method again."
    )
    raise RuntimeError(msg)


# Return true if source and target are equal or when source[key] != target[key], target[key] is empty
def compare_column_desc_map(source: Dict[str, str], target: Dict[str, str]) -> bool:
    # Keys must be the same
    if set(source.keys()) != set(target.keys()):
        return False
    for key in source:
        if key in target:
            if source[key] != target[key] and target[key]:
                return False
        else:
            return False

    return True


def format_tags(data_list: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    result_dict = {}
    for item in data_list:
        column_name = item["column_name"]
        tag_name = item["tag_name"]
        tag_value = item["tag_value"]

        if column_name not in result_dict:
            result_dict[column_name] = {}

        result_dict[column_name][tag_name] = tag_value
    return result_dict
