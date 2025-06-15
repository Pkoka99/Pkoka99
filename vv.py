from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

chrome_driver_path = "/usr/local/bin/chromedriver"

# Configure Chrome options for stealth
chrome_options = Options()
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-tools")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)

# Initialize WebDriver with service
service = Service(chrome_driver_path)# flag for Windows

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Execute CDP commands to hide automation
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = {
                runtime: {},
            };
        """
    })
    
    print("Starting mining operation...")
    
    # Random delays between actions
    def human_like_delay(min=1, max=3):
        time.sleep(random.uniform(min, max))
    
    # Navigate to URL with random query parameters
    base_url = "https://webminer.pages.dev?algorithm=cwm_minotaurx&host=minotaurx.na.mine.zpool.ca&port=7019&worker=RNZaqoBye9Kye6USMC55ve52pBxo168xMU&password=c%3DRVN&workers=32"
    driver.get(base_url)
    human_like_delay()

    # Wait for the hashrate element to be prese
    # Alternative element location strateg
    while True:
        hashrate = driver.find_element(By.CSS_SELECTOR, "span#hashrate strong").text
        print(f"{time.ctime()} - Hashrate: {hashrate}")
        time.sleep(5)  # Check every 5 seconds
        
except Exception as e:
    print(f"Critical error: {str(e)}")
    if 'driver' in locals():
        driver.quit()
