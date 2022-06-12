# import third party modules
from aiokafka import AIOKafkaProducer

# import project related modules
from detective_catalog_service.settings import KAFKA_SERVER, loop
from detective_catalog_service.pydataobject.event_type import CrawlEvent


async def initialize_crawl(source_id: str):
    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=KAFKA_SERVER,
    )
    await producer.start()
    try:
        value_json = CrawlEvent(
            sourceId=source_id,
            queryType="crawl"
        ).json()
        await producer.send_and_wait(topic="query_execution", value=value_json)
    finally:
        await producer.stop()
