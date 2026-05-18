![Header](https://capsule-render.vercel.app/api?type=venom&color=4CAF50&height=280&section=header&text=n8n%20Automation%20Pipeline&fontSize=52&fontColor=fff&fontAlignY=42&desc=Webhook%20·%20Google%20Sheets%20·%20Selenium%20·%20Flask%20·%20ngrok&descAlignY=62&descSize=16&descColor=fff&animation=twinkling)

[![Made by Nevil Dhinoja](https://img.shields.io/badge/Made%20by-Nevil%20Dhinoja-2E7D32?style=for-the-badge)](https://github.com/Nevil-Dhinoja)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![n8n](https://img.shields.io/badge/n8n-Cloud-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-API-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)](https://sheets.google.com/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Cost](https://img.shields.io/badge/API%20Cost-%240%20%2F%20₹0-22C55E?style=for-the-badge)](https://ngrok.com)

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=3000&pause=1000&color=4CAF50&center=true&vCenter=true&width=800&lines=Cloud+webhook+form+%C2%B7+Auto+data+capture;Google+Sheets+%C2%B7+Live+status+tracking;Flask+receiver+%C2%B7+ngrok+tunnel;Headless+Selenium+%C2%B7+Form+fill+%C2%B7+Screenshot;pending+%E2%86%92+processing+%E2%86%92+done)](https://git.io/typing-svg)

---

## Architecture

```
[n8n Form Trigger]  ←  User submits name / email / phone via public form URL
         │
         ▼
[Google Sheets Node]  ──  Appends row  |  status = "pending"
         │
         ▼
[HTTP Request Node]  ──  POST {email, name, phone} → ngrok public URL
         │
         ▼
[Flask receiver.py]  ──  Finds pending row by email, marks "processing"
         │
         ▼
[Selenium submit.py]  ──  Opens demo_form.html, fills fields, submits, screenshots
         │
         ▼
[Google Sheets]  ──  Updates row  |  status = "done" / "failed"  |  log = screenshot path
```

---

## What Is This?

**n8n Automation Pipeline** is a hybrid cloud-local automation workflow that accepts structured input via an n8n public form, appends it to Google Sheets with a `pending` status, fires a webhook to a local Flask server via ngrok, and uses headless Selenium to automatically fill and submit a demo form — updating the sheet to `done` with a screenshot saved per row.

**The entire stack runs at $0.**

### Key Stats

| Metric | Value |
|--------|-------|
| Pipeline stages | 4 — Capture, Store, Trigger, Automate |
| Cloud tool | n8n Cloud (free tier) |
| Data store | Google Sheets via gspread + Service Account |
| Tunnel | ngrok free tier |
| Browser automation | Selenium 4.x with built-in Selenium Manager |
| Status lifecycle | pending → processing → done / failed |
| API Cost | $0 / ₹0 |

---

## How It Works

```
n8n FORM TRIGGER
  User opens public n8n form URL
  Submits name / email / phone
         |
         v
GOOGLE SHEETS NODE
  Appends new row to n8n_automation sheet
  Columns: name | email | phone | status=pending | log
         |
         v
HTTP REQUEST NODE
  POSTs {email, name, phone} to Flask via ngrok
  Triggers local processing
         |
         v
FLASK RECEIVER  (receiver.py)
  Validates incoming POST — checks email present
  Connects to Google Sheet via gspread + Service Account
  Finds matching row by email with status=pending
  Marks row → "processing"
  Calls Selenium routine
         |
         v
SELENIUM  (submit.py)
  Opens locally hosted demo_form.html (headless Chrome)
  Fills name / email / phone fields
  Clicks submit
  Waits for success message
  Saves screenshot to screenshots/
         |
         v
GOOGLE SHEETS UPDATE
  Row status → "done" or "failed"
  Log column → screenshot path or error message
```

---

## Pipeline Stages

| Stage | File | What it does |
|-------|------|--------------|
| Capture | n8n Form Trigger | Public HTML form — accepts name, email, phone |
| Store | n8n Google Sheets Node | Appends row with status=pending to `n8n_automation` sheet |
| Trigger | n8n HTTP Request Node | POSTs payload to local Flask server via ngrok tunnel |
| Receive | `receiver.py` | Flask server — validates POST, finds row, marks processing |
| Automate | `submit.py` | Headless Selenium — fills demo form, submits, screenshots |
| Update | `receiver.py` | Updates Google Sheet row to done/failed with log |

---

## Features

| Feature | Detail |
|---------|--------|
| Public form trigger | n8n Form Trigger exposes a real HTML form — no curl needed |
| Status lifecycle | Every row tracked: pending → processing → done / failed |
| Email-based row lookup | Finds the correct sheet row by email — no row index passing needed |
| Headless Chrome | Selenium runs invisibly in the background — no browser window |
| Auto ChromeDriver | Selenium Manager (built into Selenium 4.6+) auto-downloads correct driver |
| Screenshot per row | One PNG saved per processed row with timestamp in filename |
| Error handling | Failed Selenium runs update sheet to `failed` with error message in log |
| Health endpoint | Flask `/health` endpoint for quick sanity checks |

---

## Tech Stack

### Automation & Workflow
[![n8n](https://img.shields.io/badge/n8n-Cloud%20Free-EA4B71?style=for-the-badge)](https://n8n.io/)
[![ngrok](https://img.shields.io/badge/ngrok-Free%20Tier-1F1E37?style=for-the-badge)](https://ngrok.com/)

### Backend
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

### Browser Automation
[![Selenium](https://img.shields.io/badge/Selenium-4.21-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://selenium.dev/)

### Data Store
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-gspread-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)](https://sheets.google.com/)
[![Google Auth](https://img.shields.io/badge/Google%20Auth-Service%20Account-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://console.cloud.google.com/)

---

## Project Structure

```
n8n-assessment/
├── receiver.py           <-- Flask webhook server — validates, finds row, triggers Selenium
├── submit.py             <-- Selenium logic — fills demo form, submits, screenshots
├── demo_form.html        <-- Local demo form served via http.server (Selenium target)
├── My workflow.json      <-- n8n workflow export — import directly into n8n Cloud
├── requirements.txt      <-- Python dependencies
├── screenshots/          <-- Auto-created, one PNG per processed row
│   ├── row_3_20260519_010319.png
│   └── row_4_20260519_011106.png
└── README.md
```

> `credentials.json` (Google Service Account key) is gitignored — never commit it.

---

## Installation & Setup

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Runtime |
| Google Chrome | Latest | Selenium target browser |
| n8n Cloud account | Free tier | Workflow + form trigger |
| ngrok account | Free tier | Tunnel local Flask to public URL |
| Google Cloud project | Free | Sheets API + Drive API |

---

### Step 1 — Clone

```bash
git clone https://github.com/Nevil-Dhinoja/Selenium-Automation-Assessment.git
cd Selenium-Automation-Assessment
```

### Step 2 — Install

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3 — Google Sheets + Service Account

**Create the sheet**
- Go to [Google Sheets](https://sheets.google.com) → New spreadsheet
- Name it exactly: `n8n_automation`
- Add headers in Row 1:

| A | B | C | D | E |
|---|---|---|---|---|
| name | email | phone | status | log |

**Create a Service Account (free — no billing needed)**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. New project → Enable **Google Sheets API** + **Google Drive API**
3. IAM & Admin → Service Accounts → Create Service Account → name: `n8n-sa`
4. Keys tab → Add Key → Create new key → JSON → download
5. Rename file to `credentials.json` → place in project root

**Share the sheet**
- Copy `client_email` from `credentials.json`
- Google Sheets → Share → paste email → Editor → Share

### Step 4 — Serve the demo form

```bash
python -m http.server 8080
```

Verify at: `http://localhost:8080/demo_form.html`

### Step 5 — Start ngrok

```bash
ngrok config add-authtoken YOUR_NGROK_TOKEN
ngrok http 5000
```

Copy the `https://xxxx.ngrok-free.app` URL — paste it into n8n's HTTP Request node.

### Step 6 — Start Flask receiver

```bash
python receiver.py
```

Health check:
```bash
curl http://localhost:5000/health
# → {"status": "ok"}
```

### Step 7 — Import n8n workflow

- n8n Cloud dashboard → **Import from file** → select `My workflow.json`
- Update the HTTP Request node URL to your current ngrok URL
- Connect Google Sheets credentials (OAuth2 with your Google account)
- Toggle workflow → **Active**

### Step 8 — Run a test

```bash
curl -X POST https://YOUR-N8N-WEBHOOK-URL/webhook/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"Nevil Dhinoja","email":"nevil@test.com","phone":"9876543210"}'
```

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
| `SpreadsheetNotFound` | Sheet name must be exactly `n8n_automation`; share it with service account `client_email` |
| `[WinError 193]` ChromeDriver | Remove webdriver-manager; Selenium 4.6+ Selenium Manager handles ChromeDriver automatically |
| ngrok URL rejected by n8n | Use the full `https://` URL, not `http://` |
| `email is required` from Flask | Check n8n HTTP Request body — must include `email` field |
| Screenshot blank/white | Increase `time.sleep()` in `submit.py` before `save_screenshot()` |
| Free ngrok URL changed | Restart ngrok, copy new URL, update n8n HTTP Request node URL |

---

## Roadmap

- [x] n8n Form Trigger — public HTML form for data capture
- [x] Google Sheets append — row per submission with status=pending
- [x] ngrok tunnel — exposes local Flask to n8n cloud
- [x] Flask receiver — validates POST, finds row by email, marks processing
- [x] Selenium automation — headless Chrome, fills demo form, submits
- [x] Screenshot per row — saved to screenshots/ with timestamp
- [x] Status lifecycle — pending → processing → done / failed
- [x] Error handling — failed runs update sheet with error message
- [ ] PDF upload support in n8n form with OCR extraction
- [ ] Docker + docker-compose for one-command local setup
- [ ] Email notification on processing complete
- [ ] Retry logic for failed Selenium runs

---

## License

MIT — free to use, fork and build on.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nevil%20Dhinoja-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/nevil-dhinoja)
[![GitHub](https://img.shields.io/badge/GitHub-Nevil--Dhinoja-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nevil-Dhinoja)
[![Gmail](https://img.shields.io/badge/Email-nevil%40email.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:dhinoja.nevil@email.com)

If this project helped you or saved you time, a star on the repo goes a long way.
