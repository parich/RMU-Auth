import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def check_internet(url="https://www.google.com"):
    try:
        requests.get(url, timeout=2)
        return True
    except requests.ConnectionError:
        return False

def checklist():
    while True:
        if not check_internet():
            print("No internet. Trying to login gateway...")
            time.sleep(10)
            continue
        else:
            print("Internet is available.")

            chrome_options = Options()
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

            service = Service('chromedriver.exe')
            driver = webdriver.Chrome(service=service, options=chrome_options)

            try:
                driver.get("https://plan.rmu.ac.th/survey/")
                print("Opened survey page.")

                # คลิก answerer2 และ department19
                driver.find_element(By.CSS_SELECTOR, 'label[for="answerer2"]').click()
                driver.find_element(By.CSS_SELECTOR, 'label[for="department19"]').click()

                # คลิก star51 - star517
                for i in range(1, 18):
                    label_for = f"star5{i}"
                    try:
                        driver.find_element(By.CSS_SELECTOR, f'label[for="{label_for}"]').click()
                    except Exception as e:
                        print(f"ไม่พบ {label_for} หรือคลิกไม่ได้: {e}")

                # คลิกปุ่ม Submit
                try:
                    driver.find_element(By.ID, "submitanswer").click()
                    print("✅ Submitted the form.")

                except Exception as e:
                    print("❌ ไม่สามารถคลิกปุ่ม Submit ได้:", e)

            except Exception as e:
                print("Error:", e)

            finally:
                driver.quit()

        time.sleep(5)

checklist()
