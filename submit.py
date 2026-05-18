"""
submit.py — Selenium form-fill automation
Opens the demo form, fills name/email/phone, submits, saves a screenshot.
Uses Selenium 4.6+ built-in Selenium Manager (no webdriver-manager needed).
"""

import os
import time
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ── Config ────────────────────────────────────────────────────────────────────
# Change this to your demo form URL.
# If running locally served via http.server:  "http://localhost:8080/demo_form.html"
# If exposed via ngrok: "https://xxxx.ngrok-free.app/demo_form.html"
DEMO_FORM_URL   = "http://localhost:8080/demo_form.html"
SCREENSHOTS_DIR = "screenshots"

log = logging.getLogger(__name__)


def _build_driver() -> webdriver.Chrome:
    """
    Build a headless Chrome WebDriver using Selenium Manager (built into Selenium 4.6+).
    No webdriver-manager or manual ChromeDriver install needed.
    """
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    opts.add_argument("--log-level=3")  # suppress Chrome noise

    # Selenium Manager handles ChromeDriver automatically
    return webdriver.Chrome(options=opts)


def run_selenium(name: str, email: str, phone: str, row_index) -> str:
    """
    Fill and submit the demo form.

    Returns:
        Path to the saved screenshot file.
    Raises:
        Exception on any Selenium or timeout error.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    driver = _build_driver()
    wait   = WebDriverWait(driver, 10)

    try:
        log.info("Opening demo form: %s", DEMO_FORM_URL)
        driver.get(DEMO_FORM_URL)

        # ── Fill fields ───────────────────────────────────────────────────────
        wait.until(EC.presence_of_element_located((By.ID, "name")))

        driver.find_element(By.ID, "name").clear()
        driver.find_element(By.ID, "name").send_keys(name)

        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(email)

        driver.find_element(By.ID, "phone").clear()
        driver.find_element(By.ID, "phone").send_keys(phone)

        log.info("Fields filled — name=%s  email=%s  phone=%s", name, email, phone)

        # ── Submit ────────────────────────────────────────────────────────────
        driver.find_element(By.ID, "submit-btn").click()

        # Wait for the success message to appear
        wait.until(EC.visibility_of_element_located((By.ID, "result")))
        log.info("Form submitted successfully.")

        time.sleep(0.5)  # let success state render fully

        # ── Screenshot ────────────────────────────────────────────────────────
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"row_{row_index}_{timestamp}.png"
        filepath  = os.path.join(SCREENSHOTS_DIR, filename)
        driver.save_screenshot(filepath)
        log.info("Screenshot saved: %s", filepath)

        return filepath

    finally:
        driver.quit()