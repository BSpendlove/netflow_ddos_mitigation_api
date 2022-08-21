import time
import json
from os import environ

import pika
from loguru import logger
from pymongo import MongoClient

INTERESTING_FIELDS = ["ts", "te", "td", "sa", "da", "sp", "dp", "pr", "flg", "ipkt", "ibyt", "in", "out"]
FIELD_TYPES = {"sp": int, "dp": int, "fwd": int, "stos": int, "ipkt": int, "ibyt": int, "opkt": int, "in": int, "out": int}

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=environ["RABBITMQ_HOST"],
        credentials=pika.PlainCredentials(environ["RABBITMQ_USERNAME"], environ["RABBITMQ_PASSWORD"])
    ))

    channel = connection.channel()
    channel.exchange_declare(exchange=environ["RABBITMQ_EXCHANGE"], exchange_type="fanout")

    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=environ["RABBITMQ_EXCHANGE"], queue=queue_name)

    #client = MongoClient(environ["MONGODB_URL"])
    #db = client.netflow
    #collection = db.flows

    def callback(ch, method, properties, body):
        data = body.decode()
        data = json.loads(data)
        filtered_data = {}

        """
        for k in data.keys():
            if k not in INTERESTING_FIELDS:
                continue
            
            if k in FIELD_TYPES:
                filtered_data[k] = FIELD_TYPES[k](data[k])
            else:
               filtered_data[k] = data[k]

        collection.insert_one(filtered_data)
        """
        logger.info(data)

    channel.basic_consume(queue="", auto_ack=True, on_message_callback=callback)

    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as error:
            logger.error(error)

        logger.info("Waiting 10 seconds before attempting to connect to RabbitMQ again...")
        time.sleep(10)