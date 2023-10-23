import time

from dcentralab_qa_infra_automation.walletsActions.MetamaskActions import MetamaskActions
from selenium import webdriver


def test_chrome_with_extension():
    options = webdriver.ChromeOptions()
    extension = "extensions/metamask.crx"
    options.add_extension(extension)
    driver = webdriver.Chrome(options=options)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.new_window("tab")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#connect")
    time.sleep(45)

