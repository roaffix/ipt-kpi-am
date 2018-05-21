import os
import sys
import time

import pika


class Producer:

    def open_channel(self, host_url='localhost', user_name='user1', password='user1'):
        credentials = pika.PlainCredentials(user_name, password)
        parameters = pika.ConnectionParameters(
            host_url, 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.exchange_name = ""
        self.queue_name = ""

    def create_connection_params(self, exchange_name, queue_name):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type='fanout')
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def send_message(self, message):
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key='p1', body=message)
        print(" [x] Sent %r" % message)

    def start_producing(self):
        while True:
            #print("Input msg: ")
            msg = raw_input("Input msg: ")

            if(msg == "exit()"):
                break
            self.channel.basic_publish(
                exchange=self.exchange_name, routing_key='p1', body=msg)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    producer = Producer()
    producer.open_channel()
    producer.create_connection_params("chat", "p1")

    producer.send_message("hello1")
    producer.send_message("hello2")
    time.sleep(20)
    producer.send_message("hello3")
    producer.send_message("hello4")

    # producer.start_producing()
    # producer.close()
