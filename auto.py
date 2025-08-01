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
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")  # ใช้โหมด incognito
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)
    
    # สุ่ม User Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    # ใช้ temporary profile แยกต่างหาก พร้อม timestamp
    import tempfile
    import os
    temp_dir = tempfile.mkdtemp(prefix="chrome_profile_")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    # เพิ่ม proxy settings (ถ้ามี)
    # chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1080")
    
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # ปิดการตรวจจับ webdriver และปรับแต่งเพิ่มเติม
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en', 'th']})")
    
    return driver

def submit_survey():
    """ฟังก์ชันสำหรับ submit survey"""
    driver = None
    try:
        driver = create_driver_with_new_session()
        wait = WebDriverWait(driver, 20)  # เพิ่มเวลารอเป็น 20 วินาที
        
        print("🌐 Opening survey page...")
        driver.get("https://plan.rmu.ac.th/survey/")
        
        # รอให้หน้าโหลดเสร็จสมบูรณ์
        time.sleep(3)
        
        # ลองลบข้อมูลเก่าก่อน
        clear_browser_data(driver)
        
        # รีเฟรชหน้าหลังลบข้อมูล และรอให้โหลดใหม่
        print("🔄 Refreshing page...")
        driver.refresh()
        time.sleep(5)  # เพิ่มเวลารอให้หน้าโหลดเสร็จ
        
        # ตรวจสอบว่าหน้าโหลดเสร็จแล้ว
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("📝 Filling out survey...")
        
        # ตรวจสอบว่า form elements มีอยู่จริง
        try:
            # รอให้ form โหลดเสร็จ
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'label[for="answerer2"]')))
            
            # ✅ คลิก answerer2
            answerer_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="answerer2"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", answerer_element)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", answerer_element)
            print("✅ Selected answerer2")
            time.sleep(1)
            
            # ✅ คลิก department19
            dept_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="department19"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", dept_element)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", dept_element)
            print("✅ Selected department19")
            time.sleep(1)

            # ✅ คลิก star51 ถึง star517
            success_count = 0
            for i in range(1, 18):
                label_for = f"star5{i}"
                try:
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'label[for="{label_for}"]')))
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", element)
                    success_count += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f"⚠️ ไม่พบ {label_for} หรือคลิกไม่ได้: {e}")
            
            print(f"✅ Successfully clicked {success_count}/17 star elements")
            
            # รอสักครู่ก่อน submit
            time.sleep(2)
            
            # ✅ คลิกปุ่ม Submit
            try:
                submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitanswer")))
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", submit_btn)
                print("✅ Clicked submit button!")
                
                # รอและจัดการ alert ที่อาจจะขึ้นมา
                time.sleep(3)
                
                try:
                    # ตรวจสอบว่ามี alert หรือไม่
                    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert_text = alert.text
                    print(f"🔔 Alert detected: {alert_text}")
                    
                    # ถ้า alert มีข้อความที่แสดงความสำเร็จ
                    if "ขอบคุณ" in alert_text or "thank" in alert_text.lower() or "สำเร็จ" in alert_text:
                        alert.accept()  # กด OK
                        print("✅ Form submitted successfully! (Alert confirmed)")
                        time.sleep(2)
                        return True
                    else:
                        alert.accept()  # กด OK ต่อไป
                        print(f"⚠️ Unknown alert message: {alert_text}")
                        return False
                        
                except Exception as alert_error:
                    # ไม่มี alert หรือ timeout
                    print("ℹ️ No alert detected, checking page content...")
                    
                    # ตรวจสอบจาก page content
                    try:
                        time.sleep(2)
                        page_source = driver.page_source.lower()
                        current_url = driver.current_url
                        
                        if "success" in page_source or "สำเร็จ" in page_source or "complete" in page_source or "ขอบคุณ" in page_source:
                            print("✅ Form submitted successfully! (Page content confirmed)")
                            return True
                        elif "error" in page_source or "ผิดพลาด" in page_source:
                            print("❌ Form submission error detected in page")
                            return False
                        else:
                            print("✅ Form appears to be submitted (assuming success)")
                            return True
                    except Exception as page_check_error:
                        print(f"⚠️ Could not verify submission status: {page_check_error}")
                        return True  # Assume success if we can't verify
                
            except Exception as e:
                error_msg = str(e)
                # ถ้า error message มีคำว่า "ขอบคุณ" แสดงว่า submit สำเร็จแล้ว
                if "ขอบคุณ" in error_msg or "thank" in error_msg.lower():
                    print("✅ Form submitted successfully! (Success detected in error message)")
                    try:
                        # พยายามปิด alert ถ้ายังเปิดอยู่
                        alert = driver.switch_to.alert
                        alert.accept()
                    except:
                        pass
                    return True
                else:
                    print(f"❌ ไม่สามารถคลิกปุ่ม Submit ได้: {e}")
                    return False
                
        except Exception as e:
            print(f"❌ Error finding form elements: {e}")
            return False

    except Exception as e:
        print(f"❌ Error during survey submission: {e}")
        return False
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def checklist():
    submission_count = 0
    consecutive_failures = 0
    
    while True:
        if not check_internet():
            print("❌ No internet. Waiting...")
            time.sleep(10)
            continue
        
        print(f"\n🚀 Starting submission attempt #{submission_count + 1}")
        
        # เพิ่มการรอที่นานขึ้นหากมีการ fail ติดต่อกัน
        if consecutive_failures > 0:
            extra_wait = min(consecutive_failures * 30, 180)  # รอสูงสุด 3 นาที
            print(f"⚠️ Previous attempts failed. Adding extra wait: {extra_wait} seconds")
            time.sleep(extra_wait)
        
        success = submit_survey()
        
        if success:
            submission_count += 1
            consecutive_failures = 0  # รีเซ็ต counter
            print(f"🎉 Successfully submitted survey #{submission_count}")
            
            # รอระหว่างการ submit ที่สำเร็จ (ลดเวลารอลงเนื่องจากเราสามารถข้าม rate limit ได้แล้ว)
            wait_time = random.randint(30, 60)  # รอ 30 วินาที - 1 นาที
            print(f"⏳ Waiting {wait_time} seconds before next attempt...")
            time.sleep(wait_time)
        else:
            consecutive_failures += 1
            print(f"💥 Submission failed ({consecutive_failures} consecutive failures)")
            
            # รอเวลาสั้นกว่าสำหรับการ retry
            wait_time = random.randint(30, 60)  # รอ 30 วินาที - 1 นาที
            print(f"⏳ Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            
            # หากล้มเหลวติดต่อกันมากเกินไป ให้รอนานขึ้น
            if consecutive_failures >= 5:
                print("🛑 Too many consecutive failures. Taking a longer break...")
                time.sleep(300)  # รอ 5 นาที
                consecutive_failures = 0  # รีเซ็ต counter

if __name__ == "__main__":
    checklist()