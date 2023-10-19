import logging
from types import ModuleType
from typing import Any, Dict, List, Optional, Union

import mlflow
from mlflow.utils.annotations import experimental
from pyspark.sql import DataFrame
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType

from databricks.feature_store.client import FeatureStoreClient
from databricks.feature_store.constants import (
    _DEFAULT_PUBLISH_STREAM_TRIGGER,
    _DEFAULT_WRITE_STREAM_TRIGGER,
    MERGE,
)
from databricks.feature_store.entities.feature_function import FeatureFunction
from databricks.feature_store.entities.feature_lookup import FeatureLookup

try:
    # The new classes are available in databricks-feature-store 0.15+ only
    from databricks.feature_store.entities.feature_serving_endpoint import (
        EndpointCoreConfig,
        FeatureServingEndpoint,
    )
    from databricks.feature_store.entities.feature_spec_info import FeatureSpecInfo
except ImportError:
    # We only use them for type hints, so it's fine to set them to None
    EndpointCoreConfig = None
    FeatureServingEndpoint = None
    FeatureSpecInfo = None

from databricks.feature_store.entities.feature_table import FeatureTable
from databricks.feature_store.online_store_publish_client import (
    NOSQL_SPECS,
    is_rdbms_spec,
)
from databricks.feature_store.online_store_spec import OnlineStoreSpec
from databricks.feature_store.training_set import TrainingSet
from databricks.feature_store.utils import uc_utils
from databricks.feature_store.utils.utils import as_list

_logger = logging.getLogger(__name__)


