#grabs YELP event name and location

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib2 import urlopen
import datetime

now = datetime.datetime.now()

year = str(now.year)
month = str(now.month)
day = str(now.day)

date = year + month + day

driver = webdriver.Firefox()
#URL = 'http://www.yelp.com/events/nyc/browse?start_date=' + date
URL = 'http://www.yelp.com/events/brooklyn-sunday-funday-a-boozy-brooklyn-tasting-tour'
driver.get(URL)

#name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//span[@itemprop="name"]')))
#name.click()

currenturl = driver.current_url
html = urlopen(currenturl).read()
soup = BeautifulSoup(html, "lxml")

eventnametag = soup.find("span",{"itemprop":"name"})
eventname = str(eventnametag.get_text())
streetaddresstag = soup.find("span",{"itemprop":"streetAddress"})
streetaddress = str(streetaddresstag.get_text())
citytag = soup.find("span",{"itemprop":"addressLocality"})
city = str(citytag.get_text())
statetag = soup.find("span",{"itemprop":"addressRegion"})
state = str(statetag.get_text())
pricetag = soup.find("span",{"class":"i-wrap ig-wrap-common_sprite i-24x24_movie-common_sprite-wrap event-details_ticket-info"})
price = str(pricetag.get_text())[2:]

if price == ' Free':
	print "This event is free!"
	price = float(0)
else:
	price = float(price)
	print price

destination = streetaddress + " " + city + ", " + state

print eventname


