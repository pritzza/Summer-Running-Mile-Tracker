# Summer-Running-Mile-Tracker
Python script to track strava miles.

# Set-up:
Create a csv file called ``API Data.csv`` in the same directory as the executable and enter your: ``Strava Club ID, Client ID, Access Token, Refresh Token, and Client Secret`` into its last row. 

# Usage:
Using the data in ``API Data.csv`` to make Strava API calls, the program will generate and maintain a second csv file called ``XC DB.csv``. With each execution of the program, it will log all of the runs of the 200 most recent club activities. Each row in the ``XC DB.csv`` will serve as a run from your club and will include in the columns the: ``Athlete Name, Run Name, Run Distance(meters), Run Duration(seconds), Run Elevation(meters), Run Date(mm/dd/yy)``.

# To-do:
  - Add add stuff to process the data inside ``XC DB.csv``
  - Make tables or something to store ordered rows of ``XC DB.csv``
