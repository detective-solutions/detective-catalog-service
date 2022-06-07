from detective_catalog_service.service.models.connector.accumulo import Accumulo
from detective_catalog_service.service.models.connector.postgresql import PostgreSQL
from detective_catalog_service.service.models.connector.bigquery import BigQuery
from detective_catalog_service.service.models.connector.cassandra import Cassandra

register = {
    "accumulo": Accumulo,
    "postgresql": PostgreSQL,
    "bigquery": BigQuery,
    "cassandra": Cassandra
}
