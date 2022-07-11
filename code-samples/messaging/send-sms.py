#!/usr/bin/env python
from ringcentral import SDK
import os,sys

# Load the environment file
from dotenv import load_dotenv
load_dotenv()

# Make sure you provide RECIPIENT in the .env file.
RECIPIENT    = os.environ.get('SMS_RECIPIENT')

# Make sure you provide the RC_SERVER_URL, your RC_CLIENT_ID and RC_CLIENT_SECRET in the .env file.
# You get these parameters from your application dashbord in your developer account 
# https://developers.ringcentral.com/ 
rcsdk = SDK( os.environ.get('RC_CLIENT_ID'),
             os.environ.get('RC_CLIENT_SECRET'),
             os.environ.get('RC_SERVER_URL') )
platform = rcsdk.platform()

# Make sure you provide the RC_USERNAME(phone number/email id), RC_PASSWORD and RC_EXTENSION in the .env file.
# You get these parameters from your sandbox account on the developer portal 
# https://developers.ringcentral.com/
try:
  platform.login(os.environ.get('RC_USERNAME'),
                 os.environ.get('RC_EXTENSION'),
                 os.environ.get('RC_PASSWORD') )
except:
  sys.exit("Unable to authenticate to platform. Check credentials.")

# On login success fetch the 'from_number' that the logged in user is allowed to send SMS from 
# by looking for "SmsSender" feature*/
def read_extension_phone_number():
  try:
    resp = platform.get("/restapi/v1.0/account/~/extension/~/phone-number")
    jsonObj = resp.json()
  except e:
    sys.exit("Unable to fetch SMS-enabled phone numbers")
  for record in jsonObj.records:
    for feature in record.features:
      if feature == "SmsSender":
        return send_sms(record.phoneNumber)
  sys.exit("No SMS-enabled phone number found")

# Send the actual SMS message by providing the RECIPIENT. This RECIPIENT can be 
# any working phone number. 
def send_sms(fromNumber):
  try:
    resp = platform.post('/restapi/v1.0/account/~/extension/~/sms',
              {
                  'from' : { 'phoneNumber': fromNumber },
                  'to'   : [ {'phoneNumber': RECIPIENT} ],
                  'text' : 'Hello World from Python!'
              })
    jsonObj = resp.json()
  except:
    sys.exit("Unable to send SMS")
  print (jsonObj.messageStatus)

read_extension_phone_number()