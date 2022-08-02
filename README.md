# NWS Weather Alert

## This script utilizes the National Weather Service's API to get current weather alerts for your location.  It uses this information to turn on and off a virtual switch (or do whatever else you want) in WebCoRE.  When run in a cronjob, it will turn on the switch any time a new alert is issued and off whenever there are no active alerts

## Getting the correct weather data
To setup this script to get your weather data is to plug your lat/lon into the NWS API using your locations GPS cordinates

```
https://api.weather.gov/alerts/active?point=37.4019,-122.0476
```
Supply these points values to the URL value in the API

I use this script for a few other purposes, most of which I've stripped out, but I left in a breif example how to get data from the response if you have any use for it.

From here, you just need to create a virtual switch (I called mine WeatherAlert), enable it as a valid device in WebCoRE, and then create 2 simple WebCoRE pistons

```
execute
  with 
    WeatherAlert
  do
    turn on
  end with
```

and another to turn it off
```
execute
  with
    WeatherAlert
  do
    turn off
  end with
```

Take note of the "External URL" of the pistons in the Quick Notes at the top.  You will supply these to the wcAlertOffURL and wcAlertOnURL in the script

As a final step in the script, it's a good idea to set values for the USER-AGENT and FROM in the body header.  Change the lines in the code to be something unique to you.  The From field will give the NWS the ability to contact you if there are problems or if you are doing something incorrectly.  The User Agent specifies to them more details about what is sending the data.  These values can be any string you want.

Finally, just setup cron to run this as frequently as you want.  I run it every minute as the NWS documentation says the rate limit is very generous. 

To take this a step further, I have wall mounted tables that display panels in ActionTiles.  I have the switch setup to display on my tablets so that they display pulsing red with a lightning bolt icon to indicate there is a weather alert.


