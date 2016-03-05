#takes ingredients and returns recipe for first dish listed in epicurious that uses those ingredients

from bs4 import BeautifulSoup
from urllib2 import urlopen

user_input = raw_input("Enter your ingredients here: ")
if "," in user_input:
	ingredients = user_input.split(",")
	ingredients = user_input.split()
else:
	ingredients = user_input.split()

for word in ingredients:
	if word == 'and':
		ingredients.pop(ingredients.index('and'))

BASE_URL = "http://www.epicurious.com"
URL = "http://www.epicurious.com/tools/searchresults?search="
for word in ingredients:
	URL = URL + word + "+"

#creating URL for first search result
html = urlopen(URL).read()
soup = BeautifulSoup(html, "lxml")
title = soup.find("div", "sr_title")

if title == None:
	print "Your ingredients are too weird!"
	exit()
else:
	linkitem = title.find("a","recipeLnk")
	link = linkitem.get("href")
	fulllink = BASE_URL + link

#opening URL
recipehtml = urlopen(fulllink).read()
soups = BeautifulSoup(recipehtml, "lxml")

#
item = soups.find("h1", {"itemprop":"name"})
title = item.get_text()

print "Name: " + title + "\n"

#getting description
descrip = soups.find("div","dek")
if descrip == None:
	print "Ingredients: " + "\n"
else:
	description = descrip.get_text()
	print "Description: " + "\n\n" + description + "\n\n" + "Ingredients: " + "\n"

#get ingredients
ingred = soups.find_all("li",{"itemprop":"ingredients"})
for item in ingred:
	print item.get_text()

print "\n"
print "Preparation:" + "\n"

prep = soups.find_all("li","preparation-step")
for item in prep:
	print item.get_text()

nutrit = soups.find_all("div","nutritional-info")
for item in nutrit:
	nutrittext = item.get_text()
	nutrition = nutrittext[0:nutrittext.find("Nutritional")]
	print nutrition
