"""
unit testing for database class.
DOES NOT contain a test method for search_bill because
that method is pretty extensively tested by the search class and its unit testing
reset_db and backup_db will also not be tested due to how they are handled down the pipeline
"""
import unittest
from sqlite_db.db import Database
from sqlite3 import ProgrammingError

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.test_bill = {
            'id': 15,
            'user_id': 2,
            'name': 'test',
            'description': 'test bill',
            'amount': 120,
            'due_date': '2024-11-15'
        }

    def testGNBID(self):
        self.assertTrue(self.db.get_next_bill_id(1) == 15)
        # if the user doesnt exist (which none but 1 will right now), raise a typeerror
        with self.assertRaises(TypeError):
            self.db.get_next_bill_id(2)

    def testRAB(self):
        # this user should have bills, returned as a list
        resp = self.db.return_all_bills(1)
        self.assertIsNotNone(resp)
        self.assertIs(type(resp), list)
        # this user shouldnt have anything
        resp = self.db.return_all_bills(2)
        self.assertFalse(resp)
        self.assertIs(type(resp), list)

    def testInsertRemoveBill(self):
        # this test is for both adding and removing a bill
        # this way it helps keep the test db intact instead of having to remove things constantly
        self.db.insert_bill(self.test_bill)
        # make sure the bill was added properly
        self.assertTrue(len(self.db.return_all_bills(2)) == 1)
        self.db.remove_bill(15)
        # make sure the bill was removed properly
        self.assertTrue(len(self.db.return_all_bills(2)) == 0)

    def testClose(self):
        self.db.close()
        # it will raise both these exceptions due to the cursor object being closed and not callable
        # this signifies the database was closed properly
        with self.assertRaises(ProgrammingError) and self.assertRaises(TypeError):
            self.db.return_all_bills(1)