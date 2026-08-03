import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
df_pedal = pd.read_excel('HASIL TEST DRIVE WULING AIR EV.xlsx', sheet_name='PEDAL ASELERATOR ESTIMASI')
df_arus = pd.read_excel('HASIL TEST DRIVE WULING AIR EV.xlsx', sheet_name='BATTERY CURRENT ARUS ESTIMASI')

# Standarisasi Timestamp
df_pedal['Timestamp'] = pd.to_datetime(df_pedal['Timestamp'], format='%H:%M:%S').dt.time
df_arus['Timestamp'] = pd.to_datetime(df_arus['Timestamp'], format='%H:%M:%S').dt.time

# 2. Filter Waktu (15:03:01 - 15:03:10)
t_start = pd.to_datetime('15:03:01', format='%H:%M:%S').time()
t_end = pd.to_datetime('15:03:10', format='%H:%M:%S').time()

df_p = df_pedal[(df_pedal['Timestamp'] >= t_start) & (df_pedal['Timestamp'] <= t_end)].copy().sort_values('Timestamp')
df_a = df_arus[(df_arus['Timestamp'] >= t_start) & (df_arus['Timestamp'] <= t_end)].copy().sort_values('Timestamp')

# Sinkronisasi
df_sync = pd.merge(df_p, df_a, on='Timestamp', how='inner')

# PEMBERSIHAN DATA
col_pedal = 'Pedal Value Acceleration (%)'
col_arus = 'Hasil Konversi Current Arus (Ampere)'
df_sync[col_arus] = pd.to_numeric(df_sync[col_arus].astype(str).str.replace(' A', ''), errors='coerce')
df_sync[col_pedal] = pd.to_numeric(df_sync[col_pedal], errors='coerce')
df_sync = df_sync.fillna(0)

# 3. Grafik Dual Axis
fig, ax1 = plt.subplots(figsize=(14, 7))

color1 = 'tab:red'
ax1.set_xlabel('Waktu (HH:MM:SS)')
ax1.set_ylabel('Pedal Akselerator (%)', color=color1, fontsize=12, fontweight='bold')
ax1.plot(df_sync['Timestamp'].astype(str), df_sync[col_pedal], color=color1, marker='s', linewidth=2, label='Pedal (%)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('Battery Current (Ampere)', color=color2, fontsize=12, fontweight='bold')
ax2.plot(df_sync['Timestamp'].astype(str), df_sync[col_arus], color=color2, marker='o', linestyle='--', linewidth=2, label='Arus (A)')
ax2.tick_params(axis='y', labelcolor=color2)

# 4. Anotasi Rapi dengan bbox (Agar tidak tumpang tindih)
for i, txt in enumerate(df_sync[col_pedal]):
    ax1.annotate(f"{txt:.0f}%", 
                 (df_sync['Timestamp'].astype(str).iloc[i], df_sync[col_pedal].iloc[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color=color1, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.7))

for i, txt in enumerate(df_sync[col_arus]):
    ax2.annotate(f"{txt:.0f}A", 
                 (df_sync['Timestamp'].astype(str).iloc[i], df_sync[col_arus].iloc[i]), 
                 textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color=color2, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.7))

plt.title('Korelasi Transien: Pedal Akselerator vs Arus Baterai (15:03:01 - 15:03:10)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()