class FeatureEngineeringClient:
    """
    Client for interacting with the Databricks Feature Engineering in Unity Catalog.
    """

    def __init__(
        self,
        *,
        model_registry_uri: Optional[str] = None,
    ):
        """
        Initialize a client to interact with Feature Engineering in Unity Catalog.

        Creates a client to interact with Feature Engineering in Unity Catalog.

        :param model_registry_uri: Address of local or remote model registry server. If not provided,
          defaults to the local server.
        """
        self._fs_client = FeatureStoreClient(model_registry_uri=model_registry_uri)

    def _validate_is_uc_table_name(self, name: str) -> None:
        full_name = uc_utils.get_full_table_name(
            name,
            self._fs_client._spark_client.get_current_catalog(),
            self._fs_client._spark_client.get_current_database(),
        )
        if not uc_utils.is_uc_entity(full_name):
            raise ValueError(
                "FeatureEngineeringClient only supports feature tables in Unity Catalog. "
                "For feature tables in hive metastore, use databricks.feature_store.FeatureStoreClient."
            )

    @experimental
    def create_feature_serving_endpoint(
        self,
        *,
        name: str = None,
        config: EndpointCoreConfig = None,
        **kwargs,
    ) -> FeatureServingEndpoint:
        """
        Experimental feature: Creates a Feature Serving Endpoint

        :param name: The name of the endpoint. Must only contain alphanumerics and dashes.
        :param config: Configuration of the endpoint, including features, workload_size, etc.
        """
        return self._fs_client.create_feature_serving_endpoint(
            name=name, config=config, **kwargs
        )

    @experimental
    def create_feature_spec(
        self,
        *,
        name: str,
        features: List[Union[FeatureLookup, FeatureFunction]],
        exclude_columns: Optional[List[str]] = None,
        **kwargs,
    ) -> FeatureSpecInfo:
        """
        Experimental feature: Creates a feature specification in Unity Catalog. The feature spec can be used for serving features & functions.

        :param name: The name of the feature spec.
        :param features: List of FeatureLookups and FeatureFunctions to include in the feature spec.
        :param exclude_columns: List of columns to drop from the final output.
        """
        for feature in features:
            if type(feature) == FeatureLookup:
                self._validate_is_uc_table_name(feature.table_name)

        return self._fs_client.create_feature_spec(
            name=name, features=features, exclude_columns=exclude_columns, **kwargs
        )

    def create_table(
        self,
        *,
        name: str,
        primary_keys: Union[str, List[str]],
        df: Optional[DataFrame] = None,
        timeseries_columns: Union[str, List[str], None] = None,
        partition_columns: Union[str, List[str], None] = None,
        schema: Optional[StructType] = None,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> FeatureTable:
        """
        Create and return a feature table with the given name and primary keys.

        The returned feature table has the given name and primary keys.
        Uses the provided ``schema`` or the inferred schema
        of the provided ``df``. If ``df`` is provided, this data will be saved in
        a Delta table. Supported data types for features are: ``IntegerType``, ``LongType``,
        ``FloatType``, ``DoubleType``, ``StringType``, ``BooleanType``, ``DateType``,
        ``TimestampType``, ``ShortType``, ``ArrayType``, ``MapType``, and ``BinaryType``,
        and ``DecimalType``.

        :param name: A feature table name.
          For workspace-local feature table, the format is ``<database_name>.<table_name>``, for example ``dev.user_features``.
          For feature table in Unity Catalog, the format is ``<catalog_name>.<schema_name>.<table_name>``, for example ``ml.dev.user_features``.
        :param primary_keys: The feature table's primary keys. If multiple columns are required,
          specify a list of column names, for example ``['customer_id', 'region']``.
        :param df: Data to insert into this feature table. The schema of
          ``df`` will be used as the feature table schema.
        :param timeseries_columns: Columns containing the event time associated with feature value.
          Timeseries columns should be part of the primary keys.
          Combined, the timeseries columns and other primary keys of the feature table uniquely identify the feature value
          for an entity at a point in time.


          .. note::

             Experimental: This argument may change or be removed in
             a future release without warning.

        :param partition_columns: Columns used to partition the feature table. If a list is
          provided, column ordering in the list will be used for partitioning.

          .. Note:: When choosing partition columns for your feature table, use columns that do
                    not have a high cardinality. An ideal strategy would be such that you
                    expect data in each partition to be at least 1 GB.
                    The most commonly used partition column is a ``date``.

                    Additional info: `Choosing the right partition columns for Delta tables
                    <https://bit.ly/3ueXsjv>`_
        :param schema: Feature table schema. Either ``schema`` or ``df`` must be provided.
        :param description: Description of the feature table.
        :param tags: Tags to associate with the feature table.
        """
        self._validate_is_uc_table_name(name)

        if timeseries_columns is None and "timestamp_keys" in kwargs:
            timeseries_columns = kwargs.pop("timestamp_keys")

        timeseries_columns_as_list = as_list(timeseries_columns, default=[])
        primary_keys_as_list = as_list(primary_keys, default=[])
        for tk in timeseries_columns_as_list:
            if tk not in primary_keys_as_list:
                raise ValueError(
                    f"Timeseries column '{tk}' is not in primary_keys. "
                    f"Timeseries columns must be primary keys."
                )

        return self._fs_client.create_table(
            name=name,
            primary_keys=primary_keys,
            df=df,
            timestamp_keys=timeseries_columns,
            partition_columns=partition_columns,
            schema=schema,
            description=description,
            tags=tags,
            **kwargs,
        )

    def create_training_set(
        self,
        *,
        df: DataFrame,
        feature_lookups: List[Union[FeatureLookup, FeatureFunction]],
        label: Union[str, List[str], None],
        exclude_columns: Optional[List[str]] = None,
        **kwargs,
    ) -> TrainingSet:
        """
        Create a :class:`TrainingSet <databricks.feature_store.training_set.TrainingSet>`.

        :param df: The :class:`DataFrame <pyspark.sql.DataFrame>` used to join features into.
        :param feature_lookups: List of features to use in the :class:`TrainingSet <databricks.feature_store.training_set.TrainingSet>`.
          :class:`FeatureLookups <databricks.feature_store.entities.feature_lookup.FeatureLookup>` are
          joined into the :class:`DataFrame <pyspark.sql.DataFrame>`, and
          :class:`FeatureFunctions <databricks.feature_store.entities.feature_function.FeatureFunction>` are
          computed on-demand.

        :param label: Names of column(s) in :class:`DataFrame <pyspark.sql.DataFrame>` that contain training set labels. To create a training set without a label field, i.e. for unsupervised training set, specify label = None.
        :param exclude_columns: Names of the columns to drop from the :class:`TrainingSet <databricks.feature_store.training_set.TrainingSet>` :class:`DataFrame <pyspark.sql.DataFrame>`.
        :return: A :class:`TrainingSet <databricks.feature_store.training_set.TrainingSet>` object.
        """
        for feature_lookup in feature_lookups:
            if type(feature_lookup) == FeatureLookup:
                self._validate_is_uc_table_name(feature_lookup.table_name)

        return self._fs_client.create_training_set(
            df=df,
            feature_lookups=feature_lookups,
            label=label,
            exclude_columns=exclude_columns,
            **kwargs,
        )

    @experimental
    def delete_feature_serving_endpoint(self, *, name=None, **kwargs) -> None:
        """Experimental feature"""
        self._fs_client.delete_feature_serving_endpoint(name=name, **kwargs)

    def delete_feature_table_tag(self, *, name: str, key: str) -> None:
        """
        Delete the tag associated with the feature table. Deleting a non-existent tag will emit a warning.

        :param name: the feature table name.
        :param key: the tag key to delete.
        """
        self._validate_is_uc_table_name(name)
        return self._fs_client.delete_feature_table_tag(table_name=name, key=key)

    def drop_online_table(
        self,
        name: str,
        online_store: OnlineStoreSpec,
    ) -> None:
        """
        Drop a table in an online store.

        This API first attempts to make a call to the online store provider to drop the table.
        If successful, it then deletes the online store from the feature catalog.

        :param name: Name of feature table associated with online store table to drop.
        :param online_store: Specification of the online store.

        .. note::
            Deleting an online published table can lead to unexpected failures in downstream
            dependencies. Ensure that the online table being dropped is no longer used for
            Model Serving feature lookup or any other use cases.
        """
        self._validate_is_uc_table_name(name)
        return self._fs_client.drop_online_table(name=name, online_store=online_store)

    def drop_table(self, *, name: str) -> None:
        """
        Delete the specified feature table. This API also drops the underlying Delta table.

        :param name: A feature table name. The format is ``<catalog_name>.<schema_name>.<table_name>``, for example ``ml.dev.user_features``.

        .. note::
            Deleting a feature table can lead to unexpected failures in  upstream producers and
            downstream consumers (models, endpoints, and scheduled jobs). You must delete any existing
            published online stores separately.
        """
        self._validate_is_uc_table_name(name)
        return self._fs_client.drop_table(name=name)

    @experimental
    def get_feature_serving_endpoint(
        self, *, name=None, **kwargs
    ) -> FeatureServingEndpoint:
        """Experimental feature"""
        return self._fs_client.get_feature_serving_endpoint(name=name, **kwargs)

    def get_table(self, *, name: str) -> FeatureTable:
        """
        Get a feature table's metadata.

        :param name: A feature table name. The format is ``<catalog_name>.<schema_name>.<table_name>``, for example ``ml.dev.user_features``.
        """
        self._validate_is_uc_table_name(name)
        return self._fs_client.get_table(name=name)

    def log_model(
        self,
        *,
        model: Any,
        artifact_path: str,
        flavor: ModuleType,
        training_set: Optional[TrainingSet] = None,
        registered_model_name: Optional[str] = None,
        await_registration_for: int = mlflow.tracking._model_registry.DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
        **kwargs,
    ):
        """
        Log an MLflow model packaged with feature lookup information.

        .. note::

           The :class:`DataFrame <pyspark.sql.DataFrame>` returned
           by :meth:`.TrainingSet.load_df` **must** be used to train the
           model. If it has been modified (for example data normalization, add a column,
           and similar), these modifications will not be applied at inference time,
           leading to training-serving skew.


        :param model: Model to be saved. This model must be capable of being saved by
          ``flavor.save_model``. See the `MLflow Model API
          <https://bit.ly/3yzl1r0>`_.
        :param artifact_path: Run-relative artifact path.
        :param flavor: MLflow module to use to log the model. ``flavor`` should have
          type :obj:`ModuleType <types.ModuleType>`.
          The module must have a method ``save_model``, and must support the ``python_function``
          flavor. For example, :mod:`mlflow.sklearn`, :mod:`mlflow.xgboost`, and similar.
        :param training_set: The :class:`.TrainingSet` used to train this model.
        :param registered_model_name:

          .. note::

             Experimental: This argument may change or be removed in
             a future release without warning.

          If given, create a model version under ``registered_model_name``,
          also creating a registered model if one with the given name does not exist.
        :param await_registration_for: Number of seconds to wait for the model version to finish
          being created and is in ``READY`` status. By default, the function waits for five minutes.
          Specify ``0`` or :obj:`None` to skip waiting.
        :param infer_input_example:

          .. note::

             Experimental: This argument requires databricks-feature-store v0.15+,
             and may change or be removed in a future release without warning.

          Automatically log an input example along with the model, using supplied training data.
          Defaults to ``False``.
        :return: `None`
        """
        if training_set is not None:
            feature_spec = training_set.feature_spec
            table_infos = feature_spec.table_infos
            for table_info in table_infos:
                self._validate_is_uc_table_name(table_info.table_name)

        return self._fs_client.log_model(
            model=model,
            artifact_path=artifact_path,
            flavor=flavor,
            training_set=training_set,
            registered_model_name=registered_model_name,
            await_registration_for=await_registration_for,
            **kwargs,
        )

    def publish_table(
        self,
        *,
        name: str,
        online_store: OnlineStoreSpec,
        filter_condition: Optional[str] = None,
        mode: str = MERGE,
        streaming: bool = False,
        checkpoint_location: Optional[str] = None,
        trigger: Dict[str, Any] = _DEFAULT_PUBLISH_STREAM_TRIGGER,
        features: Union[str, List[str], None] = None,
    ) -> Optional[StreamingQuery]:
        """
        Publish a feature table to an online store.

        :param name: Name of the feature table.
        :param online_store: Specification of the online store.
        :param filter_condition: A SQL expression using feature table columns that filters feature
          rows prior to publishing to the online store. For example, ``"dt > '2020-09-10'"``. This
          is analogous to running ``df.filter`` or a ``WHERE`` condition in SQL on a feature table
          prior to publishing.
        :param mode: Specifies the behavior when data already exists in this feature
          table. The only supported mode is ``"merge"``, with which the new data will be
          merged in, under these conditions:

          * If a key exists in the online table but not the offline table,
            the row in the online table is unmodified.

          * If a key exists in the offline table but not the online table,
            the offline table row is inserted into the online table.

          * If a key exists in both the offline and the online tables,
            the online table row will be updated.

        :param streaming: If ``True``, streams data to the online store.
        :param checkpoint_location: Sets the Structured Streaming ``checkpointLocation`` option.
          By setting a ``checkpoint_location``, Spark Structured Streaming will store
          progress information and intermediate state, enabling recovery after failures.
          This parameter is only supported when ``streaming=True``.
        :param trigger: If ``streaming=True``, ``trigger`` defines the timing of
          stream data processing. The dictionary will be unpacked and passed
          to :meth:`DataStreamWriter.trigger <pyspark.sql.streaming.DataStreamWriter.trigger>` as arguments. For example, ``trigger={'once': True}``
          will result in a call to ``DataStreamWriter.trigger(once=True)``.
        :param features: Specifies the feature column(s) to be published to the online store.
          The selected features must be a superset of existing online store features. Primary key columns
          and timestamp key columns will always be published.

          .. Note:: When ``features`` is not set, the whole feature table will be published.

        :return: If ``streaming=True``, returns a PySpark :class:`StreamingQuery <pyspark.sql.streaming.StreamingQuery>`, :obj:`None` otherwise.
        """
        self._validate_is_uc_table_name(name)

        if mode != MERGE:
            raise ValueError(
                f"Unsupported mode '{mode}'. '{MERGE}' is the only supported mode."
            )

        if is_rdbms_spec(online_store):
            raise ValueError(
                f"Unsupported online store '{online_store}'. Use one of {NOSQL_SPECS}."
            )

        return self._fs_client.publish_table(
            name=name,
            online_store=online_store,
            filter_condition=filter_condition,
            mode=mode,
            streaming=streaming,
            checkpoint_location=checkpoint_location,
            trigger=trigger,
            features=features,
        )

    def read_table(self, *, name: str, **kwargs) -> DataFrame:
        """
        Read the contents of a feature table.

        :param name: A feature table name. The format is ``<catalog_name>.<schema_name>.<table_name>``, for example ``ml.dev.user_features``.
        :return: The feature table contents, or an exception will be raised if this feature table does not
          exist.
        """
        self._validate_is_uc_table_name(name)
        return self._fs_client.read_table(name=name, **kwargs)

    def score_batch(
        self, *, model_uri: str, df: DataFrame, result_type: str = "double"
    ) -> DataFrame:
        """
        Evaluate the model on the provided :class:`DataFrame <pyspark.sql.DataFrame>`.

        Additional features required for
        model evaluation will be automatically retrieved from feature tables.

        .. todo::

           [ML-15539]: Replace the bitly URL in doc string

        The model must have been logged with :meth:`.FeatureEngineeringClient.log_model`,
        which packages the model with feature metadata. Unless present in ``df``,
        these features will be looked up from feature tables and joined with ``df``
        prior to scoring the model.

        If a feature is included in ``df``, the provided feature values will be used rather
        than those stored in feature tables.

        For example, if a model is trained on two features ``account_creation_date`` and
        ``num_lifetime_purchases``, as in:

        .. code-block:: python

            feature_lookups = [
                FeatureLookup(
                    table_name = 'trust_and_safety.customer_features',
                    feature_name = 'account_creation_date',
                    lookup_key = 'customer_id',
                ),
                FeatureLookup(
                    table_name = 'trust_and_safety.customer_features',
                    feature_name = 'num_lifetime_purchases',
                    lookup_key = 'customer_id'
                ),
            ]

            with mlflow.start_run():
                training_set = fe.create_training_set(
                    df,
                    feature_lookups = feature_lookups,
                    label = 'is_banned',
                    exclude_columns = ['customer_id']
                )
                ...
                  fe.log_model(
                    model,
                    "model",
                    flavor=mlflow.sklearn,
                    training_set=training_set,
                    registered_model_name="example_model"
                  )

        Then at inference time, the caller of :meth:`FeatureEngineeringClient.score_batch` must pass
        a :class:`DataFrame <pyspark.sql.DataFrame>` that includes ``customer_id``, the ``lookup_key`` specified in the
        ``FeatureLookups`` of the :mod:`training_set <databricks.feature_store.training_set>`.
        If the :class:`DataFrame <pyspark.sql.DataFrame>` contains a column
        ``account_creation_date``, the values of this column will be used
        in lieu of those in feature tables. As in:

        .. code-block:: python

            # batch_df has columns ['customer_id', 'account_creation_date']
            predictions = fe.score_batch(
                'models:/example_model/1',
                batch_df
            )

        :param model_uri: The location, in URI format, of the MLflow model logged using
          :meth:`FeatureEngineeringClient.log_model`. One of:

            * ``runs:/<mlflow_run_id>/run-relative/path/to/model``

            * ``models:/<model_name>/<model_version>``

            * ``models:/<model_name>/<stage>``

          For more information about URI schemes, see
          `Referencing Artifacts <https://bit.ly/3wnrseE>`_.
        :param df: The :class:`DataFrame <pyspark.sql.DataFrame>` to score the model on. Features from feature tables will be joined with
          ``df`` prior to scoring the model. ``df`` must:

              1. Contain columns for lookup keys required to join feature data from feature
              tables, as specified in the ``feature_spec.yaml`` artifact.

              2. Contain columns for all source keys required to score the model, as specified in
              the ``feature_spec.yaml`` artifact.

              3. Not contain a column ``prediction``, which is reserved for the model's predictions.
              ``df`` may contain additional columns.

          Streaming DataFrames are not supported.

        :param result_type: The return type of the model.
           See :func:`mlflow.pyfunc.spark_udf` result_type.
        :return: A :class:`DataFrame <pyspark.sql.DataFrame>`
           containing:

            1. All columns of ``df``.

            2. All feature values retrieved from feature tables.

            3. A column ``prediction`` containing the output of the model.

        """
        return self._fs_client.score_batch(
            model_uri=model_uri, df=df, result_type=result_type
        )

    def set_feature_table_tag(self, *, name: str, key: str, value: str) -> None:
        """
        Create or update a tag associated with the feature table. If the tag with the
        corresponding key already exists, its value will be overwritten with the new value.

        :param name: the feature table name
        :param key: tag key
        :param value: tag value
        """
        self._validate_is_uc_table_name(name)
        return self._fs_client.set_feature_table_tag(
            table_name=name, key=key, value=value
        )

    def write_table(
        self,
        *,
        name: str,
        df: DataFrame,
        mode: str = MERGE,
        checkpoint_location: Optional[str] = None,
        trigger: Dict[str, Any] = _DEFAULT_WRITE_STREAM_TRIGGER,
    ) -> Optional[StreamingQuery]:
        """
        Writes to a feature table.

        If the input :class:`DataFrame <pyspark.sql.DataFrame>` is streaming, will create a write stream.

        :param name: A feature table name. The format is ``<catalog_name>.<schema_name>.<table_name>``, for example ``ml.dev.user_features``.
        :param df: Spark :class:`DataFrame <pyspark.sql.DataFrame>` with feature data. Raises an exception if the schema does not
          match that of the feature table.
        :param mode: There is only one supported write mode:

          * ``"merge"`` upserts the rows in ``df`` into the feature table. If ``df`` contains
            columns not present in the feature table, these columns will be added as new features.

          If you want to overwrite a table, drop and recreate it.

        :param checkpoint_location: Sets the Structured Streaming ``checkpointLocation`` option.
          By setting a ``checkpoint_location``, Spark Structured Streaming will store
          progress information and intermediate state, enabling recovery after failures.
          This parameter is only supported when the argument ``df`` is a streaming :class:`DataFrame <pyspark.sql.DataFrame>`.
        :param trigger: If ``df.isStreaming``, ``trigger`` defines the timing of stream data
          processing, the dictionary will be unpacked and passed to :meth:`DataStreamWriter.trigger <pyspark.sql.streaming.DataStreamWriter.trigger>`
          as arguments. For example, ``trigger={'once': True}`` will result in a call to
          ``DataStreamWriter.trigger(once=True)``.
        :return: If ``df.isStreaming``, returns a PySpark :class:`StreamingQuery <pyspark.sql.streaming.StreamingQuery>`. :obj:`None` otherwise.
        """
        self._validate_is_uc_table_name(name)

        if mode != MERGE:
            raise ValueError(
                f"Unsupported mode '{mode}'. '{MERGE}' is the only supported mode. If you want to overwrite a table, drop and recreate it."
            )

        return self._fs_client.write_table(
            name=name,
            df=df,
            mode=mode,
            checkpoint_location=checkpoint_location,
            trigger=trigger,
        )
