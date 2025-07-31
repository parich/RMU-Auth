import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def check_internet(url="https://www.google.com"):
    try:
        requests.get(url, timeout=5)
        return True
    except requests.ConnectionError:
        return False

def login_gateway(username, password):
    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://gateway.rmu.ac.th:1003/login?03773caefb7d1541")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

while True:
    if not check_internet():
        print("No internet. Trying to login gateway...")
        login_gateway("parich", "XXX")
    else:
        print("Internet is available.")
    time.sleep(60)  #