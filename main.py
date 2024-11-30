"""
cmd line version of the program used for testing new functionality
Gets most of its functionality from input.py and search.py
"""
from input import bill_entry, bill_list, remove_bill
from search.search import Search
from conversions.conversions import convert_from_storage

import sys


def main():
    # when adding new functionality, both the options list and the input string must be updated
    options = [1, 2, 3, 4, 0]
    inp = int(input('Please select from the following options:\n'
                    + '1: Add a bill to track\n'
                    + '2: List all bills\n'
                    + '3: Search for a bill\n'
                    + '4: Remove a bill\n'
                    + '0: Exit Program\n'))
    # im pretty sure python has a switch statement now
    if inp not in options:
        # input validation
        print('please enter a valid choice')
    elif inp == 1:
        # enter a new bill
        bill_entry()
    elif inp == 2:
        # list all bills
        bill_list()
    elif inp == 3:
        # search for a bill
        search_options = [1,2,3,0]
        answer = -1
        search = Search()
        while answer != 0:
            answer = int(input('Search by:\n'
                               '1: Date\n'
                               '2: Name\n'
                               '3: Bill ID\n'
                               '0: Exit to main menu\n'))
            if answer not in search_options:
                print('Please enter a valid option')
            elif answer == 1:
                try:
                    search.set_query(input('Please enter the bill due date (YYYY-MM-DD): '))
                    results = search.search_date()
                    print(results)
                except ValueError as ve:
                    print(ve, '\n')
            elif answer == 2:
                search.set_query(input('Please enter the bill name: '))
                results = search.search_name()
                print(results)
            elif answer == 3:
                search.set_query(int(input('Please enter the bill ID: ')))
                results = search.search_billID()
                print(results)
    elif inp == 4:
        # delete a bill
        delete = int(input('Please enter the bill number to delete: '))
        remove_bill(delete)
    elif inp == 0:
        # exit the program
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    try:
        while True:
            main()
    except Exception as e:
        print('An error occurred in main:', e)
