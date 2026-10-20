# Thực hành: Lập trình Python với giao thức AMQP

## Broker sử dụng

- **RabbitMQ** 3.x chạy local (`localhost:5672`, tài khoản mặc định `guest/guest`).
- Thư viện Python: **pika** (`pip install -r requirements.txt`).
- Đổi broker (vd. broker dùng chung của lớp) bằng biến môi trường:
  `AMQP_URL=amqp://user:pass@host:5672/`

Chạy nhanh RabbitMQ bằng Docker (nếu chưa cài):

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Cách chạy

Mỗi consumer chạy liên tục, dừng bằng `Ctrl+C`. Mở consumer ở một terminal, producer ở terminal khác.

### Bài 1 – Producer → queue `iot_lab_queue` → Consumer

```bash
python consumer_bai1.py
HO_TEN="Trinh Quoc Dat" MA_SV="B23DCCN152" python producer_bai1.py
SO_MESSAGE=5 python producer_bai1.py   # mở rộng: gửi nhiều message liên tiếp
```

### Bài 2 – Cảm biến IoT gửi JSON vào `sensor_data_queue` mỗi 3 giây

```bash
python monitor_consumer_bai2.py
python sensor_producer_bai2.py
```

Payload: `{"device_id": "sensor01", "temperature": 29.5, "humidity": 62.1, "timestamp": "..."}`.
Mô phỏng 3 cảm biến `sensor01..03`, giá trị ngẫu nhiên (nhiệt độ 25–40, độ ẩm 30–80).
Consumer cảnh báo khi nhiệt độ > 35 hoặc độ ẩm < 40.

### Bài 3 – Direct exchange `iot_alert_exchange`

```bash
python warning_consumer_bai3.py    # queue warning_queue, routing key "warning"
python critical_consumer_bai3.py   # queue critical_queue, routing key "critical"
python alert_producer_bai3.py      # gửi 3 cảnh báo: info, warning, critical
```

Chạy consumer trước để queue được tạo và bind trước khi producer gửi.

## Kết quả đạt được

**Bài 1**
```
Da gui: Xin chao tu ung dung Python AMQP - B23DCCN152 - Trinh Quoc Dat
---
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN152 - Trinh Quoc Dat
Thoi gian nhan: 01:29:27
```

**Bài 2**
```
Device: sensor03
Temperature: 32.9
Humidity: 36.0
Sent at: 2026-10-13T01:29:30
CANH BAO: Do am thap
```

**Bài 3** – message `info` không consumer nào nhận; `warning` và `critical` đến đúng queue:
```
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

- [x] Kết nối được broker, gửi/nhận message qua queue
- [x] Payload JSON đúng định dạng, gửi tuần hoàn, phát hiện cảnh báo
- [x] Tạo exchange, bind queue đúng routing key, message phân phối đúng nơi nhận
