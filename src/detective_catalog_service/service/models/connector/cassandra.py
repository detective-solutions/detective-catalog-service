# import standard modules
from typing import Optional, Literal

# import third party module
from pydantic import Field

# import project related module
from detective_catalog_service.service.models.connector.main import PropertyModel


class Cassandra(PropertyModel):
    connectorName: str = "cassandra"
    user: str = Field(title="username", description="Username used for authentication to the Cassandra cluster. "
                                                    "This is a global setting used for all connections, regardless "
                                                    "of the user connected to detective.")
    password: str = Field(title="password", description="password for user authentication")
    contactPoints: str = Field("Host1, Host2", title="contact point",
                               description="Comma-separated list of hosts in a Cassandra cluster. The Cassandra driver "
                                           "uses these contact points to discover cluster topology. At least one "
                                           "Cassandra host is required.")
    loadPolicyDcAwareLocal: str = Field(title="name of datacenter", description="The name of the datacenter "
                                                                                "considered “local”.")
    port: Optional[int] = Field(5432, title="port", description="The Cassandra server port running the native client "
                                                                "protocol, defaults to 9042.")
    consistencyLevel: Optional[Literal[
        "ALL", "EACH_QUORUM", "QUORUM", "LOCAL_QUORUM", "ONE", "TWO", "THREE", "LOCAL_ONE", "ANY", "SERIAL",
        "LOCAL_SERIAL"]] = Field("ONE", title="consistency level",
                                 description="Consistency levels in Cassandra refer to the level"
                                             " of consistency to be used for both read and write operations."
                                             " More information about consistency levels can be found in the"
                                             " Cassandra consistency documentation. This property defaults "
                                             "to a consistency level of ONE. Possible values include ALL, "
                                             "EACH_QUORUM, QUORUM, LOCAL_QUORUM, ONE, TWO, THREE, LOCAL_ONE,"
                                             " ANY, SERIAL, LOCAL_SERIAL.")
    protocolVersion: Optional[str] = Field(title="protocol version", description="")
    fetchSize: Optional[int] = Field(None, title="fetch size", description="Number of rows fetched at a time in "
                                                                           "a Cassandra query.")
    partitionSizeForBatch: Optional[int] = Field(None, title="size for batch select",
                                                 description="Number of partitions batched together into a single "
                                                             "select for a single partion key column table.")
    splitSize: Optional[int] = Field(None, title="split size", description="Number of keys per split when "
                                                                           "querying Cassandra.")
    splitPerNode: Optional[int] = Field(None, title="split per node",
                                        description="Number of splits per node. By default, the values from the "
                                                    "system.size_estimates table are used. Only override when "
                                                    "connecting to Cassandra versions < 2.1.5, which lacks the "
                                                    "system.size_estimates table.")
    batchSize: Optional[int] = Field(None, title="batch size", description="Maximum number of statements to "
                                                                           "execute in one batch.")
    maxReadRowRetries: Optional[int] = Field(None, title="read timeout",
                                             description="Maximum time the Cassandra driver waits for an answer to a "
                                                         "query from one Cassandra node. Note that the underlying "
                                                         "Cassandra driver may retry a query against more than one node"
                                                         " in the event of a read timeout. Increasing this may help "
                                                         "with queries that use an index.")

    def as_properties(self):
        config = {
            "connector.name": self.connectorName,
            "cassandra.contact-points": self.contactPoints,
            "cassandra.load-policy.dc-aware.local-dc": self.loadPolicyDcAwareLocal,
            "cassandra.native-protocol-port": self.port,
            "cassandra.consistency-level": self.consistencyLevel,
            "cassandra.username": self.user,
            "cassandra.password": self.password

        }

        auto_default_fields = {
            "cassandra.protocol-version": self.protocolVersion,
            "cassandra.fetch-size": self.fetchSize,
            "cassandra.partition-size-for-batch-select": self.partitionSizeForBatch,
            "cassandra.split-size": self.splitSize,
            "cassandra.splits-per-node": self.splitPerNode,
            "cassandra.batch-size": self.batchSize,
            "cassandra.client.read-timeout": self.maxReadRowRetries
        }

        for key, value in auto_default_fields.items():
            if value is not None:
                config[key] = value
        return config
