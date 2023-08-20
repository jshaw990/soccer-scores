import os
import requests
from dotenv import load_dotenv

load_dotenv()

def getRequestFromApi(endpoint):
    """
    Query the BASE_URL for the specifc endpoint

    Args: 
        endpoint(str) : endpoint to query

    Returns: 
        dict : response data in a dictionary
    """
    
    headers = {
        'x-rapidapi-key': os.getenv('API_KEY'),
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    data = {}
    url = os.getenv('BASE_URL') + endpoint
    
    response = requests.request("GET", url, headers=headers, data=data)

    if (response.status_code != 200): 
        return 'An error has occured!'
    
    return response.json()

def getFixturesForDate(date):
    """
    Get fixtures for a specific date

    Args:
        date(str) : date for fixtures in string format matching YYYY-MM-DD
    
    Returns:
        dict : a dictionary of fixtures
    """

    endpoint = 'fixtures?league=39&season=2023&date=' + date
    request = getRequestFromApi(endpoint)
    
    print(type(request))
    print(request)

getFixturesForDate('2023-08-19')