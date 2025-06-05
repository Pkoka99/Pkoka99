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
    print("Navigating to webminer.pages.dev...")
    driver.get("https://webminer.pages.dev")
    
    # Wait for elements and interact
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "basic_worker")))
    
    print("Filling worker address...")
    driver.find_element(By.ID, "basic_worker").send_keys("RNZaqoBye9Kye6USMC55ve52pBxo168xMU")
    
    print("Setting worker count...")
    driver.find_element(By.ID, "basic_workers").clear()
    driver.find_element(By.ID, "basic_workers").send_keys("16")
    
    print("Submitting form...")
    driver.find_element(
        By.CSS_SELECTOR, 
        "button.css-17yhhjv.ant-btn.ant-btn-primary[type='submit']"
    ).click()
    
    print("Form submitted successfully in headless mode!")
    # Keep browser open due to detach option
    input("Press Enter to close the browser...")  # Remove this line for fully automated runs

except Exception as e:
    print(f"Error: {str(e)}")
    driver.save_screenshot('error_screenshot.png')  # Debug help
finally:
    # Optional: uncomment to auto-close when done
    # driver.quit()
    pass
