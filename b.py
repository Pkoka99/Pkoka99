from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs, unquote
import time
import undetected_chromedriver as uc
import threading
import os

login_url = "https://anypoint.mulesoft.com/login/"
with open("acc.txt", "r") as file:
    accounts = [line.strip().split(":") for line in file.readlines()]

def open_browser(instance_number, email, password):
    options = uc.ChromeOptions()
    
    # Keep all original arguments
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=3")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-networking")
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--mute-audio")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=800,600")
    
    # Additional stealth settings for Chrome 136
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-site-isolation-trials")
    
    driver = uc.Chrome(
        options=options,
        version_main=136,  # Matches your Chrome 136.0.7103.114
        headless=True,
        use_subprocess=True  # Better for multi-instance stability
    )

    # Enhanced stealth injection for Chrome 136
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}, app: {isInstalled: false}};
        """
    })

    driver.get(login_url)
    print(f"[{email}] OPEN CHROME")
    wait = WebDriverWait(driver, 30)

    try:
        username_field = wait.until(EC.presence_of_element_located((By.ID, "nameInput")))
        password_field = driver.find_element(By.ID, "passwordInput")
        username_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        print(f"[{email}] ✅ Login submitted.")
    except Exception as e:
        print(f"[{email}] ❌ Login fields not found: {e}")
    
    time.sleep(2)
    
    if "codebuilder" not in driver.current_url:
        driver.get("https://anypoint.mulesoft.com/codebuilder/")

    try:
        launch_button = wait.until(EC.element_to_be_clickable((By.ID, "launch-your-webide-btn-card")))
        launch_button.click()
        print(f"[{email}] ✅ Clicked Launch button")
    except:
        print(f"[{email}] ❌ Launch button not found")
        
    original_window = driver.current_window_handle

    WebDriverWait(driver, 30).until(EC.number_of_windows
