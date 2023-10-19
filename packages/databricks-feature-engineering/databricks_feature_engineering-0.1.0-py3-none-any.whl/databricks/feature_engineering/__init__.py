# Support sugar-syntax `from databricks.feature_store import FeatureStoreClient`, etc.
from databricks.feature_engineering.client import FeatureEngineeringClient
from databricks.feature_engineering.upgrade_client import UpgradeClient
from databricks.feature_engineering.version import VERSION
from databricks.feature_store.utils import request_context
from databricks.feature_store.utils.logging_utils import (
    _configure_feature_store_loggers,
)
from databricks.feature_store.utils.request_context import RequestContext


def inject_fe_client_version_to_fs_client_request_context():
    divider = "+fe-client_"
    if divider not in request_context.VERSION:
        request_context.VERSION = request_context.VERSION + divider + VERSION


def inject_upgrade_workspace_table_request_method():
    request_context.UPGRADE_WORKSPACE_TABLE = "upgrade_workpace_table"
    if (
        request_context.UPGRADE_WORKSPACE_TABLE
        not in RequestContext.valid_feature_store_method_names
    ):
        RequestContext.valid_feature_store_method_names.append(
            request_context.UPGRADE_WORKSPACE_TABLE
        )


_configure_feature_store_loggers(root_module_name=__name__)
inject_fe_client_version_to_fs_client_request_context()
inject_upgrade_workspace_table_request_method()

__all__ = ["FeatureEngineeringClient", "UpgradeClient"]
