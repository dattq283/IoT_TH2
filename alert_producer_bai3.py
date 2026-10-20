import os
import pika

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE = "iot_alert_exchange"
ALERTS = [
    ("info", "Nhiet do phong may on dinh info"),
    ("warning", "Nhiet do phong may vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical"),
]

conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
ch = conn.channel()
ch.exchange_declare(exchange=EXCHANGE, exchange_type="direct")

for level, msg in ALERTS:
    ch.basic_publish(exchange=EXCHANGE, routing_key=level, body=msg.encode())
    print(f"Da gui [{level}]: {msg}")

conn.close()
