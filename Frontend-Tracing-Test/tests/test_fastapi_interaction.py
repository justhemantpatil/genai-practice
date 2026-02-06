import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configuration
APP_URL = "http://localhost:5175" 
TRACING_LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "tracing-logs")
TEST_NAME = "test_fastapi_notes_interaction"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def wait_for_csv():
    time.sleep(3) # Wait for periodic save or refresh

def rename_csv(test_name):
    csv_files = glob.glob(os.path.join(TRACING_LOGS_DIR, "trace_*.csv"))
    if not csv_files:
        return None
    latest_csv = max(csv_files, key=os.path.getctime)
    new_name = os.path.join(TRACING_LOGS_DIR, f"{test_name}.csv")
    if os.path.exists(new_name):
        os.remove(new_name)
    os.rename(latest_csv, new_name)
    return new_name

def test_fastapi_notes_interaction():
    driver = setup_driver()
    try:
        print(f"Running: {TEST_NAME}")
        driver.get(APP_URL)
        
        # Wait for NotesApp to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "notes-container"))
        )
        
        # Fill form
        title_input = driver.find_element(By.XPATH, "//input[@placeholder='Note Title']")
        content_input = driver.find_element(By.XPATH, "//textarea[@placeholder='Note Content']")
        add_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add Note')]")
        
        title_input.send_keys("FastAPI Tracing")
        content_input.send_keys("This note tests the backend integration tracing.")
        add_button.click()
        
        # Wait for status to update
        time.sleep(2)
        
        # Refresh to trigger final trace export
        driver.refresh()
        wait_for_csv()
        
        csv_path = rename_csv(TEST_NAME)
        if csv_path:
            print(f"✓ CSV generated at: {csv_path}")
            with open(csv_path, 'r') as f:
                print(f"CSV Snippet:\n{''.join(f.readlines()[:10])}")
        else:
            print("✗ CSV not found")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_fastapi_notes_interaction()
