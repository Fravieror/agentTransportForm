import pytesseract
from PIL import Image
import requests
import re
import io
import gspread
from google.oauth2.service_account import Credentials
import cv2
import numpy as np
from google.cloud import vision
import os
from datetime import datetime


# ==== CONFIGURATION ====
SERVICE_ACCOUNT_FILE = "credentials.json"  # Path to your JSON file
TARGET_SHEET_GASTOS = "https://docs.google.com/spreadsheets/d/1i8xKEi6wnsrabbFqTPbhGsGYwwc2T2vtE5vhCGWd9MQ/edit?gid=1423941865#gid=1423941865"               # First target spreadsheet
SOURCE_SHEET_CAJA_MENOR = "https://docs.google.com/spreadsheets/d/1BPUFYUqHoZ0eZnf7emUfY5dDgWN6j0_WFnJ1pi2AaKA/edit?gid=1247963443#gid=1247963443"               # Second target spreadsheet
IMAGE_COLUMN_INDEX = 3                        # Index of column with images (1-based)
PROCESSED_COLUMN_INDEX = 8                    # Where to mark rows as DONE (1-based)

# ==== AUTHENTICATE ====
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform"
]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# ==== LOAD SHEETS ====
source_sheet = client.open_by_url(SOURCE_SHEET_CAJA_MENOR).sheet1
target_gastos = client.open_by_url(TARGET_SHEET_GASTOS).sheet1

# ==== READ DATA ====
data = source_sheet.get_all_values()
print(data)
processed_rows = []

# ==== PROCESS ROWS ====
results_target1 = []
results_target2 = []

for i, row in enumerate(data[1:], start=2):  # Skip header row, start at row 2
    processed_flag = row[PROCESSED_COLUMN_INDEX] if len(row) >= PROCESSED_COLUMN_INDEX else ""
    print(f"Row {i} processed flag: '{processed_flag}'")

    # Skip if already processed
    if processed_flag.strip().upper() == "DONE":
        continue

    # Extract fields
    # Parse date string to datetime object
    date_str = row[0]
    email = row[1]
    concepto = row[2]
    
    if "CAJA" not in concepto.strip().upper():
        processed_rows.append(i)
        print(f"Row {i} skipped, concepto does not contain 'CAJA': '{concepto}'")
        continue
    
    comprobante = row[4]
    valor = row[5]
    # Ensure valor is positive before making it negative, and handle empty/invalid values
    try:
        valor_num = float(valor.replace(',', '').replace('$', ''))
        valor = -abs(valor_num)
    except Exception:
        valor = ""


    # Append data
    results_target1.append([date_str, '', 'GUX075', concepto, '', '', comprobante, email, valor])
    print(f"Gastos Row {i}: {[date_str, '', 'GUX075', concepto, '', '', comprobante, email, valor]}")
    # Mark row for update
    processed_rows.append(i)

# ==== WRITE DATA TO TARGET SHEETS ====
if results_target1:
     target_gastos.append_rows(results_target1)
# if results_target2:
#     target_caja_menor.append_rows(results_target2)

# ==== MARK ROWS AS PROCESSED ====
for row_index in processed_rows:
    source_sheet.update_cell(row_index, PROCESSED_COLUMN_INDEX + 1, "DONE")

print(f"Processed {len(processed_rows)} new rows.")
