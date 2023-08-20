from datetime import datetime
import json

# 
# UTILITY METHODS
# 

def checkForCurrentDate(date_string):
    current_date = datetime.now().strftime('%Y-%m-%d')

    if date_string == current_date: 
        return True
    elif date_string < current_date:
        return False
    else:
        return None

def readDataFromFile(file_name = 'data.txt'):
    """
    Read data from the file_name provided and return it in a dictionary

    Args: 
        file_name(str) : file name to be returned

    Returns: 
        dict: file's data in a dictionary
    """
    
    file = open(f'data/{file_name}', 'r')
    return json.loads(file.read())

def writeDataToFile(data, file_name = 'data.txt'):
    """
    Write provided data to a text file

    Args: 
        data(str) : data to be written to the file
        file_name(str) : file name for the created file (default = 'data.txt')
    """

    file = open(f'data/{file_name}', 'w')
    file.write(data)
    file.close()
