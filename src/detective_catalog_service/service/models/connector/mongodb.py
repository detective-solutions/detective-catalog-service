# import standard modules
from typing import Optional

# import third party modules
from pydantic import Field

# import project related modules
from detective_catalog_service.service.models.connector.main import PropertyModel


class MongoDB(PropertyModel):
    connectorName: str = "mongodb"
    host: str = Field(title="Host address", description="Host address of the postgres server")
    collection: str = Field(title="Collection", description="A collection which contains schema information")
    user: str = Field(title="Username", description="username used for queries")
    password: str = Field(title="Password", description="password for user authentication")
    port: Optional[int] = Field(27017, title="Port", description="port used by the postgresql server")
    ssl: Optional[bool] = Field(False, title="SSL security", description="Use TLS/SSL for connections to mongod/mongos")

    def as_properties(self):
        return {
            "connector.name": self.connectorName,
            "mongodb.connection-url": f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/",
            "mongodb.schema-collection": self.collection,
            "mongodb.case-insensitive-name-matching": "true",
            "mongodb.ssl.enabled": f"{self.ssl}",
        }
