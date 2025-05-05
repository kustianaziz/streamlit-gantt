import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Ambil data dari link publik Google Sheets (CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQP_ACzeqBAEhJXAaO3j3nndMKVJ3QTKEFqWKt1cc2bQggHySKcoOqvZGmwMu8IamCmk6CjsHTHsv8t/pub?output=csv&gid=498246392"
df = pd.read_csv(sheet_url)

# Transformasi data menjadi format yang dibutuhkan
df['Start Date'] = pd.to_datetime(df['Dibuka Pada'])
df['End Date'] = pd.to_datetime(df['Tenggat Waktu'])

# Kolom task dengan penggabungan nama hierarki
df['Task Name'] = df['Nama klient'] + ' / ' + df['layanan aplikasi'] + ' / ' + df['Fitur Aplikasi'] + ' / ' + df['Topik'] + ' / ' + df['Topik Detail']

# Generate Task ID untuk Google Gantt
df['Task ID'] = df.index + 1  # Simple Task ID
df['Resource'] = df['layanan aplikasi']  # Menyebutkan level layanan aplikasi sebagai resource

# Kolom Dependensi, jika ada, bisa ditambahkan berdasarkan kebutuhan
df['Dependencies'] = None  # Bisa ditambahkan jika ada hubungan antar task

# Streamlit layout
st.title("Gantt Chart Bertingkat")
st.sidebar.header("Filter Data")
client_filter = st.sidebar.multiselect("Filter Client", df['Nama klient'].unique(), default=df['Nama klient'].unique())
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df['Start Date'].min(), df['End Date'].max()])

# Filter data
filtered_df = df[
    (df['Nama klient'].isin(client_filter)) &
    (df['Start Date'] >= pd.to_datetime(date_range[0])) &
    (df['End Date'] <= pd.to_datetime(date_range[1]))
]

# Display Gantt Chart
fig = px.timeline(
    filtered_df,
    x_start="Start Date",
    x_end="End Date",
    y="Task Name",
    color="Resource",
    title="Gantt Chart Bertingkat"
)

fig.update_yaxes(autorange="reversed")  # Agar task urut atas-bawah
st.plotly_chart(fig, use_container_width=True)
