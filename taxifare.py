#takes origin and destination locations in NYC and determines cost to take a taxi there

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib2 import urlopen

driver = webdriver.Firefox()
URL = 'http://www.taxiautofare.com/us/99/New-York-Taxi-fare-calculator/loid'
driver.get(URL)

fromaddress = WebDriverWait(driver,90).until(EC.presence_of_element_located((By.XPATH,"//input[@name='ctl00$MC$Source']")))
fromaddress.send_keys('40-05 21st avenue, astoria,ny')
toaddress = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@name='ctl00$MC$Destination']")))
toaddress.send_keys('888 7th avenue, new york, ny')
driver.implicitly_wait(10)

findfare = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@name='ctl00$MC$CalculateFare']")))
findfare.click()

currenturl = driver.current_url
html = urlopen(currenturl).read()
soup = BeautifulSoup(html, "lxml")
faretag = soup.find("span",{"class":"colorBlack font18px"})
fare = str(faretag.get_text())
sign = fare.index('$')
print fare[len(fare)-sign:]

