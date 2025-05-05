import streamlit as st
import pandas as pd
import plotly.express as px

# Ambil data dari Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1ffoAyT1JdsurIuSrFX_AF1m4J9qXeGZwDLKlD8TBMd4/gviz/tq?tqx=out:csv&gid=779105144"
df = pd.read_csv(sheet_url)

# Bersihkan nama kolom
df.columns = df.columns.str.strip()

# Debug kolom
st.write("Kolom yang tersedia:", df.columns.tolist())

# Ubah tanggal ke datetime
df['Mulai'] = pd.to_datetime(df['Dibuka pada'])
df['Selesai'] = pd.to_datetime(df['Tenggat Waktu'])

# Buat kolom hierarki
df['Task'] = df['Nama Klien'] + ' / ' + df['Layanan Aplikasi'] + ' / ' + df['Fitur Aplikasi']

# Filter Sidebar
client_filter = st.sidebar.multiselect("Filter Client", df['Nama Klien'].unique(), default=df['Nama Klien'].unique())
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['Mulai'].min(), df['Selesai'].max()])

# Filter data
filtered_df = df[
    (df['Nama Klien'].isin(client_filter)) &
    (df['Mulai'] >= pd.to_datetime(date_range[0])) &
    (df['Selesai'] <= pd.to_datetime(date_range[1]))
]

# Gantt Chart
fig = px.timeline(
    filtered_df,
    x_start="Mulai",
    x_end="Selesai",
    y="Task",
    color="Client",
    title="Gantt Chart Bertingkat dari Google Sheets",
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)
