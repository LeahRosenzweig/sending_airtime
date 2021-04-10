### This is the code for automatic system of sending airtime and SMS ###
### Code was initially implemented by Yuan Yuan ###

from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import numpy as np
import glob
import os
import dask.dataframe as dd
import re 
import datetime
import io
import requests
import json
from gsheets import Sheets
from bs4 import BeautifulSoup
import africastalking
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load env variables for our apps (stored in .env)
kenya_username = os.getenv('KENYA_APP_NAME')
nigeria_username = os.getenv('NIGERIA_APP_NAME')

kenya_api_key = os.getenv('KENYA_API_KEY') 
nigeria_api_key = os.getenv('NIGERIA_API_KEY')

# Convert google sheet to dataframe:
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('serviceAccount.json', scope)
client = gspread.authorize(creds)

# open specific google sheet #
sheet = client.open('KYNG_users_phone_export_followup').sheet1
google_sheet_data = sheet.get_all_records()
rawData = pd.read_json(json.dumps(google_sheet_data))
rawData.columns = ["timestamp", "last_name", "first_name", "phone_nbr", "country1"]
data = rawData
# reformatting time stamp
data["timestamp"] = data["timestamp"].apply(lambda x: datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

# define today
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(days=1)

# function to clean phone number
def clean_phone_nbr(phone_number):
    # ensure number is string and strip any whitespace
    phone = str(phone_number).strip().replace(" ", "")

    # if phone number begins with a 0, drop the 0
    if phone[0] == "0":
        phone = phone[1:]
    
    return phone

# Go through rows in dataframe
(rows, columns) = data.shape
print("Going through data...")
for i in reversed(range(rows)):
    phone = data.loc[i, "phone_nbr"]
    country1 = data.loc[i, "country1"]
    date = data.loc[i, "timestamp"]

    # Only send money if row's date is yesterday
    if date.date() == yesterday.date():
        if country1 == "Kenya":
            username = kenya_username
            sender_id = os.getenv('SENDER_ID') 
            country_code = "254"
            currency_code = "KES"
            amount = "25"
            api_key = kenya_api_key
        elif country1 == "Nigeria":
            username = nigeria_username
            sender_id = None
            country_code = "234"
            currency_code = "NGN"
            amount = "100"
            api_key = nigeria_api_key

        phone_nbr = clean_phone_nbr(phone)
        
        # apply country code if doesn't exist
        if len(phone_nbr) < 11:
            # phone number must be string to add to string
            phone_nbr = country_code + phone_nbr
        
        print("Sending to:", phone_nbr, " in:", country1)

        try:
            # Initialize Africastalking
            africastalking.initialize(username, api_key)

            # Send airtime to respondent
            airtime = africastalking.Airtime
            airresponse = airtime.send("+" + phone_nbr, amount, currency_code)
            print("Airtime response:")
            print(airresponse)
            print()

            # Send sms to respondent
            sms = africastalking.SMS
            message = "Thank you for taking our Facebook survey. Here is your airtime!"
            smsresponse = sms.send(message, ["+" + phone_nbr], sender_id)


            print("SMS response:")
            print(smsresponse)
            print()
            
        except Exception as e:
            print("Not sent due to an error:")
            print(e)


print("Finished")