import os
import pika

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
QUEUE = "iot_lab_queue"
HO_TEN = os.getenv("HO_TEN", "Trinh Quoc Dat")
MA_SV = os.getenv("MA_SV", "B23DCCN152")

conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
ch = conn.channel()
ch.queue_declare(queue=QUEUE)

so_luong = int(os.getenv("SO_MESSAGE", "1"))  # mo rong: gui nhieu message lien tiep
for i in range(1, so_luong + 1):
    msg = f"Xin chao tu ung dung Python AMQP - {MA_SV} - {HO_TEN}"
    if so_luong > 1:
        msg += f" (#{i})"
    ch.basic_publish(exchange="", routing_key=QUEUE, body=msg.encode())
    print(f"Da gui: {msg}")

conn.close()
