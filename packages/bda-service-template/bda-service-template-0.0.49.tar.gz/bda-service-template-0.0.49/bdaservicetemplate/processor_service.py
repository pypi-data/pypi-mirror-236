from abc import abstractclassmethod
from .streaming_service import StreamingService
from bdaserviceutils import get_kafka_binder_brokers, get_input_channel, get_output_channel
from kafka import KafkaConsumer, KafkaProducer
from abc import ABC, abstractclassmethod
import json


class ProcessorService(ABC, StreamingService):

    alida_service_mode = "processor"
    
    def __init__(self, parser):
        super().__init__(parser)
        self.consumer = KafkaConsumer(get_input_channel(), bootstrap_servers=[get_kafka_binder_brokers()])
        self.producer = KafkaProducer(bootstrap_servers=[get_kafka_binder_brokers()])

    def run(self):
        for message in self.consumer:
            json_message = json.loads(message.value.decode('utf-8'))
            self.on_message(message=json_message)

    @abstractclassmethod
    def on_message(self, message):
        pass

    def send_message(self, message):
        self.producer.send(get_output_channel(), json.dumps(message).encode('utf-8'))
