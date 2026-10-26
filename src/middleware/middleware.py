import pika

class MessageMiddlewareMessageError(Exception):
    pass


class MessageMiddlewareDisconnectedError(Exception):
    pass


class MessageMiddlewareCloseError(Exception):
    pass


class MessageMiddlewareDeleteError(Exception):
    pass


class MessageMiddlewareQueue():

    def __init__(self, host, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, heartbeat=0))
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_declare(queue=queue_name, durable=True)


    def start_consuming(self, on_message_callback):
        try:
            def callback(ch, method, _, body):
                on_message_callback(body, lambda: ch.basic_ack(delivery_tag=method.delivery_tag), lambda: ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True))

            self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=False)
            self.channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            raise MessageMiddlewareDisconnectedError(e)
        except Exception as e:
            raise MessageMiddlewareMessageError(e)


    def stop_consuming(self):
        try:
            self.channel.stop_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            raise MessageMiddlewareDisconnectedError(e)
        except Exception as e:
            raise MessageMiddlewareMessageError(e)


    def send(self, message):
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message, properties=pika.BasicProperties(delivery_mode=2))
        except pika.exceptions.AMQPConnectionError as e:
            raise MessageMiddlewareDisconnectedError(e)
        except Exception as e:
            raise MessageMiddlewareMessageError(e)


    def close(self):
        try:
            if self.channel != None:
                self.channel.close()
            if self.connection != None:
                self.connection.close()
        except Exception as e:
            raise MessageMiddlewareCloseError(e)


class MessageMiddlewareExchange():
    
    def __init__(self, host, exchange_name, routing_keys):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host, heartbeat=0))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

        self.connection = connection
        self.exchange_name = exchange_name
        self.routing_keys = routing_keys
        self.channel = channel


    def start_consuming(self, on_message_callback):
        try:
            queue = self.channel.queue_declare(queue='',exclusive=True, auto_delete=True)
            queue_name = queue.method.queue 
            for routing_key in self.routing_keys:
                self.channel.queue_bind(exchange=self.exchange_name, routing_key=routing_key, queue=queue_name)
            
            def callback(ch, method, _, body):
                on_message_callback(body, lambda: ch.basic_ack(delivery_tag=method.delivery_tag), lambda: ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True))
           
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
            self.channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            raise MessageMiddlewareDisconnectedError(e)
        except Exception as e:
            raise MessageMiddlewareMessageError(e)


    def stop_consuming(self):
        try:
            self.channel.stop_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            raise MessageMiddlewareDisconnectedError(e)
        except Exception as e:
            raise MessageMiddlewareMessageError(e)
    

    def send(self, message):
        try:
            for routing_key in self.routing_keys:
                self.channel.basic_publish(exchange=self.exchange_name, routing_key=routing_key, body=message)
        except pika.exceptions.AMQPConnectionError as e:
            raise MessageMiddlewareDisconnectedError(e)
        except Exception as e:
            raise MessageMiddlewareMessageError(e)


    def close(self):
        try:
            if self.channel != None:
                self.channel.close()
            if self.connection != None:
                self.connection.close()
        except Exception as e:
            raise MessageMiddlewareCloseError(e)