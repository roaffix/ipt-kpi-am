import os
import sys

import pika


class Producer:

    def open_channel(self, host_url='192.168.0.100', user_name='user1', password='user1'):
        credentials = pika.PlainCredentials(user_name, password)
        parameters = pika.ConnectionParameters(
            host_url, 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.queue_name = ""

    def create_common_queue(self, queue_name):
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name)

    def create_persistant_queue(self, queue_name):
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)

    def create_ttl_queue(self, queue_name, ttl):
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, arguments={
                                   'x-message-ttl': ttl * 1000})

    def create_bound_queue(self, queue_name):
        self.queue_name = queue_name
        self.channel.queue_declare(queue_name, arguments={"x-max-length": 10})

    def send_message(self, message):
        msg_pack = '{0} "{1}" : "{2}", "{3}" : "{4}" {5} '.format(
            "{ ", "user_name", "Andrii", "message", message, " }")
        self.channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=msg_pack)

    def start_producing(self):
        while True:
            msg = raw_input("Input msg: ")
            if(msg == "exit()"):
                self.close()
                break
            msg_pack = '{0} "{1}" : "{2}", "{3}" : "{4}" {5} '.format(
                "{ ", "user_name", "Andrii", "message", msg, " }")
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=msg_pack,
                                       properties=pika.BasicProperties(delivery_mode=2))

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    producer = Producer()
    producer.open_channel()
    producer.create_common_queue("queue_common")
    # producer.create_persistant_queue("queue_persistant")
    # producer.create_ttl_queue("queue_ttl", 15)
    producer.start_producing()
    producer.close()
