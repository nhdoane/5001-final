"""
Handles the creation of sqlite search scripts based on the type of search being performed,
with a bit of static validation
"""
import re
from sqlite_db.db import Database


def _validate(query, caller):
    """
    Takes in the query and a value unique to the calling function,
    and validates the query against the type in the database.
    Will return either a boolean value, or will raise an exception to be handled by the calling function
    :param query: The search query to be validated against the search type
    :param caller: A unique string identifier used to specify the calling function
    :return: A boolean value based on whether the query can be used for the specified search
    """
    if caller == 's_d':
        # full date matching r"\d{4}-[0-1]?[1-9]-[0-3]?[0-9]"
        try:
            return re.search(r"\d{0,4}", query)
        except TypeError as te:
            return None
    elif caller == 's_n':
        if type(query) is not str:
            raise TypeError
        else:
            return True
    elif caller == 's_b':
        if type(query) is not int:
            raise TypeError
        else:
            return True


class Search:

    def __init__(self):
        """
        instantiates the class with a blank str to be searched.
        The one creating the object is responsible for using the correct search method
        """
        self.query = ''

    def set_query(self, query):
        """
        Sets the query attribute to the passed piece of data
        :param query: string/int the new value of the query attribute
        """
        self.query = query

    def search_date(self):
        """
        Used with a formatted date (YYYY-MM-DD), then runs validation using regex to ensure the date is properly formatted,
        and if it is, it creates a SQL query to be run against the database
        :return: A list containing all the items that fit the SQL query
        """
        # get rid of any whitespace in the date search, as it will only mess with the regex
        if not _validate(self.query, 's_d'):
            raise TypeError()
        else:
            self.query = self.query.replace(' ', '')
            self.set_query(f'%{self.query}%')
            script = ['SELECT * FROM bills WHERE due_date like ?;', (self.query,)]
            db = Database()
            resp = db.search_bill(script)
            db.close()
            return resp

    def search_name(self):
        """
        Used with a string. Searches the 'name' column of the database with the provided string.
        Will throw a TypeError if an incorrect type is passed for searching
        :return: A list containing all the items that fit the SQL query
        """
        result = None
        try:
            result = _validate(self.query, 's_n')
        except TypeError:
            raise TypeError
        if result:
            self.set_query(f'%{self.query}%')
            script = ['SELECT * FROM bills WHERE name LIKE ?;', (self.query,)]
            db = Database()
            resp = db.search_bill(script)
            db.close()
            return resp

    def search_billID(self):
        """
        Used with an int. Searches the bill_id column of the database with the provided int.
        Should throw TypeError if an incorrect type is used
        :return: a single bill matching the bill_id provided
        """
        result = None
        try:
            result = _validate(self.query, 's_b')
        except TypeError as te:
            raise TypeError
        if result:
            script = ['SELECT * FROM bills WHERE bill_id = ?;', (self.query,)]
            db = Database()
            resp = db.search_bill(script)
            db.close()
            return resp