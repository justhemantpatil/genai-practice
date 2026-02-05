import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    caps = DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {
        "browser": "ALL",   # 👈 THIS IS THE KEY
        "performance": "ALL"
    }

    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", caps["goog:loggingPrefs"])

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.maximize_window()
    yield driver
    driver.quit()
