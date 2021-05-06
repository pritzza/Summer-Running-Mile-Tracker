import csv

# db initially only stored runs, but was expanded to also include the other types of strava supported activities
# the purpose of this class is to take the old db format and convert it to a new one
class DatabaseRunConverter:

    def __init__(self, csvName):
        self.OLD_CSV_FILE_NAME = csvName
        self.NEW_CSV_FILE_NAME = "new" + csvName

    def convertDatabase(self):

        newDBFile = open(self.NEW_CSV_FILE_NAME, 'w')
        newDBFile.close()

        with open(self.OLD_CSV_FILE_NAME) as oldDB:
            dbReader = csv.reader(oldDB, delimiter = ',')

            with open(self.NEW_CSV_FILE_NAME, 'w') as newDB:
                dbWriter = csv.writer(newDB, delimiter = ',', lineterminator = '\n')

                for row in dbReader:

                    row[5] = row[6]
                    dbWriter.writerow(row[:-1])

                    #### STUPID ####    
                    # if 6th column starts with a digit (meaning its a date and not an activity)
                    #if row[5] [0].isdigit():
                        
                        # turn 6th column into a "Run" activity type and put activity date as 7th column
                        #date = row[5]
                        #row[5] = "Run"

                        #row.append(date)

                        #dbWriter.writerow(row)

        newDB.close()
        oldDB.close()
