import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Gantt Chart Collapsible", layout="wide")

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQP_ACzeqBAEhJXAaO3j3nndMKVJ3QTKEFqWKt1cc2bQggHySKcoOqvZGmwMu8IamCmk6CjsHTHsv8t/pub?gid=498246392&single=true&output=csv"
df = pd.read_csv(sheet_url)

# Konversi tanggal
df['Start Date'] = pd.to_datetime(df['Start Date'], dayfirst=True, errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], dayfirst=True, errors='coerce')
df['Percent Complete'] = df['Percent Complete'].str.replace('%', '', regex=False).astype(float).fillna(0)

# Buat list rows untuk Google Chart
rows = []
for _, row in df.iterrows():
    if pd.isna(row['Start Date']) or pd.isna(row['End Date']):
        continue

    start = f"new Date({row['Start Date'].year}, {row['Start Date'].month - 1}, {row['Start Date'].day})"
    end = f"new Date({row['End Date'].year}, {row['End Date'].month - 1}, {row['End Date'].day})"
    percent = int(row['Percent Complete'])

    task_id = row['Task ID']
    task_name = f"{row['Nama klient']} / {row['layanan aplikasi']} / {row['Fitur Aplikasi']} / {row['Topik']}"
    resource = str(row['Topik Detail']).replace("'", "").replace("\n", " ") if pd.notna(row['Topik Detail']) else ""

    rows.append(f"['{task_id}', '{task_name}', '{resource}', {start}, {end}, null, {percent}, null]")

if not rows:
    st.error("Tidak ada data valid untuk ditampilkan di Gantt chart.")
else:
    row_data = ",\n".join(rows)

    # Optional untuk debug
    st.code(row_data, language='javascript')

    # Load HTML dan ganti placeholder
    with open("gantt.html", "r") as f:
        html_template = f.read()

    html_output = html_template.replace("JSONDATA", row_data)

    st.title("📊 Gantt Chart Proyek (Multi-Level Hirarki)")
    components.html(html_output, height=800, scrolling=True)
