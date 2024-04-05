#!/usr/bin/python3
import requests
import json
import os
import os.path
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter

load_dotenv()
logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler(filename='log/alerthandler.log', when='midnight', interval=1, backupCount=10, encoding='utf-8', delay=False)
formatter = Formatter(fmt='%(asctime)s - %(levelname)s = %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

msg = "No Warnings"
URL="https://api.weather.gov/alerts/active?point=37.4019,-122.0476"
aFile = "activeAlerts.dat"
header = {
        'User-Agent': 'Michael Beatty home automation alert',
        'From': 'mabeatty1978@gmail.com'
    }

ALERTOFFURL = 'https://trigger.sharptools.io/rule/dolOsSYbMI1oYePTJ77a/key/3895e49e-a731-47fe-bb11-a32c1c0b2c34'
ALERTONURL = 'https://trigger.sharptools.io/rule/8ETVMYDMYPXCxZk8IXAd/key/b882e524-24e1-42ea-95fd-bb2f4739f53f'

#Read the current active alerts, if none, instatiate Alerts
if os.path.isfile(aFile):
    with open(aFile,"r") as temp_file:
        Alerts = [line.rstrip('\n') for line in temp_file]
else:
    Alerts = []

#Get the json from NWS
logger.info('Getting current alerts')
r = requests.get(URL, headers=header)
r_data = r.json()

if not r_data['features']:
    #There are no active alerts, delete active alert file
    logger.info('No active alerts')
    if os.path.isfile(aFile):
        os.remove(aFile)
        requests.post(wcAlertOffURL)
    exit()

for i, alert in enumerate(r_data['features']):
    headline = r_data['features'][i]['properties']['headline']
    description = r_data['features'][i]['properties']['description']
    instruction = r_data['features'][i]['properties']['instruction']
    alertId = r_data['features'][i]['id']
    logger.info(headline)

    #If the current alert is not in the existing list, don't send it
    #We only want to send new alerts
    if not alertId in Alerts:
        logger.info("New active alert.  Turning on alert")
        requests.post(wcAlertOnURL)
        msg = headline + "\n\n" + description + "\n\n" + instruction
        a = open(aFile,"a")
        a.write(alertId + "\n")
        a.close()
    i += 1
