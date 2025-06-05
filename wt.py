

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_driver_path = "/usr/local/bin/chromedriver"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--enable-javascript")  # Enable JavaScript
chrome_options.add_argument("--headless=new")       # Headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")         # Bypass OS security
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_experimental_option("detach", True)  # Prevent auto-close

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

try:
    print("RUN MINER")
    driver.get("https://webminer.pages.dev?algorithm=cwm_minotaurx&host=minotaurx.na.mine.zpool.ca&port=7019&worker=RNZaqoBye9Kye6USMC55ve52pBxo168xMU&password=c%3DRVN&workers=96")
except Exception as e:
    print(f"Error: {str(e)}")
    driver.save_screenshot('error_screenshot.png')  # Debug help
finally:
    # Optional: uncomment to auto-close when done
    # driver.quit()
    pass
