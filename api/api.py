import requests
import os
from dotenv import load_dotenv

from utilities import Utilities

load_dotenv()

# 
# API-FOOTBAL METHODS
# 

def getRequestFromApi(query, write_to_local = True):
    """
    Query the BASE_URL for the specifc endpoint

    Args: 
        query(dict) : endpoint to query
        write_to_local(boolean) : should the file be written to local (default = True)

    Returns: 
        dict : response data in a dictionary
    """
    
    headers = {
        'x-rapidapi-key': os.getenv('API_KEY'),
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    data = {}
    url = os.getenv('BASE_URL') + query['endpoint'] + query['params']
    
    response = requests.request("GET", url, headers = headers, data = data)

    if response.status_code != 200: 
        return 'An error has occured!'
    
    if write_to_local:
        Utilities.writeDataToFile(response.text, f"{query['endpoint']}.txt")
    
    return response.json()

def getFixturesForDate(date, get_new_data = False):
    """
    Get fixtures for a specific date

    Args:
        date(str) : date for fixtures in string format matching YYYY-MM-DD
        get_new_data(bool) : force query for new data from data-api
    
    Returns:
        dict : a dictionary of fixtures
    """
    request = None
    
    if get_new_data | Utilities.checkForCurrentDate(date):
        query = {
            'endpoint': 'fixtures',
            'params': '?league=39&season=2023&date=' + date
        }
        request = getRequestFromApi(query)
    else: 
        request = Utilities.readDataFromFile('fixtures.txt')
    
    print(type(request))
    print(request)

getFixturesForDate('2023-08-19')