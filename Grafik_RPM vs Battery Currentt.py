import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
df_rpm = pd.read_excel('HASIL TEST DRIVE WULING AIR EV.xlsx', sheet_name='MOTOR RPMM ESTIMASI')
df_arus = pd.read_excel('HASIL TEST DRIVE WULING AIR EV.xlsx', sheet_name='BATTERY CURRENT ARUS ESTIMASI')

# Standarisasi Timestamp
df_rpm['Timestamp'] = pd.to_datetime(df_rpm['Timestamp'], format='%H:%M:%S').dt.time
df_arus['Timestamp'] = pd.to_datetime(df_arus['Timestamp'], format='%H:%M:%S').dt.time

# 2. Filter Waktu (15:03:01 - 15:03:10)
t_start = pd.to_datetime('15:03:01', format='%H:%M:%S').time()
t_end = pd.to_datetime('15:03:10', format='%H:%M:%S').time()

df_r = df_rpm[(df_rpm['Timestamp'] >= t_start) & (df_rpm['Timestamp'] <= t_end)].copy().sort_values('Timestamp')
df_a = df_arus[(df_arus['Timestamp'] >= t_start) & (df_arus['Timestamp'] <= t_end)].copy().sort_values('Timestamp')

# Sinkronisasi
df_sync = pd.merge(df_r, df_a, on='Timestamp', how='inner')

# 3. PEMBERSIHAN DATA
col_rpm = 'ESTIMASI RPM MOTOR'
col_arus = 'Hasil Konversi Current Arus (Ampere)'

df_sync[col_arus] = pd.to_numeric(df_sync[col_arus].astype(str).str.replace(' A', ''), errors='coerce')
df_sync[col_rpm] = pd.to_numeric(df_sync[col_rpm], errors='coerce')
df_sync = df_sync.fillna(0)

# 4. Grafik Dual Axis: RPM vs Battery Current
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot RPM (Sumbu Kiri - Biru)
color1 = 'tab:blue'
ax1.set_xlabel('Waktu (HH:MM:SS)')
ax1.set_ylabel('Motor RPM', color=color1, fontsize=12, fontweight='bold')
ax1.plot(df_sync['Timestamp'].astype(str), df_sync[col_rpm], color=color1, marker='o', linewidth=2, label='RPM')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, linestyle='--', alpha=0.6)

# Plot Arus (Sumbu Kanan - Hijau)
ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('Battery Current (Ampere)', color=color2, fontsize=12, fontweight='bold')
ax2.plot(df_sync['Timestamp'].astype(str), df_sync[col_arus], color=color2, marker='D', linestyle='--', linewidth=2, label='Arus')
ax2.tick_params(axis='y', labelcolor=color2)

# 5. Anotasi Dinamis (Agar tidak bertumpuk)
for i, txt in enumerate(df_sync[col_rpm]):
    time_val = df_sync['Timestamp'].astype(str).iloc[i]
    ax1.annotate(f"{txt:.0f}", (time_val, df_sync[col_rpm].iloc[i]), 
                 textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color=color1, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

for i, txt in enumerate(df_sync[col_arus]):
    time_val = df_sync['Timestamp'].astype(str).iloc[i]
    ax2.annotate(f"{txt:.0f}A", (time_val, df_sync[col_arus].iloc[i]), 
                 textcoords="offset points", xytext=(0, -15), ha='center', fontsize=8, color=color2, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

plt.title('Korelasi Transien: RPM Motor vs Arus Baterai (15:03:01 - 15:03:10)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()