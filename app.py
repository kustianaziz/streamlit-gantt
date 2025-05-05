import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Ambil data dari Google Sheets (pakai CSV export)
sheet_url = "https://docs.google.com/spreadsheets/d/1ffoAyT1JdsurIuSrFX_AF1m4J9qXeGZwDLKlD8TBMd4/gviz/tq?tqx=out:csv&gid=779105144"
df = pd.read_csv(sheet_url)

# 2. Pastikan kolom tanggal jadi datetime
df['Mulai'] = pd.to_datetime(df['Mulai'])
df['Selesai'] = pd.to_datetime(df['Selesai'])

# 3. Buat kolom gabungan hierarki
df['Task'] = df['Client'] + ' / ' + df['Topik'] + ' / ' + df['Tahapan']

# 4. Sidebar filter
client_filter = st.sidebar.multiselect("Filter Client", df['Client'].unique(), default=df['Client'].unique())
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['Mulai'].min(), df['Selesai'].max()])

# 5. Filter data
filtered_df = df[
    (df['Client'].isin(client_filter)) &
    (df['Mulai'] >= pd.to_datetime(date_range[0])) &
    (df['Selesai'] <= pd.to_datetime(date_range[1]))
]

# 6. Gantt Chart dengan Plotly
fig = px.timeline(
    filtered_df,
    x_start="Mulai",
    x_end="Selesai",
    y="Task",
    color="Client",
    title="Gantt Chart Bertingkat dari Google Sheets",
)

fig.update_yaxes(autorange="reversed")  # supaya task urut atas-bawah
st.plotly_chart(fig, use_container_width=True)
