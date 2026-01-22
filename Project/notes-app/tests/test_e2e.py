import time
from selenium.webdriver.common.by import By

def test_full_notes_flow(driver):
    driver.get("http://localhost:5173")
    time.sleep(3)  # Increased wait for page load and babel plugin to inject logs

    # Login
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("hemantadmin")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(3)  # Wait for logs to be sent

    assert "Welcome" in driver.page_source

    # Add note
    driver.find_element(By.XPATH, "//input[@placeholder='Title']").send_keys("Selenium Note")
    driver.find_element(By.XPATH, "//textarea[@placeholder='Content']").send_keys("Automated content")
    driver.find_element(By.XPATH, "//button[text()='Add Note']").click()
    time.sleep(3)  # Wait for logs to be sent

    assert "Selenium Note" in driver.page_source

    # Delete note
    driver.find_element(By.XPATH, "//button[text()='Delete']").click()
    time.sleep(3)  # Wait for logs to be sent and recorded

    print("\n--- BROWSER LOGS ---")
    logs = driver.get_log("browser")

    ui_trace_count = 0
    for log in logs:
        if "UI_TRACE" in log["message"] or "[UI_TRACE]" in log["message"]:
            print(log["message"])
            ui_trace_count += 1
    
    print(f"\nCaptured {ui_trace_count} UI trace logs")
    print("FULL E2E TEST PASSED ✅")
