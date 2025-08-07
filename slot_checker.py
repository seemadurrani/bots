import time
import os
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

CONSULATES = ["Toronto", "Ottawa"]  # Add more if needed

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def setup_driver():
    options = Options()

    # Use headless for server; disable for local debugging
    # options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")

    # Add a realistic user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login(driver):
    try:
        driver.get("https://ais.usvisa-info.com/en-ca/niv/users/sign_in")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_email")))

        driver.find_element(By.ID, "user_email").send_keys(EMAIL)
        driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(5)

        print("✅ Logged in successfully")
        return True
    except Exception as e:
        print(f"❌ Login failed: {e}")
        send_telegram("❌ Visa bot failed to log in.")
        return False

def go_to_appointment_page(driver):
    try:
        # Replace 'YOUR_ID' with your actual ID after logging in manually once
        driver.get("https://ais.usvisa-info.com/en-ca/niv/schedule/YOUR_ID/appointment")
        time.sleep(5)
        return True
    except Exception as e:
        print(f"❌ Could not load appointment page: {e}")
        return False

def check_consulate(driver, name):
    try:
        select = Select(driver.find_element(By.ID, "appointments_consulate_appointment_facility_id"))
        select.select_by_visible_text(name)
        time.sleep(3)

        for _ in range(2):  # This month and next
            calendar = driver.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
            available = calendar.find_elements(By.CLASS_NAME, "ui-state-default")

            if available:
                msg = f"✅ Visa slot available in {name}! Go book now!"
                print(msg)
                send_telegram(msg)
                return True

            # Click next month
            driver.find_element(By.CLASS_NAME, "ui-datepicker-next").click()
            time.sleep(2)

        print(f"No slots at {name}")
        return False

    except Exception as e:
        print(f"❌ Error checking {name}: {e}")
        return False

# ---- Script Start ----
driver = setup_driver()

if not login(driver):
    driver.quit()
    exit(1)

if not go_to_appointment_page(driver):
    driver.quit()
    exit(1)

while True:
    print("🔍 Checking for slots...")
    session_expired = "sign_in" in driver.current_url

    if session_expired:
        print("🔁 Session expired. Re-logging in...")
        if not login(driver):
            break
        if not go_to_appointment_page(driver):
            break

    for consulate in CONSULATES:
        if check_consulate(driver, consulate):
            break

    print("⏳ Waiting 2 minutes...")
    time.sleep(120)
    try:
        driver.refresh()
        time.sleep(5)
    except WebDriverException as e:
        print(f"⚠️ Refresh failed: {e}")
        break

driver.quit()
