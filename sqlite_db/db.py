"""
database class. creates/opens the database, and houses all the functions for interacting with the database
NOTE: error handling is incredibly generic and not best practice at the moment
"""
import sqlite3 as sql
import os


class Database:

    def __init__(self):
        """creates a local sqlite3 db (if it doesnt exist)
            and creates the 'bills' and 'users' tables (also if they dont exist)

        Returns:
            sqlite3.connection: a sqlite3 connection object, connected to the local db
            sqlite3.cursor: a sqlite3 cursor object, for posting and fetching data to and from the local db
        """
        # find the current location of this file, and create/open the database from here
        here = os.path.dirname(os.path.abspath(__file__))
        self.con = sql.connect(here + '\\local.db')
        self.cur = self.con.cursor()
        self.cur.executescript('CREATE TABLE IF NOT EXISTS users(user_id INTEGER NOT NULL PRIMARY KEY, \
                          username TEXT, \
                          password TEXT); \
                          ')
        self.con.commit()
        self.cur.executescript('CREATE TABLE IF NOT EXISTS bills(bill_id INTEGER NOT NULL PRIMARY KEY, \
                          user_id INTEGER, \
                          name TEXT, \
                          desc TEXT, \
                          amt INTEGER, \
                          due_date DATE); \
                          ')
        self.con.commit()

    def insert_bill(self, bills: dict):
        """inserts a bill into the database.
          Assumes you have an open connection to pass to the function.
          Has built-in error handling for sqlite issues.

        Args:
            bills (Dict): A dict of bills

        Returns:
            Returns a boolean value of True on successful insertion, and False if an exception occurred
        """
        try:
            # sqlite3 needs to be passed an iterable sequence when using qmark notation
            # named placeholders are deprecated since 3.12 and will raise an error in 3.14
            self.cur.execute(
                'INSERT INTO bills (bill_id,user_id,name,desc,amt,due_date) VALUES(:id,:user_id,:name,:description,:amount,:due_date)',
                bills)
            self.con.commit()
            print('Bill was added Successfully!')
        except Exception as e:
            raise e('Error in insert_bill: ', bills["id"])

    def get_next_bill_id(self, user_id: int):
        """Returns the next available bill ID in a user's stored data. Does not handle opening or closing a connection to the database.

        Args:
            user_id (int): the ID of the user

        Returns:
            resp + 1: The max bill_id in the user's data, incremented by one
        """
        # TODO: user_id in sql statement needs testing
        try:
            id = (user_id,)
            resp = self.cur.execute('SELECT MAX(bill_id) from bills WHERE user_id = ?;', id)
            resp = resp.fetchone()[0]
            return resp + 1
        except Exception as e:
            raise e('Error in get_next_bill_id')

    def return_all_bills(self, user_id: int):
        """
        Fetches all bills from the database associated with the specified user ID
        :param user_id: The ID of the user associated with the bills
        :return: All bills as a list. Will return an empty list if no bills are found associated with provided user ID
        """
        try:
            id = (user_id,)
            resp = self.cur.execute('SELECT * FROM bills WHERE user_id = ?;', id)
            resp = resp.fetchall()
            return resp
        except Exception as e:
            raise e('error in return_all_bills')

    def remove_bill(self, bill_id):
        """
        removes the selected bill from the database, selected by its bill ID
        :param bill_id: The ID of the bill to be deleted
        :return: Null
        """
        try:
            id = (bill_id,)
            self.cur.execute('DELETE FROM bills WHERE bill_id = ?', id)
            self.con.commit()
        except Exception as e:
            raise e('error in remove_bill')

    def search_bill(self, script):
        try:
            resp = self.cur.execute(script[0], script[1])
            return resp.fetchall()
        except Exception as e:
            raise e('Error in search_bill')

    def close(self):
        """
        Closes the database connection.
        I have issues calling this, even with threading and forcing the program to wait for the thread's return
        so I usually leave this to the automatic __del__ call
        """
        try:
            self.cur.close()
            self.con.close()
        except Exception as e:
            raise e('Error in close')
