import pandas as pd

# 1. Load Data Mentah Percobaan Kedua
file_name = 'SNIFFING_WULING_TOTAL2_144527.csv'
# Menggunakan sep=';' karena file kamu menggunakan titik koma
df = pd.read_csv(file_name, sep=';')

# Bersihkan spasi jika ada di nama kolom
df.columns = df.columns.str.strip()

# 2. Tambahkan kolom analisis Byte secara otomatis
# Memecah kolom 'Data_Raw' menjadi Byte_1 sampai Byte_8
split_data = df['Data_Raw'].astype(str).str.split(expand=True)
for i in range(8):
    df[f'Byte_{i+1}'] = split_data[i] if i in split_data.columns else '-'

# 3. Mapping ID yang sudah divalidasi
id_valid = {
    '0x155': 'Pedal Accelerator',
    '0x16E': 'Motor RPM',
    '0x16C': 'Current (Arus)',
    '0x1E5': 'Battery Voltage'
}
df['Keterangan_Komponen'] = df['CAN_ID'].astype(str).map(id_valid).fillna('Belum Teridentifikasi')

# 4. Urutkan berdasarkan Waktu dan ID agar rapi
df = df.sort_values(by=['Timestamp', 'CAN_ID'])

# 5. Ringkasan untuk Terminal
print(f"--- LAPORAN PERCOBAAN 2 ---")
print(f"Total Baris Data: {len(df)}")
print(f"Total ID Unik ditemukan: {df['CAN_ID'].nunique()}")
print(f"Daftar 10 ID pertama: {list(df['CAN_ID'].unique()[:10])}")

# 6. Simpan ke Excel (Seluruh 115 ID masuk sini)
output_name = 'REKAP_TOTAL_PERCOBAAN_DUA.xlsx'
df.to_excel(output_name, index=False)

print(f"\n✅ SELESAI, BOLO!")
print(f"File '{output_name}' sudah jadi dan berisi rekap seluruh ID.")