from detective_catalog_service.service.models.accumulo import Accumulo
from detective_catalog_service.service.models.postgresql import PostgreSQL
from detective_catalog_service.service.models.bigquery import BigQuery
from detective_catalog_service.service.models.cassandra import Cassandra

register = {
    "accumulo": Accumulo,
    "postgresql": PostgreSQL,
    "bigquery": BigQuery,
    "cassandra": Cassandra
}
