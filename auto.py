import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

def check_internet(url="https://www.google.com"):
    try:
        requests.get(url, timeout=2)
        return True
    except requests.ConnectionError:
        return False

def clear_browser_data(driver):
    """ลบข้อมูล cookies และ localStorage"""
    try:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        print("🧹 Cleared browser data")
    except Exception as e:
        print(f"⚠️ Error clearing data: {e}")

def create_driver_with_new_session():
    """สร้าง driver ใหม่พร้อม user agent แบบสุ่ม"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # เปิดเมื่อไม่ต้องการเห็นเบราว์เซอร์
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # สุ่ม User Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    # ใช้ temporary profile แยกต่างหาก
    chrome_options.add_argument(f"--user-data-dir=/tmp/chrome_profile_{random.randint(1000, 9999)}")
    
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # ปิดการตรวจจับ webdriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def submit_survey():
    """ฟังก์ชันสำหรับ submit survey"""
    driver = create_driver_with_new_session()
    wait = WebDriverWait(driver, 15)  # เพิ่มเวลารอ
    
    try:
        print("🌐 Opening survey page...")
        driver.get("https://plan.rmu.ac.th/survey/")
        
        # รอให้หน้าโหลดเสร็จสมบูรณ์
        time.sleep(2)
        
        # ลองลบข้อมูลเก่าก่อน
        clear_browser_data(driver)
        
        # รีเฟรชหน้าหลังลบข้อมูล
        driver.refresh()
        time.sleep(3)
        
        print("📝 Filling out survey...")
        
        # ✅ รอจนกระทั่ง element พร้อมก่อนคลิก
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="answerer2"]'))).click()
        time.sleep(0.5)
        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="department19"]'))).click()
        time.sleep(0.5)

        # ✅ คลิก star51 ถึง star517
        for i in range(1, 18):
            label_for = f"star5{i}"
            try:
                element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'label[for="{label_for}"]')))
                driver.execute_script("arguments[0].click();", element)  # ใช้ JavaScript click
                time.sleep(0.2)  # หน่วงเวลาเล็กน้อย
            except Exception as e:
                print(f"⚠️ ไม่พบ {label_for} หรือคลิกไม่ได้: {e}")

        # รอสักครู่ก่อน submit
        time.sleep(1)
        
        # ✅ คลิกปุ่ม Submit
        try:
            submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitanswer")))
            driver.execute_script("arguments[0].click();", submit_btn)  # ใช้ JavaScript click
            print("✅ Submitted the form successfully!")
            
            # รอให้การ submit เสร็จสิ้น
            time.sleep(3)
            return True
            
        except Exception as e:
            print("❌ ไม่สามารถคลิกปุ่ม Submit ได้:", e)
            return False

    except Exception as e:
        print(f"❌ Error during survey submission: {e}")
        return False
    
    finally:
        driver.quit()

def checklist():
    submission_count = 0
    
    while True:
        if not check_internet():
            print("❌ No internet. Waiting...")
            time.sleep(10)
            continue
        
        print(f"\n🚀 Starting submission attempt #{submission_count + 1}")
        
        success = submit_survey()
        
        if success:
            submission_count += 1
            print(f"🎉 Successfully submitted survey #{submission_count}")
        else:
            print("💥 Submission failed, will retry...")
        
        # รอระหว่างการ submit (ลดเวลารอลง)
        wait_time = random.randint(10, 30)  # รอแบบสุ่ม 10-30 วินาที
        print(f"⏳ Waiting {wait_time} seconds before next attempt...")
        time.sleep(wait_time)

if __name__ == "__main__":
    checklist()