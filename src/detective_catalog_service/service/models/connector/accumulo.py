# import standard modules
from typing import Optional

# import third party modules
from pydantic import Field

# import project related module
from detective_catalog_service.service.models.connector.main import PropertyModel


class Accumulo(PropertyModel):
    connectorName: str = "accumulo"
    instance: str = Field(title="instance", description="Name of the Accumulo instance")
    zookeepers: str = Field(title="zookeepers", description="ZooKeeper connect string")
    user: Optional[str] = Field("root", title="username",
                                description="Accumulo user to be used by query engine default root")
    password: str = Field(title="password", description="Accumulo password for user")
    zookeeperMetadataRoot: Optional[str] = Field("/presto-models",
                                                 title="zookeeper metadata root",
                                                 description="Root znode for storing metadata."
                                                 "Only relevant if using default Metadata Manager")
    cardinalityCacheSize: Optional[int] = Field(10000, title="cardinality cache size",
                                                description="Sets the size of the index cardinality cache")
    cardinalityCacheExpireDuration: Optional[str] = Field("5m", title="cardinality cache expire duration",
                                                          description="Sets the expiration duration of the cardinality"
                                                          "cache.")

    def as_properties(self):
        return {
          "connector.name": self.connectorName,
          "models.instance": self.instance,
          "models.zookeepers": self.zookeepers,
          "models.username": self.user,
          "models.password": self.password,
          "models.zookeeper.metadata.root": self.zookeeperMetadataRoot,
          "models.cardinality.cache.size": self.cardinalityCacheSize,
          "models.cardinality.cache.expire.duration": self.cardinalityCacheExpireDuration
        }
