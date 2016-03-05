#opens up a file of Georgia Staff URLs, extracts locations of their offices, and puts them in a CSV file

import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

with open('staffurls.csv','rU') as myfile:
        reader = csv.reader(myfile, delimiter=',')
        rows = list(reader)

firstURL = rows[0]

driver = webdriver.Firefox()
driver.get(firstURL)

locations=list()

for loc in driver.find_elements_by_xpath('.//li[@class="place"]'):
    location = loc.text
    location = location.encode('ascii', 'ignore').decode('ascii')
    location = str(location)
for namey in driver.find_elements_by_xpath('.//strong[@class="name"]'):
    name = namey.text
    name = name.encode('ascii', 'ignore').decode('ascii')
    name = str(name)
    nameloc = name + " # " + location
    locations.append(nameloc)

for URL in rows[1:len(rows)-1]:
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(URL) 
    for loc in driver.find_elements_by_xpath('.//li[@class="place"]'):
        location = loc.text
        location = location.encode('ascii', 'ignore').decode('ascii')
        location = str(location)
    for namey in driver.find_elements_by_xpath('.//strong[@class="name"]'):
        name = namey.text
        name = name.encode('ascii', 'ignore').decode('ascii')
        name = str(name)
        nameloc = name + " # " + location
        locations.append(nameloc)
        
georgialoc = "/Users/gwendolyn/Desktop/Programming/Work/Matthew/Georgia_Tech/georgiafaclocations.csv"
#georgianames = "/Users/gwendolyn/Desktop/Programming/Work/Matthew/Georgia_Tech/georgiafacnames.csv"

with open(georgialoc, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in locations:
        writer.writerow([val]) 
