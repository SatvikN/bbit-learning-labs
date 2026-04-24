import pika
import json
from concurrent.futures import ThreadPoolExecutor
import time
import threading
from typing import Any
import os
from producer_interface import mqProducerInterface

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('codespaces-daa410',
                                            5672,
                                            '/',
                                            credentials)
        self.m_connection = pika.BlockingConnection(parameters=parameters)

        # Establish Channel
        self.m_channel = self.m_connection.channel()

        # Create the exchange if not already present
        self.m_channel.exchange_declare(self.exchange_name)

        pass

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        self.m_channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=json.dumps({"test": "test"}),
            properties=pika.BasicProperties(content_type='application/json')
        )

        # Close Channel
        self.m_channel.close()

        # Close Connection
        self.m_connection.close()
    
        pass
