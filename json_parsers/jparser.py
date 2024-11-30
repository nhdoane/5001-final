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
