import requests
import os
from dotenv import load_dotenv

from utilities import Utilities
from database import MongoConnection

load_dotenv()

class FootballApi:
    def get_account_status():
        """
        Query the API-Football to print the status of the account and remaining daily queries
        """
        headers = {
            'x-rapidapi-key': os.getenv('FOOTBALL_API_KEY'),
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        url = os.getenv('FOOTBALL_URL') + 'status'
        
        response = requests.request("GET", url, headers = headers)

        if response.status_code != 200: 
            return 'An error has occured!'
        
        response = response.json()['response']

        if response['subscription']['active']:
            remaining = response['requests']['limit_day'] - response['requests']['current']

            print(f"The account for email: {response['account']['email']} has {remaining} requests remaining")

        print(f"The account for email: {response['account']['email']} is currently not active.")

    def get_request(query, write_to_db = True, write_to_local = True):
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

        url = os.getenv('FOOTBALL_URL') + query['endpoint'] + query['params']
        
        response = requests.request("GET", url, headers = headers)

        if response.status_code != 200: 
            return 'An error has occured!'
        
        if write_to_local:
            Utilities.write_data_to_file(response.text, f"{query['endpoint']}.txt")

        
        if write_to_db: 
            MongoConnection.write_to_db(response.json()['response'], collection = query['endpoint'])
        
        return response.json()