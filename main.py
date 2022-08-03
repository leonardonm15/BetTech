from selenium import webdriver
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
driver.get("https://livecasino.bet365.com/Play/LiveRoulette")
assert "Python" in driver.title

