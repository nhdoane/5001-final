"""
Handles input from the cmd line and provides most of the base functionality for main.py
Also provides methods for the GUI
"""
from threading import Thread, Lock
from tkinter import messagebox
import re

from requests.packages import target

from json_parsers.jparser import db_test_data
from sqlite_db.db import Database
from conversions.conversions import convert_for_storage, convert_from_storage


def bill_entry():
    # init vars
    user_id = 1
    name = ''
    desc = ''
    amt = -1
    due_date = -1
    db = Database()

    # get next bill_id to use
    bill_id = db.get_next_bill_id(user_id)

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

    # send them away to the local database
    lock = Lock()
    bill_add_thread = Thread(target=db.insert_bill(bill), args=(lock,))
    bill_add_thread.start()
    bill_add_thread.join()
    db.close()


def bill_list():
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
    return data


def remove_bill(bill_id: int):
    db = Database()
    result = db.remove_bill(bill_id)
    return result


def reset_database():
    try:
        db = Database(object_only=True)
        db.reset_db()
    except FileNotFoundError as fnf:
        messagebox.showinfo('File not found:', str(fnf))
    db_test_data()


def backup_database(save_dir):
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
    db = Database()
    print(db.get_next_bill_id(1))
    db.close()
