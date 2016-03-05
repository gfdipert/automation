#opens up a file of georgia faculty URLs and extracts names and descriptions for each, then dumps them into a spreadsheet

import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

with open('georgiafacurls.csv','rU') as myfile:
        reader = csv.reader(myfile, delimiter=',')
        rows = list(reader)

firstURL = rows[0]

driver = webdriver.Firefox()
driver.get(firstURL)

comb = list()
descrip = list()

for namey in driver.find_elements_by_xpath('.//strong[@class="name"]'):
    name = namey.text
    name = name.encode('ascii', 'ignore').decode('ascii')
    name = str(name)
for elem in driver.find_elements_by_xpath('.//div[@class="field-items"]'):
    description = elem.text
    description = description.encode('ascii', 'ignore').decode('ascii')
    description = str(description)
    description = description.replace("\n","<br>")
    description = description.replace("<br><br><br>Research Areas and Descriptors", "<br><br>Research Areas and Descriptors")
    description = description.replace("Background", "<br>Background")
    description = description.replace("Research", "<br>Research")
    description = name + " # " + description
    descrip.append(description)

for URL in rows[1:len(rows)-1]:
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driver.get(URL) 
    for namey in driver.find_elements_by_xpath('.//strong[@class="name"]'):
        name = namey.text
        name = name.encode('ascii', 'ignore').decode('ascii')
        name = str(name)
    for elem in driver.find_elements_by_xpath('.//div[@class="field-items"]'):
        description = elem.text
        description = description.encode('ascii', 'ignore').decode('ascii')
        description = str(description)
        description = description.replace("\n","<br>")
        description = description.replace("<br><br><br>Research Areas and Descriptors", "<br><br>Research Areas and Descriptors")
        description = description.replace("Background", "<br>Background")
        description = description.replace("Research", "<br>Research")
        description = name + " # " + description
        descrip.append(description)
        
georgiadescrip = "/Users/gwendolyn/Desktop/Programming/Work/Matthew/georgiadescrip.csv"

with open(georgiadescrip, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in descrip:
        writer.writerow([val]) 
