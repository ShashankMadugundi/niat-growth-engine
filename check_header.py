from services.google_sheets import get_google_client
from config import GOOGLE_SHEET_ID

client = get_google_client()
spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)
worksheet = spreadsheet.worksheet("Leads")

headers = worksheet.row_values(1)

for i, header in enumerate(headers, start=1):
    print(f"Column {i}: {repr(header)}")

print("Total columns:", len(headers))