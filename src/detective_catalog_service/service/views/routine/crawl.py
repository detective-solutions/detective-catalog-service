# import standard modules
import json

# import third party modules
from aiokafka import AIOKafkaProducer

# import project related modules
from detective_catalog_service.settings import KAFKA_SERVER, loop
from detective_catalog_service.pydataobject.event_type import CrawlEvent, CrawlBody, CrawlContext


async def initialize_crawl(source_id: str):
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=KAFKA_SERVER
    )
    await producer.start()
    try:
        event = CrawlEvent(
            context=CrawlContext(
                tenantId="c50416fc-ec70-11ec-858d-9cb6d0fe269b",
                timestamp="2022-01-01T12:01:00",
                eventType="crawlQuery",
                userId="root",
            ),
            body=CrawlBody(sourceId=source_id)
        ).dict()
        await producer.send_and_wait(topic="query_execution", value=json.dumps(event).encode("utf-8"))
    finally:
        await producer.stop()
