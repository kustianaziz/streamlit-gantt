# appgant.py
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Load data from published Google Sheets (CSV format)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQP_ACzeqBAEhJXAaO3j3nndMKVJ3QTKEFqWKt1cc2bQggHySKcoOqvZGmwMu8IamCmk6CjsHTHsv8t/pub?gid=498246392&single=true&output=csv"
df = pd.read_csv(sheet_url)

# Fill NA to empty string to avoid errors
df = df.fillna("")

# Convert date
df['Start Date'] = pd.to_datetime(df['Start Date'], dayfirst=True)
df['End Date'] = pd.to_datetime(df['End Date'], dayfirst=True)

# Generate hierarchical task structure
rows = []

for idx, row in df.iterrows():
    client_id = f"client_{row['Task ID'].split('/')[0]}"
    app_id = f"{client_id}_app_{row['layanan aplikasi']}"
    feat_id = f"{app_id}_feat_{row['Fitur Aplikasi']}"
    task_id = row['Task ID']

    # Level 1 - Client
    if not any(r['id'] == client_id for r in rows):
        rows.append({"id": client_id, "name": row['Task Name'], "parent": None, "start": None, "end": None, "complete": 0})

    # Level 2 - Layanan Aplikasi
    if not any(r['id'] == app_id for r in rows):
        rows.append({"id": app_id, "name": row['layanan aplikasi'], "parent": client_id, "start": None, "end": None, "complete": 0})

    # Level 3 - Fitur Aplikasi
    if not any(r['id'] == feat_id for r in rows):
        rows.append({"id": feat_id, "name": row['Fitur Aplikasi'], "parent": app_id, "start": None, "end": None, "complete": 0})

    # Level 4 - Task Detail
    rows.append({
        "id": task_id,
        "name": f"{row['Topik']} - {row['Topik Detail']}",
        "parent": feat_id,
        "start": row['Start Date'].strftime('%Y-%m-%d'),
        "end": row['End Date'].strftime('%Y-%m-%d'),
        "complete": int(str(row['Percent Complete']).replace('%', '').strip())
    })

# Pass data into HTML via JavaScript
components.html(
    open("gantt.html").read().replace("__DATA__", str(rows)),
    height=600,
    scrolling=True
)
