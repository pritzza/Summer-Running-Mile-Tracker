from APIRetriever import APIRetriever
from DatabaseMaintainer import DatabaseMaintainer

def main():

    DB_FILE_NAME = "XC DB.csv"
    PRINT_DEBUG_INFO = True

    retriever = APIRetriever()

    retriever.requestNewAccessToken(PRINT_DEBUG_INFO)

    dbScript = DatabaseMaintainer(retriever.getClubID(), DB_FILE_NAME, retriever.getAccessToken())

    activities = dbScript.getClubActivities()

    dbScript.updateDatabase(activities, PRINT_DEBUG_INFO)

main()