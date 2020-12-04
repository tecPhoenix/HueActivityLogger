import time
import requests
import numpy as np
from datetime import datetime

#Please enter your bridges IP Adress
bridge_ip = "192.168.2.225"


apiKey = "" #API Key for talking with your bridge - Generated after pressing the link button
baseRequestUrl = "http://"+bridge_ip+"/api"
log = open("activities.log","a") #There your logs will be saved after exit the programm

#First Time Authentication
def hueAuthenticate():
	global apiKey
	payload = '{"devicetype":"activityLogger"}'
	
	while (apiKey == ""):
		r = requests.post(baseRequestUrl,data=payload)
		responseArr = r.json()
		
		try:
			if(responseArr[0]["success"]):
				print("Successfully logged in!\nLooking for changes...")
				apiKey = responseArr[0]["success"]["username"]
				open("hueApiKey.txt","w").write(apiKey)
		except:
				print("Please press the link button on your hue bridge")
		time.sleep(2)

def checkForChanges():
	enabled = True
	lightUrl = baseRequestUrl+"/"+apiKey+"/lights"
	data = requests.get(lightUrl).json()
	
	while (enabled == True):
		if (not np.array_equal(requests.get(lightUrl).json(),data)): #Compares the old-saved and new array
			now = datetime.now()
			
			infoString = "Changes detected - "+now.strftime("%d/%m/%Y %H:%M:%S")
			print(infoString)
			log.write(infoString+"\n")
			data = requests.get(lightUrl).json()
		time.sleep(2)

if (open("hueApiKey.txt","r").read() == ""):
	hueAuthenticate()
	checkForChanges()
else:
	print("User already logged in!\nLooking for changes...")
	apiKey = open("hueApiKey.txt","r").read()
	checkForChanges()
	





