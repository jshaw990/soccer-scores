from utilities import Utilities
from database import MongoConnection
from football_api import FootballApi

def get_fixtures_for_date(date, get_new_data = False):
    """
    Get fixtures for a specific date

    Args:
        date(str) : date for fixtures in string format matching YYYY-MM-DD
        get_new_data(bool) : force query for new data from data-api
    
    Returns:
        dict : a dictionary of fixtures
    """
    response = None
    
    if get_new_data | Utilities.check_for_current_date(date):
        query = {
            'endpoint': 'fixtures',
            'params': f'?league=39&season=2023&date={date}'
        }
        response = FootballApi.get_request(query)
    else: 
        response = MongoConnection.get_collection_from_db('fixtures')
    
    print(f'Number of fixtures for date {date}: {len(response)}')
    return response

def getTeamsForLeague(league, get_new_data = False):
    """
    Get teams for a specific league

    Args:
        get_new_data(bool) : force query for new data from data-api
    
    Returns:
        dict : a dictionary of teams
    """
    response = None
    
    if get_new_data:
        query = {
            'endpoint': 'teams',
            'params': f'?league={league}&season=2023'
        }
        response = FootballApi.get_request(query)
        
    else: 
        response = MongoConnection.get_collection_from_db('team')
    
    print(f'Number of teams in league {league}: {len(response)}')
    return response

def get_league_table(get_new_data = False):
    response = None

    if get_new_data:
        query = {
            'endpoint': 'standings',
            'params': f'?league=39&season=2023'
        }
        response = FootballApi.get_request(query)

    else:
        response = MongoConnection.get_collection_from_db('table')

    return response

get_league_table(True)

def write_FixturesToDb():
    request = Utilities.read_data_from_file('fixtures.txt')
    MongoConnection.write_to_db(request['response'], collection = 'fixtures')

def get_leagues_and_write():
    query = {
            'endpoint': 'leagues',
            'params': ''
        }
    
    response = FootballApi.get_request(query)
