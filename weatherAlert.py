#!/usr/bin/python3
import requests
import json
import os
import os.path
from dotenv import load_dotenv

load_dotenv()

msg = "No Warnings"
URL="https://api.weather.gov/alerts/active?point=37.4019,-122.0476"
aFile = "activeAlerts.dat"
header = {
        'User-Agent': 'This is my test alert',
        'From': 'myname@email.com'
    }

#wcAlertOffURL = #your webcore piston url to turn the alert off 
#wcAlertOnURL = #your webcore piston url to turn the alert on 

#Read the current active alerts, if none, instatiate Alerts
if os.path.isfile(aFile):
    with open(aFile,"r") as temp_file:
        Alerts = [line.rstrip('\n') for line in temp_file]
else:
    Alerts = []

#Get the json from NWS
r = requests.get(URL, headers=header)
r_data = r.json()

if not r_data['features']:
    #There are no active alerts, delete active alert file
    if os.path.isfile(aFile):
        os.remove(aFile)
        requests.post(wcAlertOffURL)
    exit()

for i, alert in enumerate(r_data['features']):
    headline = r_data['features'][i]['properties']['headline']
    description = r_data['features'][i]['properties']['description']
    instruction = r_data['features'][i]['properties']['instruction']
    alertId = r_data['features'][i]['id']
    
    #If the current alert is not in the existing list, don't send it
    #We only want to send new alerts
    if not alertId in Alerts:
        requests.post(wcAlertOnURL)
        msg = headline + "\n\n" + description + "\n\n" + instruction
        a = open(aFile,"a")
        a.write(alertId + "\n")
        a.close()
    i += 1
