"""
A json parser used for resetting the database mostly. jparser and jparser_multi were originally just used to create the
database when running json_testing.py (which has since been deleted), but have been appropriated for use with
resetting and repopulating the test db

wont get a test suite because its mostly just a helper method for test databases and shouldnt see regular usage
"""
import json
import os
from threading import Thread, Lock

from sqlite_db.db import Database
from conversions.conversions import convert_for_storage


def jparser(jfile):
    """takes in a json file that has been opened and loaded previously, parses it, and adds it to the local database.
  Handles only a single bill, for a single user

  Args:
      jfile (json file): an opened and loaded json file
  """
    # TODO: change out user_id field when user accounts are implemented
    db = Database()
    bills = {
        'id': jfile['id'],
        'name': jfile['name'],
        'description': jfile['description'],
        'amount': convert_for_storage(jfile['amount']),
        'due_date': jfile['due_date'],
        'user_id': 1
    }
    db.insert_bill(bills)
    db.close()


def jparser_multi(jfile):
    """takes in a json file that has been opened and loaded previously,
  parses it, and adds it to the local database. handles json files with multiple bills
  for a single user

  Args:
      jfile (json file): an opened and loaded json file
  """
    # TODO: change out user_id field when user accounts are implemented

    # opens the local database connection and returns the relevant objects
    db = Database()

    # instantiates an empty dict object
    bills = {}
    # goes through each bill within the loaded json file, assigns it out,
    # and attempts to insert it into the local db
    for bill in jfile["bills"]:
        bills[bill['id']] = {
            'id': bill['id'],
            'name': bill['name'],
            'description': bill['description'],
            'amount': convert_for_storage(bill['amount']),
            'due_date': bill['due_date'],
            'user_id': 1
        }
        db.insert_bill(bills[bill['id']])
    db.close()


def db_test_data():
    """
    repopulates a newly created database with test data.
    :return:
    """
    try:
        lock = Lock()
        # testing multi bill json input
        here = os.path.dirname(os.path.abspath(__file__))
        json_input = here + '\\test.json'

        with open(json_input) as file:
            parsed_input = json.load(file)

        # input the multi-bill json
        jpm_thread = Thread(target=jparser_multi(parsed_input), args=(lock,))
        jpm_thread.start()
        # not sure if these join statements are needed, as it performs the same when they are commented out,
        # but because they cause the program to wait until the thread finishes, i'll keep them there for good measure
        jpm_thread.join()

        # testing single bill json input
        jsingle_input = here + '\\test_single.json'

        with open(jsingle_input) as file:
            parsed_input = json.load(file)

        # threading is necessary to prevent race conditions
        # as we are currently perform multiple write operations to a single database
        jp_thread = Thread(target=jparser(parsed_input), args=(lock,))
        jp_thread.start()
        jp_thread.join()
        return True
    except Exception as e:
        print('error in db_test_data:', e)