import serial
import time
import csv
import os
from datetime import datetime

# --- KONFIGURASI ---
PORT_COM = 'COM5' 
BAUD_RATE = 115200
# Nama file otomatis pakai jam agar tidak menimpa data lama
NAMA_FILE_LOG = f"SNIFFING_WULING_TOTAL_{datetime.now().strftime('%H%M%S')}.csv"

print(f"--- MEMULAI SNIFFING SEMUA ID (115+ ID) ---")
print(f"File Output: {NAMA_FILE_LOG}")
print(f"Menunggu data dari mobil...\n")

try:
    ser = serial.Serial(PORT_COM, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    ser.flushInput()

    # Tulis header CSV di awal
    with open(NAMA_FILE_LOG, mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Timestamp', 'CAN_ID', 'Data_Raw'])

    while True:
        if ser.in_waiting > 0:
            try:
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Format sesuai Arduino kamu: ID:0x... , ...
                if "ID:" in raw_line and "," in raw_line:
                    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    
                    # Ambil bagian ID dan Data
                    data_part = raw_line.split("ID:")[1] 
                    isi = data_part.split(",")
                    
                    if len(isi) >= 2:
                        can_id = isi[0].strip()
                        raw_data = isi[1].strip()
                        
                        # 1. TAMPILKAN LANGSUNG (Mengalir Deras)
                        print(f"[{ts}] ID: {can_id} | DATA: {raw_data}")

                        # 2. SIMPAN KE CSV SECARA OTOMATIS
                        with open(NAMA_FILE_LOG, mode='a', newline='') as f:
                            writer = csv.writer(f, delimiter=';')
                            writer.writerow([ts, can_id, raw_data])
                            
            except Exception as e:
                # Jika ada baris error/aneh, tetap lanjut jangan berhenti
                continue

except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Pastikan Arduino IDE tertutup dan kabel USB kencang.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()