import urllib2
import json
import os
import glob
import time
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
CITY = "Zurich"
GPS_COORDS = "47.3738,8.5371"
DARKSKY_API_KEY = "a35e794af0d32e8e344a3a2e072198fd"
MINUTES_BETWEEN_READS = 15
# ---------------------------------

URL='https://api.darksky.net/forecast/a35e794af0d32e8e344a3a2e072198fd/47.3901,8.661?exclude=minutely,hourly,daily,alerts,flags&units=ca'

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_current_conditions():
	api_conditions_url = "https://api.darksky.net/forecast/" + DARKSKY_API_KEY + "/" + GPS_COORDS + "?units=ca&exclude=minutely,hourly,daily,alerts,flags"
	try:
		f = urllib2.urlopen(api_conditions_url)
	except:
		return []
	json_currently = f.read()
	f.close()
	return json.loads(json_currently)

def weather_icon(ds_icon):
	icon = {
		"clear-day"            	: ":sunny:",
		"clear-night"           : ":new_moon_with_face:",
		"rain"                  : ":umbrella:",
		"snow"                  : ":snowflake:",
		"sleet"                 : ":sweat_drops: :snowflake:",
		"wind"                  : ":wind_blowing_face:",
		"fog"                   : ":fog:",
		"cloudy"                : ":cloud:",
		"partly-cloudy-day"     : ":partly_sunny:",
		"partly-cloudy-night"   : ":new_moon_with_face:",
		"unknown"               : ":sun_with_face:",
	}
	return icon.get(ds_icon,":sun_with_face:")

def weather_status_icon(ds_icon,moon_phase):
	icon = weather_icon(ds_icon)
	if (icon == ":new_moon_with_face:"):
		return moon_icon(moon_phase)
	return icon

def main():
	curr_conditions = get_current_conditions()
	if ('currently' not in curr_conditions):
		print "Error! Dark Sky API call failed, check your GPS coordinates and make sure your Dark Sky API key is valid!\n"
		print curr_conditions
		exit()
	else:
		streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
	while True:
		
		curr_conditions = get_current_conditions()
		if ('currently' not in curr_conditions):
			print "Error! Dark Sky API call failed. Skipping a reading then continuing ...\n"
			print curr_conditions
		else:
			streamer.log(":house: Location",GPS_COORDS)
			
			if 'humidity' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['humidity']):
				streamer.log(":droplet: Humidity(%)", curr_conditions['currently']['humidity']*100)

			if 'temperature' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['temperature']): 
				streamer.log("Temperature",curr_conditions['currently']['temperature'])

			if 'apparentTemperature' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['apparentTemperature']): 
				streamer.log("Feels Like",curr_conditions['currently']['apparentTemperature'])

			if 'dewPoint' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['dewPoint']):
				streamer.log("Dewpoint",curr_conditions['currently']['dewPoint'])

			if 'windSpeed' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['windSpeed']):
				streamer.log(":dash: Wind Speed",curr_conditions['currently']['windSpeed'])

			if 'windGust' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['windGust']):
				streamer.log(":dash: Wind Gust",curr_conditions['currently']['windGust'])

			if 'windBearing' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['windBearing']):
				streamer.log(":dash: Wind Direction",wind_dir_icon(curr_conditions['currently']['windBearing']))

			if 'pressure' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['pressure']):
				streamer.log("Pressure",curr_conditions['currently']['pressure'])

			if 'precipIntensity' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['precipIntensity']):
				streamer.log(":umbrella: Precipitation Intensity",curr_conditions['currently']['precipIntensity'])

			if 'precipProbability' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['precipProbability']):
				streamer.log(":umbrella: Precipitation Probabiity(%)",curr_conditions['currently']['precipProbability']*100)

			if 'cloudCover' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['cloudCover']):
				streamer.log(":cloud: Cloud Cover(%)",curr_conditions['currently']['cloudCover']*100)

			if 'uvIndex' in curr_conditions['currently'] and isFloat(curr_conditions['currently']['uvIndex']):
				streamer.log(":sunny: UV Index:",curr_conditions['currently']['uvIndex'])

			if 'summary' in curr_conditions['currently']:
				streamer.log(":cloud: Weather Summary",curr_conditions['currently']['summary'])

			if 'hourly' in curr_conditions:
				streamer.log("Today's Forecast",curr_conditions['hourly']['summary'])

			if 'daily' in curr_conditions:
				if 'data' in curr_conditions['daily']:
					if 'moonPhase' in curr_conditions['daily']['data'][0]:
						moon_phase = curr_conditions['daily']['data'][0]['moonPhase']
						streamer.log(":crescent_moon: Moon Phase",moon_icon(moon_phase))
						streamer.log(":cloud: Weather Conditions",weather_status_icon(curr_conditions['currently']['icon'],moon_phase))

			streamer.flush()
		time.sleep(60*MINUTES_BETWEEN_READS)

if __name__ == "__main__":
    main()
    
