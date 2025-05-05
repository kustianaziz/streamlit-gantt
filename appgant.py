import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Load data dari Google Sheet CSV
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQP_ACzeqBAEhJXAaO3j3nndMKVJ3QTKEFqWKt1cc2bQggHySKcoOqvZGmwMu8IamCmk6CjsHTHsv8t/pub?output=csv&gid=498246392"
df = pd.read_csv(sheet_url)

# Format tanggal dan percent
df['Start Date'] = pd.to_datetime(df['Start Date'], dayfirst=True, errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], dayfirst=True, errors='coerce')
df['Percent Complete'] = df['Percent Complete'].str.replace('%', '').astype(float)
df = df.dropna(subset=['Start Date', 'End Date'])


# Format data ke JavaScript Gantt
rows = []
rows = []
for i, row in df.iterrows():
    try:
        start = row['Start Date']
        end = row['End Date']
        if pd.isna(start) or pd.isna(end):
            continue  # Lewati baris yang kosong

        rows.append([
            row['Task ID'],
            f"{row['Topik']} - {row['Topik Detail']}",
            row['Task Name'],
            f"new Date({start.year}, {start.month - 1}, {start.day})",
            f"new Date({end.year}, {end.month - 1}, {end.day})",
            'null',
            row['Percent Complete'],
            None
        ])
    except Exception as e:
        print(f"Error on row {i}: {e}")
        continue


# Ubah ke string JS
row_strings = [f"['{r[0]}', '{r[1]}', '{r[2]}', {r[3]}, {r[4]}, {r[5]}, {r[6]}, {r[7]}]" for r in rows]
json_data = "[" + ",\n".join(row_strings) + "]"

# Load HTML template
with open("gantt.html", "r") as f:
    html_template = f.read()

# Sisipkan data
html_filled = html_template.replace("JSONDATA", json_data)

# Tampilkan
st.set_page_config(layout="wide")
st.title("📌 Gantt Chart Bertingkat (Collapsible) - Google Gantt")
components.html(html_filled, height=700, scrolling=True)
