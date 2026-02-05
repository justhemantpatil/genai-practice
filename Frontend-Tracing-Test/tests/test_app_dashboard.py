"""
Test Case 1: App + Dashboard Interaction
This test interacts with the main App component and Dashboard component
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
APP_URL = "http://localhost:5175"  # Vite default dev server
TRACING_LOGS_DIR = os.path.join(os.path.dirname(__file__), "..", "tracing-logs")
TEST_NAME = "test_app_dashboard_interaction"

def setup_driver():
    """Initialize Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Uncomment to run headless
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def wait_for_csv():
    """Wait for CSV file to be generated"""
    time.sleep(2)  # Wait for file write to complete

def get_latest_csv():
    """Get the most recently created CSV file"""
    csv_files = glob.glob(os.path.join(TRACING_LOGS_DIR, "*.csv"))
    if not csv_files:
        return None
    latest_csv = max(csv_files, key=os.path.getctime)
    return latest_csv

def rename_csv(test_name):
    """Rename the latest CSV to test name"""
    latest_csv = get_latest_csv()
    if latest_csv:
        new_name = os.path.join(TRACING_LOGS_DIR, f"{test_name}.csv")
        # If file already exists, remove it
        if os.path.exists(new_name):
            os.remove(new_name)
        os.rename(latest_csv, new_name)
        print(f"✓ CSV renamed to: {new_name}")
        return new_name
    else:
        print("✗ No CSV file found!")
        return None

def test_app_dashboard_interaction():
    """Test Case 1: Interact with App and Dashboard components"""
    driver = setup_driver()
    
    try:
        print(f"\n{'='*60}")
        print(f"Running: {TEST_NAME}")
        print(f"{'='*60}\n")
        
        # Navigate to app
        print("→ Navigating to app...")
        driver.get(APP_URL)
        time.sleep(2)
        
        # Interact with App component - Click "Toggle Glow" button
        print("→ Clicking 'Toggle Glow' in App component...")
        glow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Toggle Glow')]"))
        )
        glow_button.click()
        time.sleep(1)
        
        # Click "System Alert" button
        print("→ Clicking 'System Alert' in App component...")
        alert_button = driver.find_element(By.XPATH, "//button[contains(., 'System Alert')]")
        alert_button.click()
        time.sleep(1)
        
        # Interact with Dashboard component - Click "Refresh Data"
        print("→ Clicking 'Refresh Data' in Dashboard component...")
        refresh_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Refresh Data')]"))
        )
        refresh_button.click()
        time.sleep(1)
        
        # Click "Upload Logs" in Dashboard
        print("→ Clicking 'Upload Logs' in Dashboard component...")
        upload_button = driver.find_element(By.XPATH, "//button[contains(., 'Upload Logs')]")
        upload_button.click()
        time.sleep(1)
        
        # Refresh page to trigger CSV save via beforeunload
        print("→ Refreshing page to trigger CSV export...")
        driver.refresh()
        wait_for_csv()
        
        # Check and rename CSV
        csv_path = rename_csv(TEST_NAME)
        
        if csv_path and os.path.exists(csv_path):
            file_size = os.path.getsize(csv_path)
            print(f"✓ Test PASSED: CSV generated ({file_size} bytes)")
            
            # Read and display first few lines
            with open(csv_path, 'r') as f:
                lines = f.readlines()[:5]
                print(f"\nFirst 5 lines of CSV:")
                for line in lines:
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
    test_app_dashboard_interaction()
