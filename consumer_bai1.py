import os
from datetime import datetime
import pika

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
QUEUE = "iot_lab_queue"

conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
ch = conn.channel()
ch.queue_declare(queue=QUEUE)


def on_message(ch, method, properties, body):
    print(f"Da nhan message: {body.decode()}")
    print(f"Thoi gian nhan: {datetime.now():%H:%M:%S}")


ch.basic_consume(queue=QUEUE, on_message_callback=on_message, auto_ack=True)
print(f"Dang lang nghe queue '{QUEUE}'. Nhan Ctrl+C de dung.")
try:
    ch.start_consuming()
except KeyboardInterrupt:
    ch.stop_consuming()
conn.close()
