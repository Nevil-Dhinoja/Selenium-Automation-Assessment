"""
receiver.py — Flask webhook server
Receives POST from n8n with email/name/phone,
finds the matching pending row in Google Sheets, runs Selenium, updates status.
"""

import logging
from flask import Flask, request, jsonify
from submit import run_selenium

import gspread
from google.oauth2.service_account import Credentials

# ── Config ────────────────────────────────────────────────────────────────────
GOOGLE_CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_NAME        = "n8n_automation"
WORKSHEET_INDEX         = 0

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)

app = Flask(__name__)


def get_sheet():
    creds  = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME).get_worksheet(WORKSHEET_INDEX)


def find_row_by_email(sheet, email: str):
    """
    Search all rows for a matching email with status = pending.
    Returns (row_index, row_data) — row_index is 1-based (header = row 1).
    Returns (None, None) if not found.
    """
    all_rows = sheet.get_all_values()
    for i, row in enumerate(all_rows[1:], start=2):  # skip header row
        if len(row) >= 4 and row[1].strip().lower() == email.strip().lower():
            if row[3].strip().lower() in ("pending", ""):
                return i, {
                    "name":   row[0],
                    "email":  row[1],
                    "phone":  row[2],
                    "status": row[3],
                }
    return None, None


def update_status(sheet, row_index: int, status: str, log_msg: str = ""):
    sheet.update_cell(row_index, 4, status)
    if log_msg:
        sheet.update_cell(row_index, 5, log_msg)


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True) or {}
    log.info("Incoming payload: %s", payload)

    email = payload.get("email", "").strip()
    name  = payload.get("name", "").strip()
    phone = payload.get("phone", "").strip()

    if not email:
        log.warning("Missing email in payload.")
        return jsonify({"error": "email is required"}), 400

    try:
        sheet = get_sheet()
        row_index, data = find_row_by_email(sheet, email)
    except Exception as exc:
        log.exception("Failed to connect to Google Sheet")
        return jsonify({"error": str(exc)}), 500

    if row_index is None or data is None:
        log.warning("No pending row found for email: %s — using payload data", email)
        row_index = 0
        data = {"name": name, "email": email, "phone": phone}
    else:
        log.info("Found row %d for email %s", row_index, email)
        update_status(sheet, row_index, "processing")

    try:
        screenshot_path = run_selenium(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            row_index=row_index,
        )
        if isinstance(row_index, int):
            update_status(sheet, row_index, "done", f"Screenshot: {screenshot_path}")
        log.info("Row %s → done. Screenshot: %s", row_index, screenshot_path)
        return jsonify({"status": "done", "screenshot": screenshot_path}), 200

    except Exception as exc:
        err_msg = str(exc)
        if isinstance(row_index, int):
            update_status(sheet, row_index, "failed", f"Error: {err_msg}")
        log.exception("Selenium failed for row %s", row_index)
        return jsonify({"status": "failed", "error": err_msg}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)