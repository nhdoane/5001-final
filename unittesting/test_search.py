"""
Testing suite for the Search class and its methods
"""
import unittest

from search.search import Search


class TestSearch(unittest.TestCase):

    def setUp(self):
        # instantiates a class search object, as well as some built in queries to test with
        self.search = Search()
        self.query1 = 'internet'
        self.query2 = 'more than one word'
        self.query3 = 'A much fuller string compared to the others'
        self.query4 = '2024 - 11 - 15'
        self.query5 = 25
        self.floatQuery = 20.4

    def testSetQuery(self):
        # verify it instantiates emtpy
        self.assertEqual(self.search.query, '')
        # pass the queries and make sure they all set properly
        self.search.set_query(self.query1)
        self.assertEqual(self.search.query, self.query1)
        self.search.set_query(self.query2)
        self.assertEqual(self.search.query, self.query2)
        self.search.set_query(self.query3)
        self.assertEqual(self.search.query, self.query3)
        self.search.set_query(self.query4)
        self.assertEqual(self.search.query, self.query4)
        self.search.set_query(self.query5)
        self.assertEqual(self.search.query, self.query5)

    def testSearchDate(self):
        # this should just literally look for any int between 0-9999
        # if empty, it returns the full list
        # if given a float or str, it correctly says nothing was found
        self.search.set_query(self.query4)
        # should pull three entries from the test database
        self.assertTrue(len(self.search.search_date()) == 3)
        self.search.set_query('24')
        # should pull all but one entry from the test database
        self.assertTrue(len(self.search.search_date()) == 13)
        # should only pull 1 from the test database
        self.search.set_query('01')
        self.assertTrue(len(self.search.search_date()) == 3)
        # testing some non-digit strings and floats. They should both just return nothing with no errors
        self.search.set_query(self.query1)
        self.assertTrue(len(self.search.search_date()) == 0)
        self.search.set_query(self.floatQuery)
        with self.assertRaises(TypeError):
            self.search.search_date()

    def testSearchName(self):
        # should return 4 items
        self.search.set_query('ll')
        self.assertTrue(len(self.search.search_name()) == 4)
        # should return one item
        self.search.set_query(self.query1)
        self.assertTrue(len(self.search.search_name()) == 1)
        # all should return 0
        self.search.set_query(self.query4)
        self.assertTrue(len(self.search.search_name()) == 0)
        # raises a type error if given something other than a string
        self.search.set_query(self.floatQuery)
        with self.assertRaises(TypeError):
            self.search.search_name()

    def testSearchId(self):
        # these should all only ever return 1
        self.search.set_query(1)
        self.assertTrue(len(self.search.search_billID()) == 1)
        self.search.set_query(2)
        self.assertTrue(len(self.search.search_billID()) == 1)
        self.search.set_query(3)
        self.assertTrue(len(self.search.search_billID()) == 1)
        self.search.set_query(4)
        self.assertTrue(len(self.search.search_billID()) == 1)
        self.search.set_query(5)
        self.assertTrue(len(self.search.search_billID()) == 1)
        # raises a typeerror if given not an int
        with self.assertRaises(TypeError):
            self.search.set_query(self.query1)
            self.search.search_billID()
        with self.assertRaises(TypeError):
            self.search.set_query(self.floatQuery)
            self.search.search_billID()
