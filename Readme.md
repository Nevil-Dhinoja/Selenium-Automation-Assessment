# n8n + Google Sheets + Selenium — End-to-End Automation Pipeline

A hybrid cloud-local automation workflow built for an interview assessment.  
Accepts form input via n8n, stores data in Google Sheets, and uses Selenium to automatically fill and submit a local demo form — with full status tracking and screenshot capture.

---

## Architecture

```
[n8n Form Trigger]  ←  User submits name / email / phone
        │
        ▼
[Google Sheets]  ──  Appends row with status = "pending"
        │
        ▼
[n8n HTTP Request]  ──  POST {email, name, phone} → ngrok public URL
        │
        ▼
[Flask receiver.py]  ──  Finds pending row, marks "processing"
        │
        ▼
[Selenium submit.py]  ──  Opens demo form, fills fields, submits, screenshots
        │
        ▼
[Google Sheets]  ──  Updates status to "done" / "failed" + log
```

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Cloud workflow | n8n Cloud (free tier) |
| Data store | Google Sheets + gspread |
| Tunnel | ngrok (free tier) |
| Local server | Python + Flask |
| Browser automation | Python + Selenium 4.x |
| ChromeDriver | Selenium Manager (built-in, auto) |

---

## Project Structure

```
n8n-assessment/
├── receiver.py          # Flask webhook server
├── submit.py            # Selenium automation logic
├── demo_form.html       # Local demo form (Selenium target)
├── requirements.txt     # Python dependencies
├── workflow_export.json # n8n workflow export
├── screenshots/         # Auto-created, one PNG per processed row
└── README.md
```

> `credentials.json` (Google Service Account key) is gitignored — never commit it.

---

## Setup Guide

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/n8n-assessment.git
cd n8n-assessment
```

### 2. Python environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Google Sheets + Service Account

#### 3a. Create the sheet
- Go to [Google Sheets](https://sheets.google.com) → New spreadsheet
- Name it exactly: `n8n_automation`
- Add these headers in Row 1:

| A | B | C | D | E |
|---|---|---|---|---|
| name | email | phone | status | log |

#### 3b. Create a Service Account (free, no billing needed)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts → Create Service Account**
5. Name it `n8n-sa` → Create → skip role → Done
6. Click the service account → **Keys → Add Key → Create new key → JSON**
7. Download and rename the file to `credentials.json`
8. Place it in the project root (it is gitignored)

#### 3c. Share the sheet
- Open `credentials.json`, copy the `client_email` value
- In Google Sheets → **Share** → paste the email → **Editor** access → Share

---

### 4. Serve the demo form

Open a terminal and run:

```bash
python -m http.server 8080
```

Verify at: `http://localhost:8080/demo_form.html`

---

### 5. Start ngrok

```bash
# Install: https://ngrok.com/download
ngrok config add-authtoken YOUR_NGROK_TOKEN
ngrok http 5000
```

Copy the `https://xxxx.ngrok-free.app` URL — you will use it in n8n.

> Free ngrok URLs change every session. Update the HTTP Request node URL in n8n when you restart ngrok.

---

### 6. Start Flask receiver

```bash
source venv/bin/activate
python receiver.py
```

Health check:
```bash
curl http://localhost:5000/health
# → {"status": "ok"}
```

---

### 7. n8n Workflow Setup

Import `workflow_export.json` into your n8n Cloud instance:
- n8n dashboard → **Import from file** → select `workflow_export.json`
- Open the **HTTP Request** node → update the URL to your current ngrok URL
- Connect Google Sheets credentials (OAuth2 with your Google account)
- Toggle workflow to **Active**

#### n8n workflow has 3 nodes:

**Node 1 — n8n Form Trigger**  
Exposes a public HTML form with fields: name, email, phone

**Node 2 — Google Sheets (Append Row)**  
Appends name / email / phone / status=pending to `n8n_automation` sheet

**Node 3 — HTTP Request**  
POSTs `{email, name, phone}` to your ngrok URL `/webhook`

---

### 8. Run a test

Option A — via n8n Form URL (copy from Form Trigger node):
```
https://yourworkspace.app.n8n.cloud/form/xxxxxx
```

Option B — via curl:
```bash
curl -X POST https://YOUR-N8N-WEBHOOK-URL/webhook/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"9876543210"}'
```

Expected result:
1. Google Sheet gets a new row with `status = pending`
2. Flask receives POST, marks row `processing`
3. Selenium opens `demo_form.html`, fills fields, submits
4. Screenshot saved to `screenshots/`
5. Google Sheet row updated to `status = done`

---

## 3 Terminals Required

| Terminal | Command | Purpose |
|----------|---------|---------|
| 1 | `python -m http.server 8080` | Serve demo form |
| 2 | `ngrok http 5000` | Expose Flask publicly |
| 3 | `python receiver.py` | Run Flask webhook server |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `SpreadsheetNotFound` | Sheet name must be exactly `n8n_automation`; share it with service account email |
| `[WinError 193]` ChromeDriver | Use Selenium 4.6+ without webdriver-manager; Selenium Manager handles it automatically |
| ngrok URL rejected by n8n | Use the full `https://` URL, not `http://` |
| `email is required` from Flask | Check n8n HTTP Request body — must include `email` field |
| Screenshot is blank | Increase `time.sleep()` in `submit.py` before `save_screenshot()` |

---

## Notes

- `credentials.json` is gitignored — set up your own using the steps above
- ChromeDriver is managed automatically by Selenium 4.6+ — no manual installation needed
- Free ngrok URL changes on every restart — update n8n HTTP Request node URL each session