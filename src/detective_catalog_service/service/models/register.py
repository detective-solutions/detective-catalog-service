from detective_catalog_service.service.models.connector.accumulo import Accumulo
from detective_catalog_service.service.models.connector.postgresql import PostgreSQL
from detective_catalog_service.service.models.connector.bigquery import BigQuery
from detective_catalog_service.service.models.connector.cassandra import Cassandra


class Register:

    REGISTER = {
        "accumulo": Accumulo,
        "postgresql": PostgreSQL,
        "bigquery": BigQuery,
        "cassandra": Cassandra
    }

    @classmethod
    def get(cls, connector_name: str):
        return cls.REGISTER[connector_name]

    @classmethod
    def list(cls):
        return [
            {"connectorName": key, "displayName": value.__name__}
            for key, value in cls.REGISTER.items()
        ]
