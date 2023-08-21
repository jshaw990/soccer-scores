from datetime import datetime
import json

class Utilities:
    """
    Utility methods
    """

    def check_for_current_date(date_string):
        """
        Check if provided date_string is today (True), 

        Returns:
            bool : if True - date is today, if False - date is in the past, if None - Date is in the future or invalid
        
        Raises:
            ValueError: Date is in the future
            Exception: Date is invalid
        """
        current_date = datetime.now().strftime('%Y-%m-%d')

        if date_string == current_date: 
            return True
        elif date_string < current_date:
            return False
        elif date_string > current_date:
            raise ValueError(f'Date cannot be in the future.')
        else:
            raise Exception(f'Date is not valid. Date provided: {date_string}')

    def readDataFromFile(file_name = 'data.txt'):
        """
        Read data from the file_name provided and return it in a dictionary

        Args: 
            file_name(str) : file name to be returned

        Returns: 
            dict: file's data in a dictionary
        """
        print(file_name)
        file = open(f'api/data/{file_name}', 'r')
        return json.loads(file.read())

    def write_data_to_file(data, file_name = 'data.txt'):
        """
        Write provided data to a text file

        Args: 
            data(str) : data to be written to the file
            file_name(str) : file name for the created file (default = 'data.txt')
        """

        file = open(f'api/data/{file_name}', 'w')
        file.write(data)
        file.close()