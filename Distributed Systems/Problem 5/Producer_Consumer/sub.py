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
        self.queue_name = ""
        self.queue_size = 0

    def create_common_queue(self, queue_name):
        self.queue_name = queue_name
        qs = self.channel.queue_declare(queue=queue_name)
        self.queue_size = qs.method.message_count

    def create_persistant_queue(self, queue_name):
        self.queue_name = queue_name
        qs = self.channel.queue_declare(queue=queue_name, durable=True)
        self.queue_size = qs.method.message_count

    def create_ttl_queue(self, queue_name, ttl):
        self.queue_name = queue_name
        qs = self.channel.queue_declare(queue=queue_name, arguments={
                                        'x-message-ttl': ttl * 1000})
        self.queue_size = qs.method.message_count

    def create_bound_queue(self, queue_name):
        self.queue_name = queue_name
        qs = self.channel.queue_declare(
            queue_name, arguments={"x-max-length": 10})
        self.queue_size = size

    def start_dummy_listener(self, queue_name):
        print('   Waiting for messages. To exit press CTRL+C   ')

        def callback(ch, method, properties, body):
            msg_unpack = json.loads(body)
            print('{0} : {1}'.format(
                msg_unpack['user_name'], msg_unpack['message']))
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            # ch.basic_reject(delivery_tag=method.delivery_tag)
            # ch.basic_nack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(callback, queue=queue_name, no_ack=False)
        self.channel.start_consuming()

    def start_distribute_task(self):
        print('   Waiting for task. To exit press CTRL+C   ')

        def callback(ch, method, properties, body):
            msg_unpack = json.loads(body)

            print("Received task " +
                  msg_unpack['message'] + " from " + msg_unpack['user_name'])
            time.sleep(5)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # ch.basic_reject(delivery_tag=method.delivery_tag)
            # ch.basic_nack(delivery_tag=method.delivery_tag)
            print("Done")

        #self.channel.basic_qos(prefetch_count=1, prefetch_size=0)
        self.channel.basic_consume(
            callback, queue=self.queue_name, no_ack=False)
        self.channel.start_consuming()

    def get_message(self, queue_name, count, ttl=60):

        queue_type = queue_name.replace("queue_", "")
        if queue_type == "common":
            self.create_common_queue(queue_name=queue_name)
        elif queue_type == "persistant":
            self.create_persistant_queue(queue_name=queue_name)
        elif queue_type == "ttl":
            self.create_ttl_queue(queue_name=queue_name, ttl=ttl)
        else:
            print("Error")
            return ""

        if self.queue_size == 0:
            print "Empty queue"
            return "Empty queue"
        elif count > self.queue_size:
            count = count % self.queue_size + 1
        else:
            pass

        for i in range(0, count):
            i = 0
            for body in self.channel.basic_get(queue=queue_name, no_ack=True):
                i += 1
                if(i == 3):
                    msg_unpack = json.loads(body)
                    print('{0} : {1}'.format(
                        msg_unpack['user_name'], msg_unpack['message']))
                    return(msg_unpack['message'])

    def msg_pack(self, message):
        msg_pack = '{0} "{1}" : "{2}", "{3}" : "{4}" {5} '.format("{ ", "user_name", "Misha",
                                                                  "message", msg + " changed", " }")
        return msg_pack

    def modify_msg_and_send_response(self, response_queue_name, msg):
        self.create_common_queue(response_queue_name)
        self.channel.basic_publish(
            exchange='', routing_key=response_queue_name, body=self.msg_pack(msg))


if __name__ == '__main__':
    consumer = Consumer()
    consumer.open_channel()

    msg = consumer.get_message(queue_name="queue_common", count=1)
    consumer.modify_msg_and_send_response("queue_common_response", msg)

    # consumer.create_common_queue("queue_common")
    # consumer.create_common_queue("queue_common_response")
    # consumer.create_persistant_queue("queue_persistant")
    #consumer.create_ttl_queue("queue_ttl", 5)

    # consumer.start_dummy_listener("queue_common_response")
    # consumer.start_distribute_task()
