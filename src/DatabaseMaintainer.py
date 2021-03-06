import csv
import json
import requests

from datetime import date

# uses API calls to get data which it writes to a csv db
class DatabaseMaintainer:
    def __init__(self, clubID, csvName, accessToken):
        
        self.CLUB_ID = str(clubID)
        self.CSV_FILE_NAME = csvName
        self.ACCESS_TOKEN = accessToken
        self.STARTING_URL = "https://www.strava.com/api/v3/"

        self.DB_EXISTS = self.doesDBExist()
        self.NUM_DB_ENTRIES = self.getNumEntries()

    def doesDBExist(self):
        try:
            open(self.CSV_FILE_NAME)
            return True

        except FileNotFoundError:
            return False

    def getNumEntries(self):
        csv_file = csv.reader(open(self.CSV_FILE_NAME, 'r'), delimiter=',')

        entries = 0

        for row in csv_file:
            entries += 1

        return entries
        
    def makeURL(self, path):
        return self.STARTING_URL + path + "access_token=" + self.ACCESS_TOKEN

    def getResult(self, URL):
        return json.loads(requests.get(URL).text)

    def updateDatabase(self, activities, printDebug=False):

        activities.reverse()    # we reverse the dictionary so that the entries are written in chronological order top to bottom (old -> new)

        added = 0

        for entry in activities:

            data = [ 
                entry["athlete"]["firstname"] + ' ' + entry["athlete"]["lastname"],     # Athlete Name
                entry["name"],                                                          # Run Name
                str(entry["distance"]),                                                 # Run Distance
                str(entry["moving_time"]),                                              # Run Duration
                str(entry["total_elevation_gain"])                                      # Run Elevation Gain
            ]

            # get rid of any unicode chars in run name
            data[1] = data[1].encode('ascii', 'ignore')
            data[1] = data[1].decode()

            if self.isUniqueData(data):

                # append the date of when activity is being added to DB
                # had infuriating bug of doing this before checking isUniqueData, and always getting it wrong cause it would think a run wasnt the same based on when it as added
                data.append( date.today().strftime("%m/%d/%y") )

                self.write(data, printDebug)
                added += 1
                
        print("Done; added ", added, " runs.")

    # check if the data already exists in the db (is a duplicate)
    def isUniqueData(self, data):

        # if you're running script for the first time, the CSV probably doesnt exist, so its safe to say all entires are unique
        if (self.DB_EXISTS):
            csv_file = csv.reader(open(self.CSV_FILE_NAME, 'r'), delimiter=',')

            CHECKING_DEPTH = 200 # only the n most recent entries for if they're dupes of the current data

            index = 0

            for row in csv_file:

                if (index > self.NUM_DB_ENTRIES - CHECKING_DEPTH): # if index is of the CHECKING_DEPTH most recent db entries
                    if data == row[:-1] :   # if the activity we're trying to add is equal to all but the date of row
                        return False

                index += 1

            return True

        else:
            return True

    def write(self, data, printDebug = False):

        with open(self.CSV_FILE_NAME, mode = 'a') as runDB:
            dbWriter = csv.writer(runDB, delimiter = ',', lineterminator = '\n')

            dbWriter.writerow(data)

            if printDebug:
                print("wrote: ", data)

    def getRunners(self):
        # https://www.strava.com/api/v3/clubs/{id}/members?page=&per_page=
        return self.getResult( self.makeURL("clubs/" + self.CLUB_ID) )

    def getClubActivities(self, numActivities = 200):
        # https://www.strava.com/api/v3/clubs/{id}/activities?page=&per_page=

        # 200 is the most runs you can get from a single Strava API call
        MAX_RUNS_PER_PAGE = 200

        if (numActivities > MAX_RUNS_PER_PAGE) or (numActivities < 1) or ( not(isinstance(numActivities, int)) ):
            numActivities = MAX_RUNS_PER_PAGE
            print("invalid num of activities")

        URL = self.makeURL("clubs/" + self.CLUB_ID + "/activities?page=1&per_page=" + str(numActivities) + '&')

        return self.getResult(URL)

    #### program doesnt use these ####
    # doesn't like working
    def getRunnerStats(self, id):
        #/athletes/{id}/stats
        URL = self.makeURL("athletes/" + str(id) + "/stats?")
        results = self.getResult(URL)

    # also doesnt like working
    def getActivity(self, activityID):
        # https://www.strava.com/api/v3/activities/{id}?include_all_efforts=
        # doesnt work but doesnt throw error?
        URL = self.makeURL("activities/" + str(activityID) + '?')
        results = self.getResult(URL)