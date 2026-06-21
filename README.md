# API-Nira-FOA

Backend API untuk sistem monitoring **Nira Enau berbasis IoT** yang melakukan pemantauan level nira secara real-time, prediksi waktu panen, monitoring baterai, integrasi dashboard Blynk, dan notifikasi Telegram.

---

## 📌 Deskripsi

API-Nira-FOA adalah layanan backend berbasis Flask yang menerima data sensor dari perangkat IoT (seperti ESP32), memproses data level nira, menghitung estimasi waktu hingga wadah penuh menggunakan logika prediksi (ANFIS placeholder), memonitor kapasitas baterai, serta mengirimkan data ke Blynk dan Telegram.

Sistem ini dirancang untuk membantu proses pemantauan nira enau secara otomatis sehingga petani dapat mengetahui:

* Persentase isi nira saat ini
* Estimasi waktu hingga penuh
* Status baterai perangkat
* Kekuatan sinyal jaringan (RSSI)
* Notifikasi otomatis saat nira hampir penuh / penuh

---

## 🚀 Features

* Real-time monitoring level nira
* Prediksi waktu hingga wadah penuh
* Battery capacity estimation
* Integrasi Blynk Dashboard
* Notifikasi Telegram otomatis
* REST API berbasis Flask
* Mendukung integrasi IoT (ESP32 / sensor)

---

## 🛠 Tech Stack

* Python 3.x
* Flask
* Requests
* Blynk Cloud API
* Telegram Bot API

---

## 📂 Struktur Project

```bash
api-nira-foa/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/username/api-nira-foa.git
cd api-nira-foa
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running Project

Jalankan server:

```bash
python app.py
```

Server akan berjalan pada:

```bash
http://localhost:5000
```

---

## 📡 API Endpoint

### Home

```http
GET /
```

Response:

```json
Server Nira Enau Aktif!
```

---

### Receive Sensor Data

```http
POST /api/nira
```

Body JSON:

```json
{
  "nira_persen": 55.5,
  "uptime_jam": 12,
  "rssi": -65
}
```

Response:

```json
{
  "status": "success",
  "sisa_waktu": 3.2
}
```

---

## 📊 Monitoring Parameters

Parameter yang diproses:

* `nira_persen` → Persentase isi nira
* `uptime_jam` → Lama perangkat aktif
* `rssi` → Kekuatan sinyal WiFi

Output monitoring:

* Level Nira (%)
* Estimasi Waktu Penuh
* Sisa Baterai (%)
* Status Koneksi

---

## 🔔 Notification System

Telegram notifikasi akan dikirim ketika:

* Nira mencapai 50%
* Nira mencapai 80%
* Nira mencapai 100% (Penuh)

Contoh notifikasi:

```text
Nira mencapai 50%. Prediksi penuh sekitar 4.5 jam lagi.
```

---

## 📈 Future Development

* Implementasi model ANFIS penuh
* Dashboard monitoring web
* Database logging
* Data analytics
* Machine learning prediction enhancement

---

## 👨‍💻 Author

Developed for IoT-based Nira Enau Monitoring System Project.
