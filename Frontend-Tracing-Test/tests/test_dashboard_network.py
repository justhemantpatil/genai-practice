"""
Test Case 2: Dashboard + NetworkPanel Interaction
This test interacts with Dashboard and NetworkPanel components
"""
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
TEST_NAME = "test_dashboard_network_interaction"

def setup_driver():
    """Initialize Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def wait_for_csv():
    """Wait for CSV file write"""
    time.sleep(2)

def get_latest_csv():
    """Get most recent CSV"""
    csv_files = glob.glob(os.path.join(TRACING_LOGS_DIR, "*.csv"))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getctime)

def rename_csv(test_name):
    """Rename CSV to test name"""
    latest_csv = get_latest_csv()
    if latest_csv:
        new_name = os.path.join(TRACING_LOGS_DIR, f"{test_name}.csv")
        if os.path.exists(new_name):
            os.remove(new_name)
        os.rename(latest_csv, new_name)
        print(f"✓ CSV renamed to: {new_name}")
        return new_name
    return None

def test_dashboard_network_interaction():
    """Test Case 2: Interact with Dashboard and NetworkPanel"""
    driver = setup_driver()
    
    try:
        print(f"\n{'='*60}")
        print(f"Running: {TEST_NAME}")
        print(f"{'='*60}\n")
        
        print("→ Navigating to app...")
        driver.get(APP_URL)
        time.sleep(2)
        
        # Dashboard interactions
        print("→ Clicking 'Optimize' in Dashboard...")
        optimize_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Optimize')]"))
        )
        optimize_button.click()
        time.sleep(1.5)
        
        print("→ Clicking 'Settings' in Dashboard...")
        settings_button = driver.find_element(By.XPATH, "//button[contains(., 'Settings')]")
        settings_button.click()
        time.sleep(1)
        
        # NetworkPanel interactions
        print("→ Clicking 'Ping Gateway' in NetworkPanel...")
        ping_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ping Gateway')]"))
        )
        ping_button.click()
        time.sleep(1)
        
        print("→ Clicking 'Trace Route' in NetworkPanel...")
        trace_button = driver.find_element(By.XPATH, "//button[contains(., 'Trace Route')]")
        trace_button.click()
        time.sleep(2)  # Trace route has recursive calls
        
        # Trigger CSV save
        print("→ Closing page to trigger CSV export...")
        driver.refresh()
        wait_for_csv()
        
        csv_path = rename_csv(TEST_NAME)
        
        if csv_path and os.path.exists(csv_path):
            file_size = os.path.getsize(csv_path)
            print(f"✓ Test PASSED: CSV generated ({file_size} bytes)")
            
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                print(f"\nTotal rows in CSV: {len(lines)}")
                print(f"First 5 lines:")
                for line in lines[:5]:
                    print(f"  {line.strip()}")
        else:
            print("✗ Test FAILED: CSV not generated")
            
    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print(f"\n{'='*60}\n")
        driver.quit()

if __name__ == "__main__":
    test_dashboard_network_interaction()
