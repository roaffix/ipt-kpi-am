import json
import time

import pika


class Consumer:

    def open_channel(self, host_url='localhost', user_name='user1', password='user1'):
        credentials = pika.PlainCredentials(user_name, password)
        parameters = pika.ConnectionParameters(
            host_url, 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.exchange_name = ""
        self.queue_name = ""

    def create_listener_params(self, exchange_name):
        self.exchange_name = exchange_name
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue_name)

    def start_listener(self):
        print('   Waiting for logs. To exit press CTRL+C     ')

        def callback(ch, method, properties, body):
            msg_unpack = json.loads(body)
            print('{0} : {1}'.format(
                msg_unpack['user_name'], msg_unpack['message']))

        self.channel.basic_consume(
            callback, queue=self.queue_name, no_ack=True)
        self.channel.start_consuming()


if __name__ == '__main__':
    consumer = Consumer()
    consumer.open_channel()
    consumer.create_listener_params("chat")
    consumer.start_listener()
