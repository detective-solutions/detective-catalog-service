# import standard modules
import json
from datetime import datetime as dt

# import third party modules
from aiokafka import AIOKafkaProducer

# import project related modules
from detective_catalog_service.settings import KAFKA_SERVER, loop
from detective_catalog_service.pydataobject.event_type import CrawlEvent, CrawlBody, CrawlContext


async def initialize_crawl(source_id: str, tenant_id: str):
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=KAFKA_SERVER
    )
    await producer.start()
    try:
        event = CrawlEvent(
            context=CrawlContext(
                tenantId=tenant_id,
                timestamp=str(dt.now()),
                eventType="crawlQuery",
                userId="root",
            ),
            body=CrawlBody(sourceId=source_id)
        ).dict()
        await producer.send(topic="query_execution", value=json.dumps(event).encode("utf-8"))
    finally:
        await producer.stop()
