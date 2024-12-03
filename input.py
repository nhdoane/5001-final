"""
Handles input from the cmd line and provides most of the base functionality for main.py
Also provides methods for the GUI
"""
from threading import Thread, Lock
from tkinter import messagebox
import re

from json_parsers.jparser import db_test_data
from sqlite_db.db import Database
from conversions.conversions import convert_for_storage, convert_from_storage


def bill_entry(newbill = ()):
    """
    opens a connection to the database, collects relevant bill information, and passes that information to the database.
    """
    # init vars
    user_id = 1
    name = ''
    desc = ''
    amt = -1
    due_date = -1
    db = Database()

    # get next bill_id to use
    bill_id = db.get_next_bill_id(user_id)

    if newbill:
        amt = newbill[2]
        print(amt)
        bill = {
            'id': bill_id,
            'user_id': user_id,
            'name': newbill[0],
            'description': newbill[1],
            'amount': convert_for_storage(amt),
            'due_date': newbill[3]
        }
    else:
        # get bill name
        while name == '':
            try:
                # ph is placeholder
                ph_name = input('Please enter the bill name: ')
                if ph_name.isdigit():
                    print('Please enter a string')
                else:
                    name = ph_name
            except Exception as e:
                print('Error: ', e)

        # get bill desc
        while desc == '':
            try:
                desc = input('Please enter a bill description: ')
            except Exception as e:
                print('Error: ', e)

        # get bill amount
        while amt == -1:
            try:
                ph_amt = input('Enter bill amount: ')
                if ph_amt.isalpha():
                    print('Cannot be a string')
                else:
                    amt = float(ph_amt)
            except Exception as e:
                print('Error: ', e)

        # get due_date
        while due_date == -1:
            try:
                ph_dd = input('enter a date in the format YYYY-MM-DD: ')
                if re.fullmatch(r"\d{4}-[0-1]?[1-9]-[0-3]?[0-9]", ph_dd):
                    due_date = ph_dd
                else:
                    print('Please enter the date in the requested format')
            except Exception as e:
                print('Error: ', e)

        # assign them out to a dict
        bill = {
            'id': bill_id,
            'user_id': user_id,
            'name': name,
            'description': desc,
            'amount': convert_for_storage(amt),
            'due_date': due_date
        }

    try:
        # send them away to the local database
        lock = Lock()
        bill_add_thread = Thread(target=db.insert_bill(bill), args=(lock,))
        bill_add_thread.start()
        bill_add_thread.join()
        db.close()
        return True
    except Exception as e:
        print('An error occurred in bill entry:', e)


def bill_list():
    """
    Opens a db connection and pulls a list of all bills associated with a user ID.
    Appends those bills to a list that follows a specific format that makes it easier to pull data for the GUI
    :return: list A list of bills with minor formatting changes
    """
    db = Database()
    bills = db.return_all_bills(1)
    # header = ['Bill ID', 'Name', 'Amount', 'Due Date', 'Description']
    data = []
    for bill in bills:
        # A bill in order is:
        # [0]bill_id: int
        # [1]user_id: int
        # [2]name: str
        # [3]desc: str
        # [4]amt: comes back as int, after convert_from_storage its a float
        # [5]due_date: str
        amount = format(convert_from_storage(bill[4]), '.2f')
        data.append([bill[0], bill[2], amount, bill[5], bill[3]])
    # print(tabulate(data, headers=header, tablefmt='grid', floatfmt='.2f'))
    db.close()
    return data


def remove_bill(bill_id: int):
    """
    Opens the database and deletes the bill with the corresponding bill ID
    :param bill_id: int the unique ID of the bill to be deleted
    :return: Nothing, at the moment
    """
    db = Database()
    result = db.remove_bill(bill_id)
    db.close()
    return result


def reset_database():
    """
    create an empty database object and initiates the database reset procedure.
    Throws an error if the file is not found during the deletion stage
    :return:
        returns True if the database was reset and the data was successfully added
    """
    try:
        db = Database(object_only=True)
        db.reset_db()
    except FileNotFoundError as fnf:
        messagebox.showinfo('File not found:', str(fnf))
    return db_test_data()


def backup_database(save_dir):
    """

    :param save_dir: string The string representation of the directory path to store a copy of the database to
    :return:
        returns True if the backup was successful
    """
    try:
        lock = Lock()
        db = Database(object_only=True)
        backup = Thread(target=db.backup_db(save_dir), args=(lock,))
        backup.start()
        backup.join()
        return True
    except FileNotFoundError as fnf:
        messagebox.showinfo('File not found:', str(fnf))


def test():
    """
    Test function that just opens a db connection and tries to pull the next unique bill ID, which is the max bill + 1
    literally only used this for testing certain db connection functions. deprecated since i have other methods
    successfully connecting to the database to test with
    """
    db = Database()
    print(db.get_next_bill_id(1))
    db.close()
