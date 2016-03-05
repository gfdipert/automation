#opens up a file of Georgia Faculty URLs, extracts names, downloads images, dumps images in a Folder

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import csv

with open('georgiafacurls.csv','rU') as myfile:
        reader = csv.reader(myfile, delimiter=',')
        rows = list(reader)

firstURL = rows[0]
namelist = []

driver = webdriver.Firefox()
driver.get(firstURL)

for elem in driver.find_elements_by_xpath('.//strong[@class="name"]'):
    name = elem.text
    name = name.encode('ascii', 'ignore').decode('ascii')
    name = str(name)

img = driver.find_element_by_xpath('.//img[@class = "alignleft"]')
src = img.get_attribute('src')
driver.get(src)
img = requests.get(src)
with open(name + " image.jpeg", 'wb') as f:
    f.write(img.content)

namelist.append([name + ".jpeg"])

for URL in rows[1:len(rows)-1]:
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
	driver.get(URL) 
	for elem in driver.find_elements_by_xpath('.//strong[@class="name"]'):
    		name = elem.text
    		name = name.encode('ascii', 'ignore').decode('ascii')
    		name = str(name)
    		namelist.append([name + ".jpeg"])
	img = driver.find_element_by_xpath('.//img[@class = "alignleft"]')
	src = img.get_attribute('src')
	driver.get(src)
	img = requests.get(src)
	with open(name + " image.jpeg", 'wb') as f:
    		f.write(img.content)

georgiaimagelist = "/Users/gwendolyn/Desktop/Programming/Work/Matthew/Georgia_Images/georgiaimagelist.csv"

with open(georgiaimagelist, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in namelist:
        writer.writerow(val) 



