# import standard modules
import json

# import third party modules
from kafka import KafkaConsumer

# import project related modules
from detective_catalog_service.settings import KAFKA_SERVER
from detective_catalog_service.service.event import post_event
from detective_catalog_service.pydataobject.transformer import EventOperation
from detective_catalog_service.service.listeners.registration import initialize_listeners


consumer = KafkaConsumer(
    "catalog",
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    api_version=(0, 10, 2)
)

# masking service!
initialize_listeners()
for message in consumer:
    message = message.value