import logging
from typing import Dict, Optional

from databricks.feature_engineering.uc_client import UcClient
from databricks.feature_engineering.uc_spark_client import UcSparkClient
from databricks.feature_engineering.utils import upgrade_utils
from databricks.feature_store.api.proto.feature_catalog_pb2 import ProducerAction
from databricks.feature_store.client import FeatureStoreClient
from databricks.feature_store.entities.feature_table import FeatureTable
from databricks.feature_store.utils import request_context, schema_utils, uc_utils
from databricks.feature_store.utils.request_context import RequestContext

_logger = logging.getLogger(__name__)


class UpgradeClient:
    """
    Client for upgrading workspace feature table metadata to Unity Catalog.
    """

    def __init__(
        self,
        *,
        feature_store_uri: Optional[str] = None,
        model_registry_uri: Optional[str] = None,
    ):
        """
        Creates a client to to upgrade workspace feature table metadata to Unity Catalog. Takes in an optional parameter to identify the remote
        workspace for multi-workspace Feature Store.

        :param feature_store_uri: An URI of the form ``databricks://<scope>.<prefix>`` that identifies the credentials
          of the intended Feature Store workspace. Throws an error if specified but credentials were not found.
        :param model_registry_uri: Address of local or remote model registry server. If not provided,
          defaults to the local server.
        """
        self._fs_client = FeatureStoreClient(
            feature_store_uri=feature_store_uri, model_registry_uri=model_registry_uri
        )
        self._spark_client = self._fs_client._spark_client
        self._spark_client_helper = self._fs_client._spark_client_helper
        self._catalog_client = self._fs_client._catalog_client
        self._uc_spark_client = UcSparkClient(self._spark_client)
        self._uc_client = UcClient(self._catalog_client)

    def upgrade_workspace_table(
        self,
        *,
        source_workspace_table: str,
        target_uc_table: str,
        overwrite: bool = False,
    ) -> None:
        """
        Upgrade a workspace feature table metadata to Unity Catalog.

        This api will upgrade the following metadata to Unity Catalog: primary keys, timeseries columns, table description,
        column descriptions, table tags, column tags, notebook lineage, job lineage.

        .. note::
            You must first upgrade the underlying workspace delta table to Unity Catalog before calling this api.
            Attempting to call this api before upgrading the underlying delta table will result in an error.
            Upgrade the workspace delta table by following: `Upgrade tables and views to Unity Catalog
            <https://docs.databricks.com/en/data-governance/unity-catalog/migrate.html#upgrade-tables-and-views-to-unity-catalog>`_
        :param source_workspace_table: Name of the source workspace feature table.
        :param target_uc_table: Name of the Unity Catalog table that source workspace table has been upgraded to.
        :param overwrite: Set this to true if you want to overwrite existing target table metadata.
        """
        source_table_name = uc_utils.get_full_table_name(
            source_workspace_table,
            self._spark_client.get_current_catalog(),
            self._spark_client.get_current_database(),
        )
        target_table_name = uc_utils.get_full_table_name(
            target_uc_table,
            self._spark_client.get_current_catalog(),
            self._spark_client.get_current_database(),
        )
        # Validations
        if not uc_utils.is_default_hms_table(source_table_name):
            raise ValueError(
                "source_workspace_table name must be a valid workspace table name"
            )
        if not uc_utils.is_uc_entity(target_table_name):
            raise ValueError("target_uc_table name must be a valid UC table name")
        # Tables exist
        source_ft = self._fs_client.get_table(name=source_table_name)
        self._spark_client_helper.check_feature_table_exists(target_table_name)
        # Schemas are the same
        source_features = self._uc_client.get_features(
            source_table_name,
            req_context=RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
        )
        target_df = self._spark_client.read_table(target_table_name)
        if not schema_utils.catalog_matches_delta_schema(
            source_features, target_df.schema
        ):
            upgrade_utils.raise_source_table_not_match_target_table_schema_error(
                source_features, target_df.schema
            )

        self._upgrade_pk_tk(source_ft, target_table_name, overwrite)

        # # Collect existing metadata
        target_ft = self._fs_client.get_table(name=target_table_name)
        target_features = self._uc_client.get_features(
            target_table_name,
            req_context=RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
        )
        ft_col_desc_map: Dict[str, str] = {
            c.name: c.description for c in source_features
        }
        target_ft_col_desc_map: Dict[str, str] = {
            c.name: c.description for c in target_features
        }
        feature_tags_target = upgrade_utils.format_tags(
            self._uc_spark_client.get_all_column_tags(target_table_name)
        )
        feature_tags_source: Dict[
            str, Dict[str, str]
        ] = {}  # { feature_name: {tag_key: tag_value} }
        for feature in source_features:
            feature_tags_source[feature.name] = {
                tag.key: tag.value
                for tag in self._uc_client.get_feature_tags(
                    feature.feature_id,
                    RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
                )
            }
            if not feature.name in feature_tags_target:
                feature_tags_target[feature.name] = {}

        self._validate_metadata(
            source_ft,
            ft_col_desc_map,
            feature_tags_source,
            target_ft,
            target_ft_col_desc_map,
            feature_tags_target,
            overwrite,
        )

        self._upgrade_descriptions(
            source_ft=source_ft,
            target_ft=target_ft,
            target_table_name=target_table_name,
            ft_col_desc_map=ft_col_desc_map,
            target_ft_col_desc_map=target_ft_col_desc_map,
        )
        self._upgrade_tags(
            source_ft,
            target_ft,
            target_table_name,
            feature_tags_source,
            feature_tags_target,
            overwrite,
        )
        self._upgrade_lineage(source_ft, target_table_name, source_table_name)
        self._uc_client.upgrade_to_uc(source_table_name, target_table_name)
        _logger.info("Successfully completed upgrade")

    def _upgrade_lineage(
        self, source_ft: FeatureTable, target_table_name: str, source_table_name: str
    ):
        # Table - producer
        _logger.info("Upgrading producers...")
        notebooks = source_ft.notebook_producers
        jobs = source_ft.job_producers
        for notebook in notebooks:
            self._catalog_client.add_notebook_producer(
                target_table_name,
                notebook.notebook_id,
                notebook.revision_id,
                ProducerAction.WRITE,  # This field is ignored by FS service
                RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
            )
        for job in jobs:
            self._catalog_client.add_job_producer(
                target_table_name,
                job.job_id,
                job.run_id,
                ProducerAction.WRITE,  # This field is ignored by FS service
                RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
            )

        # Columns - consumer
        _logger.info("Upgrading consumers...")
        consumers = self._catalog_client.get_consumers(
            source_table_name, RequestContext(request_context.UPGRADE_WORKSPACE_TABLE)
        )
        for consumer in consumers:
            if consumer and consumer.notebook:
                self._catalog_client.add_notebook_consumer(
                    {target_table_name: consumer.features},
                    consumer.notebook.notebook_id,
                    consumer.notebook.revision_id,
                    RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
                )
            if consumer and consumer.job_run:
                self._catalog_client.add_job_consumer(
                    {target_table_name: consumer.features},
                    consumer.job_run.job_id,
                    consumer.job_run.run_id,
                    RequestContext(request_context.UPGRADE_WORKSPACE_TABLE),
                )

    def _upgrade_tags(
        self,
        source_ft: FeatureTable,
        target_ft: FeatureTable,
        target_table_name: str,
        feature_tags_source,
        feature_tags_target,
        overwrite: bool,
    ):
        # Table
        if source_ft.tags == target_ft.tags:
            _logger.info("Table tags already upgraded")
        else:
            if overwrite and target_ft.tags:
                _logger.info("Overwrite mode, removing existing tags from target table")
                self._uc_spark_client.unset_table_tags(
                    target_table_name, list(target_ft.tags.keys())
                )
            _logger.info("Upgrading table tags...")
            self._uc_spark_client.set_table_tags(target_table_name, source_ft.tags)
        # Column
        if feature_tags_source == feature_tags_target:
            _logger.info("Column tags already upgraded")
        else:
            _logger.info("Upgrading column tags...")
            for feature in feature_tags_source:
                source_tags = feature_tags_source[feature]
                target_tags = feature_tags_target[feature]
                if source_tags != target_tags:
                    if overwrite and target_tags:
                        _logger.info(
                            f"Overwrite mode, removing existing column '{feature}' tags from target table"
                        )
                        self._uc_spark_client.unset_column_tags(
                            target_table_name, feature, list(target_tags.keys())
                        )
                    self._uc_spark_client.set_column_tags(
                        target_table_name, feature, source_tags
                    )

    def _upgrade_descriptions(
        self,
        source_ft: FeatureTable,
        target_ft: FeatureTable,
        target_table_name,
        ft_col_desc_map,
        target_ft_col_desc_map,
    ):
        # Don't need to consider overwrite here since it will always overwrite
        # Table
        if target_ft.description == source_ft.description:
            _logger.info("Table description already upgraded")
        else:
            _logger.info("Upgrading table description...")
            self._spark_client.set_table_comment(
                target_table_name, source_ft.description
            )
        # Column
        if ft_col_desc_map == target_ft_col_desc_map:
            _logger.info("Column descriptions already upgraded")
        else:
            _logger.info("Upgrading columns descriptions...")
            for (
                source_feature_name,
                source_feature_description,
            ) in ft_col_desc_map.items():
                if (
                    target_ft_col_desc_map[source_feature_name]
                    != source_feature_description
                ):
                    self._uc_spark_client.set_column_comment(
                        target_table_name,
                        source_feature_name,
                        source_feature_description,
                    )

    def _upgrade_pk_tk(
        self, source_ft: FeatureTable, target_table_name: str, overwrite: bool
    ):
        target_pk = self._spark_client.get_pk_from_table_create_stmt(target_table_name)
        should_overwrite = False
        # Check whether PK matches
        # Note that source_ft is from get_table which should combine tk into pk so we can
        # just do direct comparison with target_pk (from sql)
        if target_pk and target_pk != source_ft.primary_keys:
            if not overwrite:
                upgrade_utils.raise_target_table_not_match_source_table_error(
                    property="Primary keys",
                    source_workspace_table_value=source_ft.primary_keys,
                    target_uc_table_value=target_pk,
                )
            else:
                should_overwrite = True
        # Check whether TK matches
        if target_pk and len(target_pk) > 0:
            target_ft = self._fs_client.get_table(name=target_table_name)
            if target_ft.timestamp_keys != source_ft.timestamp_keys:
                if not overwrite:
                    upgrade_utils.raise_target_table_not_match_source_table_error(
                        property="Timeseries columns",
                        source_workspace_table_value=source_ft.timestamp_keys,
                        target_uc_table_value=target_ft.timestamp_keys,
                    )
                else:
                    should_overwrite = True

        if should_overwrite:
            _logger.info(
                "Overwrite mode, deleting existing primary key constraint on target table"
            )
            self._uc_spark_client.drop_pk(target_table_name)

        # Get PK again. If it doesn't exist either it never existed or we deleted existing one. In both cases we
        # need to set PK to match source table.
        if not self._spark_client.get_pk_from_table_create_stmt(target_table_name):
            source_tk = None
            if source_ft.timestamp_keys:
                source_tk = source_ft.timestamp_keys[0]
            # fs.get_table already includes tk as part of PK
            self._uc_spark_client.set_pk_tk(
                target_table_name, source_ft.primary_keys, source_tk
            )

    def _validate_metadata(
        self,
        source_ft: FeatureTable,
        ft_col_desc_map: Dict[str, str],
        feature_tags_source: Dict[str, Dict[str, str]],
        target_ft: FeatureTable,
        target_ft_col_desc_map: Dict[str, str],
        feature_tags_target: Dict[str, Dict[str, str]],
        overwrite: bool,
    ):
        # PK
        # We should never hit this case because we should've already set pk/tk by this point.
        if source_ft.primary_keys != target_ft.primary_keys:
            upgrade_utils.raise_target_table_not_match_source_table_error(
                property="Primary keys",
                source_workspace_table_value=source_ft.primary_keys,
                target_uc_table_value=target_ft.primary_keys,
            )

        # TK
        # We should never hit this case because we should've already set pk/tk by this point.
        if source_ft.timestamp_keys != target_ft.timestamp_keys:
            upgrade_utils.raise_target_table_not_match_source_table_error(
                property="Timeseries columns",
                source_workspace_table_value=source_ft.timestamp_keys,
                target_uc_table_value=target_ft.timestamp_keys,
            )

        # Partitions
        # We don't error if they don't match since we cannot set partitions to an existing delta table without a table rewrite.
        if source_ft.partition_columns != target_ft.partition_columns:
            _logger.warn(
                upgrade_utils.target_table_source_table_mismatch_msg(
                    "Partition columns",
                    source_ft.partition_columns,
                    target_ft.partition_columns,
                )
            )

        # Description
        # Table
        if target_ft.description and target_ft.description != source_ft.description:
            if not overwrite:
                upgrade_utils.raise_target_table_not_match_source_table_error(
                    property="Table description",
                    source_workspace_table_value=source_ft.description,
                    target_uc_table_value=target_ft.description,
                )
        # Column
        if not upgrade_utils.compare_column_desc_map(
            ft_col_desc_map, target_ft_col_desc_map
        ):
            if not overwrite:
                upgrade_utils.raise_target_table_not_match_source_table_error(
                    property="Column descriptions",
                    source_workspace_table_value=ft_col_desc_map,
                    target_uc_table_value=target_ft_col_desc_map,
                )
        # Tags
        # Table
        if target_ft.tags and source_ft.tags != target_ft.tags:
            if not overwrite:
                upgrade_utils.raise_target_table_not_match_source_table_error(
                    property="Table tags",
                    source_workspace_table_value=source_ft.tags,
                    target_uc_table_value=target_ft.tags,
                )
        # Column
        for feature_name in feature_tags_source:
            if (
                feature_tags_target[feature_name]
                and feature_tags_source[feature_name]
                != feature_tags_target[feature_name]
            ):
                if not overwrite:
                    upgrade_utils.raise_target_table_not_match_source_table_error(
                        property=f"Column '{feature_name}' tags",
                        source_workspace_table_value=feature_tags_source[feature_name],
                        target_uc_table_value=feature_tags_target[feature_name],
                    )
