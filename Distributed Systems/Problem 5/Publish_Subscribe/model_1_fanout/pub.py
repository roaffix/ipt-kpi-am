import os
import sys

import pika


class Producer:

    def open_channel(self, host_url='localhost', user_name='user1', password='user1'):
        credentials = pika.PlainCredentials(user_name, password)
        parameters = pika.ConnectionParameters(
            host_url, 5672, '/', credentials)
        self.connection = pika. pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.exchange_name = ""

    def create_exchange(self, exchange_name):
        self.exchange_name = exchange_name
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type='fanout')

    def send_message(self, message):
        msg_pack = '{0} "{1}" : "{2}", "{3}" : "{4}" {5} '.format(
            "{ ", "user_name", "Andrii", "message", message, " }")
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key='', body=msg_pack)

    def start_producing(self):
        while True:
            #print("Input msg: ")
            msg = raw_input("Input msg: ")

            if(msg == "exit()"):
                self.close()
                break
            msg_pack = '{0} "{1}" : "{2}", "{3}" : "{4}" {5} '.format(
                "{ ", "user_name", "Andrii", "message", msg, " }")
            self.channel.basic_publish(
                exchange=self.exchange_name, routing_key='', body=msg_pack)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    producer = Producer()
    producer.open_channel()
    producer.create_exchange("chat")
    producer.start_producing()
    producer.close()
