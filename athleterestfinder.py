#asks user for favorite athlete, opens up Yelp, searches for restaurant in athlete's hometown, prints 1st (non-sponsored) restaurant name result

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib2 import urlopen

athlete = raw_input("Who's your favorite athlete?")

#launching espn
driver = webdriver.Firefox()
URL = 'http://espn.go.com'
driver.get(URL)
html = urlopen(URL).read()
soup = BeautifulSoup(html, "lxml")

#getting to athlete page
driver.find_element_by_id('global-search-trigger').click()

#finding player page for athlete
search = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='Search Sports, Teams or Players...']")))
search.send_keys(athlete)
search.send_keys(Keys.RETURN)

#clicking on player page search result
playerpage = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Player Page')]")))
playerpage.click()

#converting player page to beautiful soup object
currenturl = driver.current_url
html = urlopen(currenturl).read()
soup = BeautifulSoup(html, "lxml")

#extracting hometown
metadata = soup.find("ul", {"class":"player-metadata floatleft"})
info = str(metadata.get_text())
snippet = info[info.index('in '):info.index('(Age')]
hometown = snippet[3:]
print hometown

#opening up Yelp in another tab
driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
driver.get('http://www.yelp.com')

#entering "restaurant" into search field, and hometown in location, then searching
find = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@class='main-search_field pseudo-input_field']")))
find.send_keys('dinner restaurant')
city = driver.find_element_by_id("dropperText_Mast")
city.clear()
city.send_keys(hometown)
button = driver.find_element_by_xpath("//i[@class='i ig-common_sprite i-search-common_sprite']")
button.click()

#locating and printing 1st (non-sponsored) restaurant name result
currenturl = driver.current_url
html = urlopen(currenturl).read()
soup = BeautifulSoup(html, "lxml")
restel = soup.find_all("a",{"class":"biz-name"})
best = restel[1]
print best.get_text()

