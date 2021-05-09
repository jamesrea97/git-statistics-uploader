"""This module contains Kafka handling logic"""
import json
from kafka import KafkaProducer

async def publish(bootstrap_servers: str, topic: str, value: dict[str, str]):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    return producer.send(topic=topic, value=value)
