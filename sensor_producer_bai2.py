import json
import os
import random
import time
from datetime import datetime
import pika

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
QUEUE = "sensor_data_queue"
DEVICES = ["sensor01", "sensor02", "sensor03"]  # mo rong: mo phong 3 cam bien
INTERVAL = 3


def make_payload(device_id):
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(25, 40), 1),
        "humidity": round(random.uniform(30, 80), 1),
        "timestamp": datetime.now().isoformat(timespec="seconds"),  # mo rong: thoi gian gui
    }


conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
ch = conn.channel()
ch.queue_declare(queue=QUEUE)
print(f"Gui du lieu moi {INTERVAL} giay vao '{QUEUE}'. Nhan Ctrl+C de dung.")
try:
    while True:
        for device_id in DEVICES:
            body = json.dumps(make_payload(device_id))
            ch.basic_publish(exchange="", routing_key=QUEUE, body=body,
                             properties=pika.BasicProperties(content_type="application/json"))
            print(f"Da gui: {body}")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    pass
conn.close()
