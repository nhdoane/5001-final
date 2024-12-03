"""
Probably not needed honestly. it just turns things into floats or makes them not floats
"""
import unittest
import conversions.conversions as cv

class TestConversions(unittest.TestCase):

    def setUp(self):
        self.amt1 = 10.00
        self.amt2 = 100.00
        self.amt3 = 10
        self.amt4 = 100

    def testCForS(self):
        self.assertEqual(cv.convert_for_storage(self.amt1), 1000)
        self.assertEqual(cv.convert_for_storage(self.amt2), 10000)
        self.assertEqual(cv.convert_for_storage(self.amt3), 1000)
        self.assertEqual(cv.convert_for_storage(self.amt4), 10000)

    def testCFromS(self):
        self.assertEqual(cv.convert_from_storage(1000), self.amt1)
        self.assertEqual(cv.convert_from_storage(10000), self.amt2)
