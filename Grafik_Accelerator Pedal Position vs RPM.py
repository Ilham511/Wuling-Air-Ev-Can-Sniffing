import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
df_pedal = pd.read_excel('HASIL TEST DRIVE WULING AIR EV.xlsx', sheet_name='PEDAL ASELERATOR ESTIMASI')
df_rpm = pd.read_excel('HASIL TEST DRIVE WULING AIR EV.xlsx', sheet_name='MOTOR RPMM ESTIMASI')

# Standarisasi Timestamp
df_pedal['Timestamp'] = pd.to_datetime(df_pedal['Timestamp'], format='%H:%M:%S').dt.time
df_rpm['Timestamp'] = pd.to_datetime(df_rpm['Timestamp'], format='%H:%M:%S').dt.time

# 2. Filter Waktu (15:03:01 - 15:03:10)
t_start = pd.to_datetime('15:03:01', format='%H:%M:%S').time()
t_end = pd.to_datetime('15:03:10', format='%H:%M:%S').time()

df_p = df_pedal[(df_pedal['Timestamp'] >= t_start) & (df_pedal['Timestamp'] <= t_end)].copy().sort_values('Timestamp')
df_r = df_rpm[(df_rpm['Timestamp'] >= t_start) & (df_rpm['Timestamp'] <= t_end)].copy().sort_values('Timestamp')

# Sinkronisasi
df_sync = pd.merge(df_p, df_r, on='Timestamp', how='inner')

# 3. Nama Kolom
col_rpm = 'ESTIMASI RPM MOTOR'
col_pedal = 'Pedal Value Acceleration (%)'

# 4. Grafik Dual Axis dengan Anotasi Angka
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot RPM (Sumbu Kiri)
color1 = 'tab:blue'
ax1.set_xlabel('Waktu (HH:MM:SS)')
ax1.set_ylabel('Motor RPM', color=color1, fontsize=12, fontweight='bold')
ax1.plot(df_sync['Timestamp'].astype(str), df_sync[col_rpm], color=color1, marker='o', linewidth=2, label='RPM')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.6)

# Plot Pedal (Sumbu Kanan)
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Pedal Akselerator (%)', color=color2, fontsize=12, fontweight='bold')
ax2.plot(df_sync['Timestamp'].astype(str), df_sync[col_pedal], color=color2, marker='s', linestyle='--', linewidth=2, label='Pedal (%)')
ax2.tick_params(axis='y', labelcolor=color2)

# --- FUNGSI ANOTASI ANGKA ---
# Anotasi RPM
for i, txt in enumerate(df_sync[col_rpm]):
    ax1.annotate(f"{txt:.0f}", (df_sync['Timestamp'].astype(str).iloc[i], df_sync[col_rpm].iloc[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color=color1, fontweight='bold')

# Anotasi Pedal
for i, txt in enumerate(df_sync[col_pedal]):
    ax2.annotate(f"{txt:.0f}%", (df_sync['Timestamp'].astype(str).iloc[i], df_sync[col_pedal].iloc[i]), 
                 textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color=color2, fontweight='bold')

plt.title('Analisis Transien: Pedal vs RPM (15:03:01 - 15:03:10)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.show()