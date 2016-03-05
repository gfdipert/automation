#takes CSV of travel info data (see commuter_schedule.csv); determines what will get you there fastest, and the latest mode you can take to arrive by your destination time

import csv
import datetime

with open('commuter_schedule.csv','rU') as myfile:
	reader = csv.reader(myfile, delimiter=',')
	rows = list(reader)

#to get schedule only, and not bus and train travel times and the rest of that text
schedule = rows[3:9]

#print schedule

#converts bus and train travel times to a timedelta object
btime = datetime.timedelta(hours=2,minutes=15)
ttime = datetime.timedelta(hours=1,minutes=57)

#creates a dictionary with the bus name paired up with departure time; departure times have been convered to datetime objects
y = dict()
for value in schedule:
	timestr = value[1]
	thours = int(timestr[0:2])
	tminutes = int(timestr[3:5])
	tsecs = int(timestr[6:8])
	timestamp = datetime.datetime(year=2015,month=10,day=31,hour=thours,minute=tminutes,second=tsecs)
	y[value[0]] = timestamp
#print y

#creates dictionary of arrival times for each mode of transportation
arrivaldic = dict()
for value in schedule:
	if value[2] == 'BUS':
		arrivaldic[value[0]] = y[value[0]] + btime
	if value[2] == 'TRAIN':
		arrivaldic[value[0]] = y[value[0]] + ttime
#print arrivaldic

#creates list of arrival times and finds earliest arrival time
earliesttime = min(list(arrivaldic.values()))

#finds bus or train number corresponding to earliest time in arrival
for key, value in arrivaldic.iteritems():
	if value == earliesttime:
		earliestmode = key
print "You can get there the fastest by taking " + earliestmode

#creates list of arrival times before one pm
beforeone = list()
for arrival in list(arrivaldic.values()):
	onepm = datetime.datetime(year=2015,month=10,day=31,hour=13,minute=0,second=0)
	if arrival < onepm:
		beforeone.append(arrival)

#finds modes that match the before one PM arrival times
modenames = list()
for arrival in beforeone:
	for key, value in arrivaldic.iteritems():
		if arrival == value:
			modenames.append(key)

#print modenames

#finds the bus departure time corresponding to the list 
departurelist = list()
for modename in modenames:
	if modename in list(y.keys()):
		departure = y[modename]
		departurelist.append(departure)
		latestdeparture = max(departurelist)

#print latestdeparture

#finds the name of the bus with the latest departure time
for key, value in y.iteritems():
	if latestdeparture == value:
		latestbus = key

print "The latest bus that will get you to your destination by one pm is " + latestbus


