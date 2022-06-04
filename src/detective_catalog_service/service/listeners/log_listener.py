# ACCUMULO
# connector.name=accumulo
# accumulo.instance=xxx
# accumulo.zookeepers=xxx
# accumulo.username=username
# accumulo.password=password

# ATOP
# connector.name=atop
# atop.executable-path=/usr/bin/atop

# BIGQUERY
# connector.name=bigquery
# bigquery.project-id=<your Google Cloud Platform project id>

# BLACKHOLE
# connector.name=blackhole

# CASSANDRA
# connector.name=cassandra
# cassandra.contact-points=host1,host2
# cassandra.load-policy.dc-aware.local-dc=datacenter1

# CLICKHOUSE
# connector.name=clickhouse
# connection-url=jdbc:clickhouse://host1:8123/
# connection-user=exampleuser
# connection-password=examplepassword

# HIVE META STORE
# connector.name=delta-lake
# hive.metastore.uri=thrift://example.net:9083

# AWS GLUE
# connector.name=delta-lake
# hive.metastore=glue

# AZURE DATA LAKE 2
# hive.config.resources=<path_to_hadoop_core-site.xml>
# hive.azure.abfs-storage-account
# hive.azure.abfs-access-key

# DRUID
# connector.name=druid
# connection-url=jdbc:avatica:remote:url=http://BROKER:8082/druid/v2/sql/avatica/
# connection-url=jdbc:avatica:remote:url=http://BROKER:port/druid/v2/sql/avatica/;authentication=BASIC
# connection-user=root
# connection-password=secret

# ELASTIC SEARCH
# connector.name=elasticsearch
# elasticsearch.host=localhost
# elasticsearch.port=9200
# elasticsearch.default-schema-name=default

# GOOGLE SHEETS
# connector.name=gsheets
# credentials-path=/path/to/google-sheets-credentials.json
# metadata-sheet-id=exampleId

# JMX
# connector.name=jmx
# jmx.dump-tables=java.lang:type=Runtime,trino.execution.scheduler:name=NodeScheduler
# jmx.dump-period=10s
# jmx.max-entries=86400

# KAFKA
# connector.name=kafka
# kafka.table-names=table1,table2
# kafka.nodes=host1:port,host2:port
# kafka.config.resources=/etc/kafka-configuration.properties

# AWS kinesis
# connector.name=kinesis
# kinesis.access-key=XXXXXX
# kinesis.secret-key=XXXXXX

# KUDU
# connector.name=kudu
# kudu.authentication.type = NONE
# kudu.client.master-addresses=localhost

# LOCAL FILE
# connector.name=localfile

# MARIA DB
# connector.name=mariadb
# connection-url=jdbc:mariadb://example.net:3306
# connection-user=root
# connection-password=secret

# MEMORY CONNECTOR
# connector.name=memory
# memory.max-data-per-node=128MB

# MONGO DB
# connector.name=mongodb
# mongodb.connection-url=mongodb://user:pass@sample.host:27017/

# MYSQL
# connector.name=mysql
# connection-url=jdbc:mysql://example.net:3306
# connection-user=root
# connection-password=secret

# ORACLE
# connector.name=oracle
# connection-url=jdbc:oracle:thin:@example.net:1521:orcl
# connection-user=root
# connection-password=secret

# PHOENIX
# connector.name=phoenix (5)
# phoenix.connection-url=jdbc:phoenix:host1,host2,host3:2181:/hbase
# phoenix.config.resources=/path/to/hbase-site.xml

# PINOT
# connector.name=pinot
# pinot.controller-urls=host1:8098,host2:8098
#

# POSTGRESQL
# connector.name=postgresql
# connection-url=jdbc:postgresql://example.net:5432/database
# connection-user=root
# connection-password=secret

# PROMETHEUS
# connector.name=prometheus
# prometheus.uri=http://localhost:9090
# prometheus.query.chunk.size.duration=1d
# prometheus.max.query.range.duration=21d
# prometheus.cache.ttl=30s
# prometheus.bearer.token.file=/path/to/bearer/token/file
# prometheus.read-timeout=10s

# REDIS
# connector.name=redis
# redis.table-names=schema1.table1,schema1.table2
# redis.nodes=host:port

# AWS REDSHIFT
# connector.name=redshift
# connection-url=jdbc:redshift://example.net:5439/database
# connection-user=root
# connection-password=secret

# SINGLE STORE
# connector.name=singlestore
# connection-url=jdbc:singlestore://example.net:3306
# connection-user=root
# connection-password=secret

