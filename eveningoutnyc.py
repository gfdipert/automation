#takes location in NYC, desired activity, and # of people participating, returns specific event, destination, taxifare, and cost per person

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib2 import urlopen

activity = raw_input("What would you like to do? Enter dinner, drinks, or event. ")
home = raw_input("What's your current address? ")
people = raw_input("How many people are in your group, including you? ")

if activity == 'dinner' or 'drinks':

	location = raw_input("Which neighborhood in NYC would you like to go to? ")
	activity = 'dinner'
	desired = location + " New York, NY"

	#yelp
	driver = webdriver.PhantomJS(executable_path='/Applications/phantomjs')
	#driver = webdriver.Firefox()
	URL = 'http://www.yelp.com'
	driver.get(URL)

	#entering "restaurant" into search field, and hometown in location, then searching
	find = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@class='main-search_field pseudo-input_field']")))
	find.send_keys(activity)
	city = driver.find_element_by_id("dropperText_Mast")
	city.clear()
	city.send_keys(desired)
	button = driver.find_element_by_xpath("//i[@class='i ig-common_sprite i-search-common_sprite']")
	button.click()

	#locating and printing 1st (non-sponsored) restaurant name result
	currenturl = driver.current_url
	html = urlopen(currenturl).read()
	soup = BeautifulSoup(html, "lxml")
	restel = soup.find_all("a",{"class":"biz-name"})
	best = restel[1]
	rest = best.get_text()
	rest2 = rest.encode('ascii', 'ignore').decode('ascii')
	rest3 = str(rest2)


	#name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),"+rest2+"]")))
	name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//a[@class="biz-name"]')))
	name.click()

	currenturl = driver.current_url
	html = urlopen(currenturl).read()
	soup = BeautifulSoup(html, "lxml")
	streetaddresstag = soup.find("span",{"itemprop":"streetAddress"})
	streetaddress = str(streetaddresstag.get_text())
	citytag = soup.find("span",{"itemprop":"addressLocality"})
	city = str(citytag.get_text())
	statetag = soup.find("span",{"itemprop":"addressRegion"})
	state = str(statetag.get_text())
	item = soup.find("span", {"class":"business-attribute price-range"})
	dollar = item.get_text()

	destination = streetaddress + " " + city + ", " + state
	#print rest3
	#print destination
	#print dollar
	signs = len(dollar)
	dinnerprice = float(signs * 15)

else:
	now = datetime.datetime.now()
	year = str(now.year)
	month = str(now.month)
	day = str(now.day)

	date = year + month + day

	driver = webdriver.PhantomJS(executable_path='/Applications/phantomjs')
	#driver = webdriver.Firefox()
	URL = 'http://www.yelp.com/events/nyc/browse?start_date=' + date
	driver.get(URL)

	name = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//span[@itemprop="name"]')))
	name.click()

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
	price = str(pricetag.get_text())

	if price == ' Free':
		price = '0.0'

	destination = streetaddress + " " + city + ", " + state

driver = webdriver.Firefox()
URL = 'http://www.taxiautofare.com/us/99/New-York-Taxi-fare-calculator/loid'
driver.get(URL)

fromaddress = WebDriverWait(driver,90).until(EC.presence_of_element_located((By.XPATH,"//input[@name='ctl00$MC$Source']")))
fromaddress.send_keys(home)
toaddress = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@name='ctl00$MC$Destination']")))
toaddress.send_keys(destination)


findfare = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,"//input[@class='btncss']")))
findfare.click()

currenturl = driver.current_url
html = urlopen(currenturl).read()
soup = BeautifulSoup(html, "lxml")
faretag = soup.find("span",{"class":"colorBlack font18px"})
fare = str(faretag.get_text())
sign = fare.index('$')
taxifare = float(fare[len(fare)-sign:])

if activity == 'dinner' or 'drinks':
	pptaxi = taxifare / float(people)
	totalcost = dinnerprice + pptaxi
	print "You will be eating at " + rest3 + "which is located at " + destination
	print "Your dinner will cost approximately" + str(dinnerprice)
	print "Split with your friends you'll have to pay " + str(pptaxi) + " for the taxi."
	print "The total cost to you will be " + str(totalcost)

if activity == 'event':
	pptaxi = taxifare / float(people)
	totalcost = float(price) + pptaxi
	print "You will be going to " + "eventname" + "which is located at " + destination
	print "The event will cost you " + price
	print "Split with your friends you'll have to pay " + str(pptaxi) + " for the taxi."
	print "The total cost to you will be " + str(totalcost)



