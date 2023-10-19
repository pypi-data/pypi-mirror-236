import json
import logging
from typing import List

from databricks.feature_engineering.entities.feature import _Feature
from databricks.feature_store.api.proto.feature_catalog_pb2 import GetFeatures, GetTags
from databricks.feature_store.catalog_client import CatalogClient
from databricks.feature_store.entities.tag import Tag
from databricks.feature_store.utils import request_context, rest_utils
from databricks.feature_store.utils.request_context import RequestContext
from databricks.feature_store.utils.uc_utils import reformat_full_table_name

_logger = logging.getLogger(__name__)


class UcClient:
    def __init__(self, catalog_client: CatalogClient):
        self._catalog_client = catalog_client

    # Makes HTTP request to FS service without using protos.
    def upgrade_to_uc(self, source_table_name: str, target_table_name: str):
        body = {
            "source_table_name": source_table_name,
            "target_table_name": target_table_name,
        }
        req_context = RequestContext(request_context.UPGRADE_WORKSPACE_TABLE)
        endpoint = "/api/2.0/feature-store/feature-tables/upgrade-to-uc"
        response = rest_utils.http_request(
            host_creds=self._catalog_client._get_host_creds(),
            endpoint=endpoint,
            method="POST",
            json=body,
            extra_headers=req_context.get_headers(),
            timeout=rest_utils._DEFAULT_TIMEOUT_SECONDS,
        )
        response = rest_utils.verify_rest_response(response, endpoint)
        js_dict = json.loads(response.text)
        return js_dict

    def get_feature_tags(
        self, feature_id: str, req_context: RequestContext
    ) -> List[Tag]:
        req_body = GetTags(feature_id=feature_id)
        response_proto = self._catalog_client._call_endpoint(
            GetTags, req_body, req_context
        )
        return [Tag.from_proto(tag_proto) for tag_proto in response_proto.tags]

    def get_features(
        self, feature_table: str, req_context: RequestContext
    ) -> List[_Feature]:
        all_features = []
        page_token = None
        while True:
            # Use default max_results
            req_body = GetFeatures(
                feature_table=reformat_full_table_name(feature_table),
                page_token=page_token,
            )
            response_proto = self._catalog_client._call_endpoint(
                GetFeatures, req_body, req_context
            )
            all_features.extend(
                [_Feature.from_proto(feature) for feature in response_proto.features]
            )
            page_token = response_proto.next_page_token
            if not page_token:
                break
        return all_features
