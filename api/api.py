import requests
import os
from dotenv import load_dotenv

from utilities import Utilities
from database import MongoConnection

load_dotenv()

# 
# API-FOOTBAL METHODS
# 

def get_request_from_football(query, write_to_db = True, write_to_local = True):
    """
    Query the FOOTBALL_URL for the specifc endpoint

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
    url = os.getenv('FOOTBALL_URL') + query['endpoint'] + query['params']
    
    response = requests.request("GET", url, headers = headers, data = data)

    print(response.text)

    if response.status_code != 200: 
        return 'An error has occured!'
    
    if write_to_db: 
        MongoConnection.write_to_db(response.json()['response'], collection = query['endpoint'])
    
    if write_to_local:
        Utilities.write_data_to_file(response.text, f"{query['endpoint']}.txt")
    
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
    
    if get_new_data | Utilities.check_for_current_date(date):
        query = {
            'endpoint': 'fixtures',
            'params': f'?league=39&season=2023&date={date}'
        }
        request = get_request_from_football(query)
    else: 
        # request = Utilities.readDataFromFile('fixtures.txt')
        # MongoConnection.write_to_db(request['response'], collection = 'fixtures')
        request = MongoConnection.get_collection_from_db('fixtures')
    
    print(f'Number of fixtures for date {date}: {len(request)}')

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
        request = get_request_from_football(query)
        
    else: 
        # request = Utilities.readDataFromFile('teams.txt')
        # MongoConnection.write_to_db(request['response'], collection = 'team')
        request = MongoConnection.get_collection_from_db('team')
    
    print(f'Number of teams in league {league}: {len(request)}')

# getFixturesForDate('2023-08-18')
# getTeamsForLeague(39)

def write_FixturesToDb():
    request = Utilities.readDataFromFile('fixtures.txt')
    MongoConnection.write_to_db(request['response'], collection = 'fixtures')

def get_leagues_and_write():
    query = {
            'endpoint': 'leagues',
            'params': ''
        }
    
    request = get_request_from_football(query)

# write_FixturesToDb()
get_leagues_and_write()