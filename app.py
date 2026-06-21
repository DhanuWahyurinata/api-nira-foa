from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# ========================================================
# KREDENSIAL BLYNK & TELEGRAM
# ========================================================
BLYNK_AUTH_TOKEN = "iQzz4E6ABVj5obYjRrIwz4wlWkmHGjfd"
TELEGRAM_BOT_TOKEN = "8875092454:AAFXOGlTXULXecrgOAPaKCaNVhJ3E-HXmZk"
TELEGRAM_CHAT_ID = "8178380257"

# Variabel Global
nira_lalu = 0
waktu_lalu = time.time()
sudah_notif_50 = False
sudah_notif_80 = False
sudah_notif_100 = False

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
        print(f"[TELEGRAM] Pesan terkirim: {pesan}")
    except Exception as e:
        print(f"[TELEGRAM] Gagal kirim: {e}")

def update_blynk(pin, value):
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        requests.get(url, timeout=5)
    except Exception as e:
        print(f"[BLYNK] Gagal update pin {pin}: {e}")

@app.route('/')
def home():
    return "Server Nira Enau Aktif!"

@app.route('/api/nira', methods=['POST'])
def terima_data():
    global nira_lalu, waktu_lalu
    global sudah_notif_50, sudah_notif_80, sudah_notif_100

    data = request.json
    if not data:
        return jsonify({"error": "Tidak ada data JSON"}), 400

    nira_persen = float(data.get('nira_persen', 0))
    uptime_jam = float(data.get('uptime_jam', 0))
    rssi = data.get('rssi', 0)

    # 1. LOGIKA ANFIS PLACEHOLDER
    waktu_sekarang = time.time()
    selisih_waktu_menit = (waktu_sekarang - waktu_lalu) / 60.0
    kecepatan_isi = 0

    if selisih_waktu_menit > 0.05:
        selisih_nira = nira_persen - nira_lalu
        if selisih_nira > 0:
            kecepatan_isi = selisih_nira / selisih_waktu_menit
        nira_lalu = nira_persen
        waktu_lalu = waktu_sekarang

    # Simulasi perhitungan cerdas (akan diganti model ANFIS nanti)
    sisa_jam_penuh = 99
    if kecepatan_isi > 0.005 and nira_persen < 100:
        sisa_kapasitas = 100.0 - nira_persen
        sisa_jam_penuh = (sisa_kapasitas / kecepatan_isi) / 60.0
    elif nira_persen >= 100:
        sisa_jam_penuh = 0

    # 2. LOGIKA BATERAI
    kapasitas_awal_mah = 12580.0
    konsumsi_arus_ma = 70.0
    mah_terpakai = uptime_jam * konsumsi_arus_ma
    sisa_kapasitas_mah = max(kapasitas_awal_mah - mah_terpakai, 0)
    sisa_baterai_persen = min((sisa_kapasitas_mah / kapasitas_awal_mah) * 100.0, 100.0)

    print(f"Data Masuk -> Nira: {nira_persen}% | Sisa Jam: {sisa_jam_penuh:.1f} | Baterai: {sisa_baterai_persen:.0f}%")

    # 3. UPDATE BLYNK
    update_blynk("v1", round(nira_persen, 1))
    update_blynk("v3", rssi)
    update_blynk("v4", round(sisa_baterai_persen, 1))

    if sisa_jam_penuh == 99:
        update_blynk("v2", "Stagnan")
    elif sisa_jam_penuh == 0:
        update_blynk("v2", "Penuh")
    else:
        update_blynk("v2", f"{sisa_jam_penuh:.1f} Jam Lagi")

    # 4. LOGIKA TELEGRAM
    if nira_persen < 10.0:
        sudah_notif_50 = sudah_notif_80 = sudah_notif_100 = False

    if 50.0 <= nira_persen < 80.0 and not sudah_notif_50:
        kirim_telegram(f"Nira mencapai *50%*. Prediksi penuh sekitar {sisa_jam_penuh:.1f} jam lagi.")
        sudah_notif_50 = True
    elif 80.0 <= nira_persen < 100.0 and not sudah_notif_80:
        kirim_telegram(f"Nira sudah *80%*! Bersiap panen. Estimasi penuh {sisa_jam_penuh:.1f} jam lagi.")
        sudah_notif_80 = True
    elif nira_persen >= 100.0 and not sudah_notif_100:
        kirim_telegram(f"*PENTING:* Nira sudah *100% (Penuh)*! Segera panen sekarang.")
        sudah_notif_100 = True

    return jsonify({"status": "success", "sisa_waktu": sisa_jam_penuh})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)