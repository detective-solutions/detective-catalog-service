# import standard modules
from typing import Optional

# import third party modules
from pydantic import Field

# import project related module
from detective_catalog_service.service.models.connector.main import PropertyModel


class BigQuery(PropertyModel):
    connectorName: str = "bigquery"
    projectId: str = Field(title="big query project id", description="The Google Cloud Project ID where the "
                                                                     "data reside")
    parentProjectId: str = Field(title="big query parent project id", description="The project ID Google Cloud Project "
                                                                                  "to bill for the export")
    parallelism: Optional[str] = Field(title="partitions to split data",
                                       description="The number of partitions to split the data into. By default The "
                                                   "number of executors")
    viewsEnabled: Optional[bool] = Field(False, title="views enabled", description="Enables the connector to read from "
                                                                                   "views and not only tables.")
    viewExpireDuration: Optional[str] = Field("24h", title="view expire duration",
                                              description="Expire duration for the materialized view.")
    viewMaterializationProject: Optional[str] = Field(title="view materialization project",
                                                      description="The project  where the  materialized view is going "
                                                                  "to be created")
    viewMaterializationDataset: Optional[str] = Field(title="view materialization dataset",
                                                      description="The dataset here the materialized view is going "
                                                                  "to be created")
    skipViewMaterialization: Optional[bool] = Field(False, title="skip view materialization",
                                                    description="Use REST API to access views instead of Storage API. "
                                                                "BigQuery BIGNUMERIC and TIMESTAMP types are "
                                                                "unsupported.")
    viewCacheTTL: Optional[str] = Field("15m", title="duration for materialization",
                                        description="Duration for which the materialization of a view will be cached "
                                                    "and reused. Set to 0ms to disable the cache.")
    maxReadRowRetries: Optional[int] = Field(3, title="retries in case of issues", description="The number of retries "
                                                                                               "in case of retryable "
                                                                                               "server issues")
    credentialKey: Optional[str] = Field(None, title="credential key", description="The base64 encoded credentials key")

    # TODO: not enabled, size there is no process yet to add the configuration file automatically
    # credentialFile: Optional[str] = Field(None, title="path to credential file",
    # description="The path to the JSON credentials file")
    caseInsensitiveNameMatching: Optional[bool] = Field(False, title="case insensitive name matching",
                                                        escription="Support case insensitive schema and table names.")
    queryResultsCache: Optional[bool] = Field(False, title="cache query results",
                                              description="Enable cache of query results")

    def as_properties(self):
        config = {
            "connector.name": self.connectorName,
            "bigquery.project-id": self.projectId,
            "bigquery.parent-project-id": self.parentProjectId,
            "bigquery.views-enabled": self.viewsEnabled,
            "bigquery.view-expire-duration": self.viewExpireDuration,
            "bigquery.skip-view-materialization": self.skipViewMaterialization,
            "bigquery.views-cache-ttl": self.viewCacheTTL,
            "bigquery.max-read-rows-retries": self.maxReadRowRetries,
            "bigquery.case-insensitive-name-matching": self.caseInsensitiveNameMatching,
            "bigquery.query-results-cache.enabled": self.queryResultsCache
        }

        auto_default_fields = {
            "bigquery.parallelism": self.parallelism,
            "bigquery.view-materialization-project": self.viewMaterializationProject,
            "bigquery.view-materialization-dataset": self.viewMaterializationDataset,
            "bigquery.credentials-key": self.credentialKey
        }

        for key, value in auto_default_fields.items():
            if value is not None:
                config[key] = value

        return config
