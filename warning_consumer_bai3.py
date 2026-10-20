import os
import pika

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "iot_alert_exchange"
QUEUE = "warning_queue"
ROUTING_KEY = "warning"

conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
ch = conn.channel()
ch.exchange_declare(exchange=EXCHANGE, exchange_type="direct")
ch.queue_declare(queue=QUEUE)
ch.queue_bind(queue=QUEUE, exchange=EXCHANGE, routing_key=ROUTING_KEY)


def on_message(ch, method, properties, body):
    print(f"[{QUEUE}] Da nhan: {body.decode()}")


ch.basic_consume(queue=QUEUE, on_message_callback=on_message, auto_ack=True)
print(f"[{QUEUE}] Dang cho canh bao muc '{ROUTING_KEY}'. Nhan Ctrl+C de dung.")
try:
    ch.start_consuming()
except KeyboardInterrupt:
    ch.stop_consuming()
conn.close()
