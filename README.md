# Wuling Air EV CAN Bus Sniffing & Data Analysis

Repositori ini berisi dokumentasi, kode program mikrokontroler, serta skrip analisis data Python untuk proyek penelitian yang berjudul **"Identifikasi Parameter Operasional pada Wuling Air EV Menggunakan CAN Bus Sniffing"**. 

Proyek ini mengembangkan sistem akuisisi data berbiaya rendah untuk merekam dan menganalisis komunikasi *Controller Area Network* (CAN) Bus secara pasif pada kendaraan listrik Wuling Air EV tanpa memerlukan basis data CAN (*DBC*) resmi dari pabrikan.

---

## 📂 Struktur Repositori

```text
├── arduino/
│   └── esp32_can_sniffer.ino          # Kode program ESP32 & MCP2515 untuk menangkap data CAN Bus (Listen-Only Mode)
├── python/
│   ├── test_running.py                # Skrip Python untuk uji coba dan perekaman data awal
│   ├── data_processing.py             # Skrip pemrosesan dan dekode data mentah (CSV) menggunakan Pandas
│   ├── plot_kecepatan.py              # Skrip visualisasi grafik hubungan Pedal Akselerator (APP) vs RPM Motor
│   ├── plot_baterai_suhu.py           # Skrip visualisasi grafik hubungan Pedal Akselerator (APP) vs Arus Baterai
│   └── plot_can_signals.py            # Skrip visualisasi grafik hubungan RPM Motor vs Arus Baterai
├── Paper-Reverse-Engineering-CAN-Wuling-EN.docx.docx  # Dokumen laporan lengkap (Bahasa Inggris)
├── Paper-Reverse-Engineering-CAN-Wuling-ID.docx.docx  # Dokumen laporan lengkap (Bahasa Indonesia)
└── README.md                          # Dokumentasi proyek

🛠️ Perangkat Keras yang Digunakan
Mikrokontroler ESP32 (DevKitC)  Modul Transceiver CAN MCP2515 (8MHz)
Konektor / Kabel OBD-II (Pin 6 untuk CAN High dan Pin 14 untuk CAN Low)
🚀 Cara Menjalankan Program1. Firmware Arduino (Pengumpulan Data)Buka file arduino/esp32_can_sniffer.ino menggunakan Arduino IDE.Pastikan pustaka yang diperlukan (mcp_can library) sudah terinstal.Atur kecepatan komunikasi CAN pada 500 kbps dengan kristal 8 MHz.Unggah (upload) program ke board ESP32.Hubungkan modul ke port OBD-II Wuling Air EV untuk mulai merekam data mentah ke format CSV.  2. Analisis & Visualisasi Data (Python)Pastikan pustaka Python berikut telah terinstal di komputer Anda (pandas dan matplotlib):pip install pandas matplotlib
Pemrosesan Data Mentah: Jalankan skrip Pandas untuk mendekode nilai heksadesimal ke parameter fisik (RPM Motor, Arus Baterai, dan Posisi Pedal Akselerator / APP):python python/data_processing.py
Membuat Grafik Analisis: Jalankan skrip visualisasi untuk menampilkan grafik hubungan antar parameter operasional: python python/plot_kecepatan.py
python python/plot_baterai_suhu.py
python python/plot_can_signals.py
📈 Hasil Utama PenelitianBerhasil merekam 115 ID CAN unik selama ~49 menit pengujian jalan dalam berbagai kondisi operasional.  Berhasil mendekode 3 parameter utama kendaraan tanpa dokumen pabrikan:  Posisi Pedal Akselerator (APP) pada ID CAN 0x17D (Byte 4 & 6)  RPM Motor pada ID CAN 0x16E (Byte 5 & 7)  Arus Baterai pada ID CAN 0x16C (Byte 5 & 6)[cite: 1]📄 Lisensi & KontributorProyek ini dikembangkan untuk keperluan akademik dan penelitian mandiri dalam bidang kendaraan listrik (Electric Vehicle)[cite: 1]. Silakan gunakan atau modifikasi dengan tetap mencantumkan sumber referensi yang sesuai.
Setelah ditempelkan (*paste*) semuanya ke kotak editor di GitHub, gulir layar ke bawah lalu klik tombol hijau **Commit changes...** untuk menyimpan.
