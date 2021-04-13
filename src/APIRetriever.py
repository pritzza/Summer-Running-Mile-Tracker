import csv
import json
import requests

from datetime import date

# uses API calls and a csv data file to get API tokens needed to make other API calls
class APIRetriever:
    def __init__(self):

        # header looks like:
        # Club ID,Client ID,Access Token,Refresh Token,Client Secret
        self.DATA_FILE = "API Data.csv"

        # indexes of various API data in data file        
        self.CLUB_ID_INDEX = 0    # [1] for header
        self.CLIENT_ID_INDEX = self.CLUB_ID_INDEX + 1    # Client ID
        self.AT_INDEX        = self.CLIENT_ID_INDEX + 1  # Access Token
        self.RT_INDEX        = self.AT_INDEX + 1         # Refresh Token
        self.CS_INDEX        = self.RT_INDEX + 1         # Client Secret

        self.GRANT_TYPE = "refresh_token"
        self.CLIENT_ID = self.getClientID()
        self.CLIENT_SECRET = self.getClientSecret()
        self.REFRESH_TOKEN = self.getRefreshToken()
    
    def requestNewAccessToken(self, printDebug=False):
        r = requests.post(
        "https://www.strava.com/api/v3/oauth/token?" + 
        "client_id="      + self.CLIENT_ID + 
        "&client_secret=" + self.CLIENT_SECRET + 
        "&grant_type="    + self.GRANT_TYPE + 
        "&refresh_token=" + self.REFRESH_TOKEN
        )

        response = json.loads(r.text)

        if printDebug:
            print("Got Access Token:", response["access_token"], "and Refresh Token:", response["refresh_token"])

        self.saveAccessToken(response["access_token"])
        self.saveRefreshToken(response["refresh_token"])

        return response["access_token"]

    # generic util function to safely return a given element from the data file
    def getDataElement(self, fileName, element):

        with open(self.DATA_FILE, mode='r') as csvFile:
            csvReader = csv.reader(csvFile, delimiter = ',')

            e = list(csvReader)[-1] [element]  # get [element] of last line in CSV

            csvFile.close()

        return e
    
    def writeDataElement(self, fileName, element, data):

        with open(self.DATA_FILE, mode='r') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')

            rows = list(csvReader)

            csvFile.close()

        with open(self.DATA_FILE, mode='w') as csvfile: 
            csvWriter = csv.writer(csvfile, delimiter = ',', lineterminator = '\n') 

            rows[-1] [element] = data
            for row in rows:
                csvWriter.writerow(row) 

            csvFile.close()

    # access token setter and getters
    def getAccessToken(self):
        return self.getDataElement(self.DATA_FILE, self.AT_INDEX)

    def saveAccessToken(self, token):
        self.writeDataElement(self.DATA_FILE, self.AT_INDEX, token)

    # refresh token setter and getters
    def getRefreshToken(self):
        return self.getDataElement(self.DATA_FILE, self.RT_INDEX)

    def saveRefreshToken(self, token):
        self.writeDataElement(self.DATA_FILE, self.RT_INDEX, token)

    # misc API constants' getters
    def getClientSecret(self):
        return self.getDataElement(self.DATA_FILE, self.CS_INDEX)

    def getClientID(self):
        return self.getDataElement(self.DATA_FILE, self.CLIENT_ID_INDEX)
            
    def getClubID(self):
        return self.getDataElement(self.DATA_FILE, self.CLUB_ID_INDEX)