from databricks.feature_store.entities._feature_store_object import _FeatureStoreObject
from databricks.feature_store.entities.data_type import DataType


# This is an internal version of Feature object and should not be used outside of uc_client.
class _Feature(_FeatureStoreObject):
    def __init__(
        self,
        feature_table,
        feature_id,
        name,
        data_type,
        description,
        data_type_details=None,
    ):
        self._feature_table = feature_table
        self._name = name
        self._data_type = data_type
        self._description = description
        self._data_type_details = data_type_details
        self._feature_id = feature_id

    @property
    def feature_id(self):
        return self._feature_id

    @property
    def feature_table(self):
        return self._feature_table

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    @property
    def data_type_details(self):
        return self._data_type_details

    @property
    def description(self):
        return self._description

    @classmethod
    def from_proto(cls, feature_proto):
        return cls(
            feature_table=feature_proto.table,
            feature_id=feature_proto.id,
            name=feature_proto.name,
            data_type=DataType.to_string(feature_proto.data_type),
            data_type_details=feature_proto.data_type_details,
            description=feature_proto.description,
        )
