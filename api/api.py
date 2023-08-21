import requests
import os
from dotenv import load_dotenv

from utilities import Utilities
from database import DatabaseConnection

load_dotenv()

# 
# API-FOOTBAL METHODS
# 

def getRequestFromApi(query, write_to_db = True, write_to_local = True):
    """
    Query the BASE_URL for the specifc endpoint

    Args: 
        query(dict) : endpoint to query
        write_to_local(boolean) : should the file be written to local (default = True)
        write_to_local(boolean) : should the file be written to local (default = True)

    Returns: 
        dict : response data in a dictionary
    """
    
    headers = {
        'x-rapidapi-key': os.getenv('FOOTBALL_API_KEY'),
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    data = {}
    url = os.getenv('BASE_URL') + query['endpoint'] + query['params']
    
    response = requests.request("GET", url, headers = headers, data = data)

    print(response.text)

    if response.status_code != 200: 
        return 'An error has occured!'
    
    # if write_to_db: 
    #     DatabaseConnection.write_to_db(response.json()['response'], collection = query['endpoint'])
    
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
        DatabaseConnection.write_to_db(request['response'], collection = 'fixtures')
    
    print(type(request))
    print(request)

def getTeamsForLeague(league, get_new_data = False):
    """
    Get teams for a specific league

    Args:
        get_new_data(bool) : force query for new data from data-api
    
    Returns:
        dict : a dictionary of teams
    """
    request = None
    
    if get_new_data:
        query = {
            'endpoint': 'teams',
            'params': f'?league={league}&season=2023'
        }
        request = getRequestFromApi(query)
        
    else: 
        request = Utilities.readDataFromFile('teams.txt')
        DatabaseConnection.write_to_db(request['response'], collection = 'team')
    
    print(type(request))
    print(request)

getFixturesForDate('2023-08-19', True)
getTeamsForLeague(39)