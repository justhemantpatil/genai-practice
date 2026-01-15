import time
from selenium.webdriver.common.by import By

def test_full_notes_flow(driver):
    driver.get("http://localhost:5173")
    time.sleep(2)

    # Login
    driver.find_element(By.XPATH, "//input[@placeholder='Username']").send_keys("hemantadmin")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(2)

    assert "Welcome" in driver.page_source

    # Add note
    driver.find_element(By.XPATH, "//input[@placeholder='Title']").send_keys("Selenium Note")
    driver.find_element(By.XPATH, "//textarea[@placeholder='Content']").send_keys("Automated content")
    driver.find_element(By.XPATH, "//button[text()='Add Note']").click()
    time.sleep(2)

    assert "Selenium Note" in driver.page_source

    # Delete note
    driver.find_element(By.XPATH, "//button[text()='Delete']").click()
    time.sleep(2)

    print("FULL E2E TEST PASSED ✅")
