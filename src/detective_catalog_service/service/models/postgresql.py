# import standard modules
from typing import Optional

# import third party modules
from pydantic import Field

# import project related modules
from detective_catalog_service.service.models.main import PropertyModel


class PostgreSQL(PropertyModel):
    connectorName: str = "postgresql"
    host: str = Field(title="host address", description="Host address of the postgres server")
    databaseSchema: str = Field(title="database schema", description="schema (e.g. public) to be used for queries")
    database: str = Field(title="database name", description="database to be used for queries")
    user: str = Field("root", title="username", description="username used for queries")
    password: str = Field(title="password", description="password for user authentication")
    port: Optional[int] = Field(5432, title="port", description="port used by the postgresql server")
    ssl: Optional[bool] = Field(False, title="ssl security", description="If you have TLS configured with a "
                                                                         "globally-trusted certificate installed on "
                                                                         "your data source, you can enable TLS between "
                                                                         "your cluster and the data source")
    metaDataCacheMaximumSize: Optional[int] = Field(10000, title="Metadata cache size", description="Maximum number of "
                                                                                                    "objects stored "
                                                                                                    "in the metadata "
                                                                                                    "cache")
    batchSize: Optional[int] = Field(1000, title="batch size", description="Maximum number of statements in a "
                                                                                "batched execution. Do not change this "
                                                                                "setting from the default. Non-default "
                                                                                "values may negatively impact "
                                                                                "performance.")

    # TODO: not enabled, size there is no process yet to add the configuration file automatically
    # caseInsensitiveNameMatching: Optional[bool] = Field(False, title="case insensitive name matching",
    # description="Support case insensitive schema and table names.")
    # caseInsensitiveNameMatchingCacheTTL: Optional[str] = Field("1m", title="case insensitive name matching cache ttl")
    # caseInsensitiveNameMatchingConfigFile: Optional[str] = Field(Null, title="case sensitive mapping",
    # description="Path to a name mapping configuration file in JSON format that allows Trino to disambiguate between
    # schemas and tables with similar names in different cases."

    def as_properties(self):
        return {
            "connector.name": self.connectorName,
            "connection-url": f"jdbc:postgresql://{self.host}:{self.port}/{self.database}?ssl={self.ssl}",
            "connection-user": self.user,
            "connection-password": self.password,
            # "case-insensitive-name-matching": self.caseInsensitiveNameMatching,
            # "case-insensitive-name-matching.cache-ttl": self.caseInsensitiveNameMatchingCacheTTLs,
            # "case-insensitive-name-matching.config-file": self.caseInsensitiveNameMatchingConfigFile
            "metadata.cache-maximum-size": self.metaDataCacheMaximumSize,
            "write.batch-size": self.batchSize
        }