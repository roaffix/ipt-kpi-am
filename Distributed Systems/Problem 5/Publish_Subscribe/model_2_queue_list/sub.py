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
        self.queue_size = ""
        self.queue_size = object

    def create_listener_params(self, queue_name, exchange_name):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type='fanout')
        self.qs = self.channel.queue_declare(queue=queue_name)
        self.queue_size = self.qs.method.message_count
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def get_last_message(self, count):
        for i in range(0, count):
            i = 0
            for body in self.channel.basic_get(queue="p1", no_ack=True):
                i += 1
                if(i == 3):
                    print(body)

    def start_listener(self):
        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r" % body)

        print("queue size : ", str(self.qs.method.message_count))
        for i in range(0, self.queue_size):
            i = 0
            for body in self.channel.basic_get(queue="p1", no_ack=True):
                i += 1
                if(i == 3):
                    print(body)
        time.sleep(20)
        print("queue size : ", str(self.qs.method.message_count))

        #self.channel.basic_consume(callback, queue=self.queue_name, no_ack=True)
        # for i in range(0,3):
       # for body in self.channel.basic_get(queue="p1", no_ack=False)

        # message = self.channel.consume(queue=self.queue_name) # basic_get(queue=self.queue_name) # start_consuming()
        # print(message)


if __name__ == '__main__':
    consumer = Consumer()
    consumer.open_channel()
    consumer.create_listener_params("p1", "chat")
    time.sleep(5)
    consumer.start_listener()
