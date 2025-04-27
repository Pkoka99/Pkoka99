import requests
import capsolver
import random
from colorama import Fore
import string
import threading
import time

r, g, w, y, b = Fore.RED, Fore.GREEN, Fore.WHITE, Fore.YELLOW, Fore.BLUE

capsolver.api_key = "CAP-6403F5BA09E14FFD50A2F6CAE746B3948EFE135957E4EFDC314D97F369B9624A"
loginn = False
url = "https://anypoint.mulesoft.com/login/signup"
site_api = "https://anypoint.mulesoft.com/accounts/api/signup"
site_api1 = "https://anypoint.mulesoft.com/accounts/login"
key = "6Le79gsUAAAAAGle4VM80JTRciqNwTYzPc9vbHdu"
urls = "https://anypoint.mulesoft.com/codebuilder/webide/api/v1/organizations/a25c3769-b42e-4154-95be-3a45883a174c/tac?type=1"
usnm = input("username : ")
def rndm(length=8):
    return ''.join(random.choices(string.digits, k=length))

def solv(skey, pgu):
    capt = capsolver.solve({
        "type": "ReCaptchaV2TaskProxyless",
        "websiteURL": pgu,
        "websiteKey": skey
    })

    return capt["gRecaptchaResponse"]
def sf(delay, ju):
    rn = ju
    print(f"\n[{y}INFO{w}] Solving CAPTCHA...\n")
    code = solv(key, url)

    if not code:
        print(f"[{r}FAILED{w}] Could not solve CAPTCHA.")
        return
    
    print(f"[{g}SUCCESS{w}] CAPTCHA Solved")

    data = {
        "firstName": "ga",
        "lastName": "cor",
        "email": "gf@exne.com",
        "title": "ff",
        "country": "AL",
        "organizationName": "Poka1337",
        "numberOfEmployees": "10001",
        "username": f"{usnm}{rn}",
        "password": "Poka1234",
        "confirmPassword": "Poka1234",
        "captchaCode": code,
        "termsAccepted": True
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
    }

    print(f"\n[{y}INFO{w}] Submitting form...")
    response = requests.post(site_api, json=data, headers=headers)
    if 'createdAt' in response.json():
      orgid = response.json().get('organizationId')
      print(f"\n[{g}SUCCESS{w}] Create Account {usnm}{rn}:Poka1234")
      with open("acc.txt", "a") as file:
          file.write(f"{usnm}{rn}:Poka1234\n")
      log(code, orgid, rn)
    else:
      print(f"[{r}FAILED{w}] Create Account")
    time.sleep(delay)
      
def log(dd, an, usn):
      print(f"\n[{y}INFO{w}] Trying To Login\n")
      data1 = {
        "firstName": "ga",
        "lastName": "cor",
        "email": "gf@exne.com",
        "title": "ff",
        "country": "AL",
        "organizationName": "Poka1337",
        "numberOfEmployees": "10001",
        "username": f"{usnm}{usn}",
        "password": "Poka1234",
        "captchaCode": dd,
        "termsAccepted": True
      }

      headers1 = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"
      }

      response1 = requests.post(site_api1, json=data1, headers=headers1)
      acc = response1.json().get('access_token')
      orgid = an
      if 'access_token' in response1.json():
         print(f"[{g}SUCCESS{w}] Login...")
         terms(orgid, acc)
      else:
         print(f"[{r}FAILED{w}] Login...")

def terms(orgi, auths):
    url = f"https://anypoint.mulesoft.com/codebuilder/webide/api/v1/organizations/{orgi}/tac?type=1"

    headers = {
    "Authorization": f"Bearer {auths}",
    "X-XSRF-TOKEN": "AnsaFpsi-f_JQGm95IbFNGWvU0PKjjB7m1VA",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://anypoint.mulesoft.com/codebuilder/",
    "Accept": "application/json, text/plain, */*",
    }

    cookies = {
    "mulesoft.sess.sig": "QxFI7LWGw0mYn_nW0jA4rc7wWBA",
    "mulesoft.sess": "eyJpZCI6Il95RnNXODdlOGhzTC0ydlFPdFJiN0dNQWZvM2VGamFDIn0=",
    "XSRF-TOKEN": "AnsaFpsi-f_JQGm95IbFNGWvU0PKjjB7m1VA",
    }

    data = "null"

    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    if 'canAcceptTac' in response.json():
       print(f"[{g}SUCCESS{w}] Verify...\n")
    else:
       print(f"[{r}FAILED{w}] Verify Terms")

def main():
    jumlah = int(input("Jumlah akun yang ingin dibuat: "))
    threads = int(input("Jumlah threads: "))
    delay = float(input("Delay antara akun (detik): "))
    thread_list = []
    for _ in range(jumlah):
        t = threading.Thread(target=sf, args=(delay, _))
        thread_list.append(t)
        t.start()

        if len(thread_list) >= threads:
            for thread in thread_list:
                thread.join()
            thread_list = []

    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    main()
    