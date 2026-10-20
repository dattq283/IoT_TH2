import json
import os
import pika

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
QUEUE = "sensor_data_queue"


def analyze(data):
    lines = [
        f"Device: {data['device_id']}",
        f"Temperature: {data['temperature']}",
        f"Humidity: {data['humidity']}",
    ]
    if "timestamp" in data:
        lines.append(f"Sent at: {data['timestamp']}")
    if data["temperature"] > 35:
        lines.append("CANH BAO: Nhiet do cao")
    if data["humidity"] < 40:
        lines.append("CANH BAO: Do am thap")
    return lines


def on_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        print("\n".join(analyze(data)))
    except (ValueError, KeyError, TypeError) as e:
        print(f"Payload khong hop le ({e}): {body!r}")
    print("-" * 30)


if __name__ == "__main__":
    conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE)
    ch.basic_consume(queue=QUEUE, on_message_callback=on_message, auto_ack=True)
    print(f"Dang giam sat queue '{QUEUE}'. Nhan Ctrl+C de dung.")
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        ch.stop_consuming()
    conn.close()
