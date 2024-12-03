"""
Incomplete GUI for ease of use
"""
# built-in
import os.path
import sys
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog

# custom methods/classes
from conversions.conversions import convert_from_storage
from input import bill_entry, bill_list, remove_bill, reset_database, backup_database
from search.search import Search


def get_font_name():
    """
    Gets the default font of the system that tkinter is using
    :return: Dict a font object
    """
    return font.nametofont('TkDefaultFont').actual()


class GUI(tk.Tk):

    def __init__(self):
        """
        Instantiates the GUI base window, frames, and creates the menu for further interaction
        """
        super().__init__()
        self.title('Now I\'m a BILLiever')
        screen_dimensions = [self.winfo_screenwidth(), self.winfo_screenheight()]
        window_dimensions = [800, 400]
        self.left_frame = ttk.Frame(self, borderwidth=5, relief='ridge')
        self.left_frame.pack(side='left', fill='both', expand=False)
        self.right_frame = ttk.Frame(self, borderwidth=5, relief='ridge')
        self.right_frame.pack(side='right', fill='both', expand=True)
        self.geometry(f'{window_dimensions[0]}x{window_dimensions[1]}'
                      f'+{int(screen_dimensions[0]/2 - window_dimensions[0]/2)}'
                      f'+{int(screen_dimensions[1]/2 - window_dimensions[1]/2)}')

        self.menu()

    def menu(self):
        """
        Main menu displayed in the left_frame
        """
        ttk.Button(self.left_frame, text='Add Bill', command=self._bill_add).pack(side='top')
        ttk.Button(self.left_frame, text='List Bills', command=self._bill_list).pack(side='top')
        ttk.Button(self.left_frame, text='Search Bills', command=self._search).pack(side='top')
        ttk.Button(self.left_frame, text='Remove Bill', command=self._remove_bill).pack(side='top')
        ttk.Button(self.left_frame, text='Quit', command=self.__close).pack(side='bottom')
        ttk.Button(self.left_frame, text='Settings', command=self._settings).pack(side='bottom')

    def _bill_add(self):
        """
        Class helper method for adding a new bill
        """
        self.__clear_frame(self.right_frame)
        bill_name = tk.StringVar()
        bill_desc = tk.StringVar()
        bill_amt = tk.StringVar()
        bill_dd = tk.StringVar()
        # bill ID and user ID will be taken care of by the controller so the methods calling the DB arent exposed by the view
        ttk.Label(self.right_frame, text='Bill Name:').pack()
        ttk.Entry(self.right_frame, textvariable=bill_name).pack()
        ttk.Label(self.right_frame, text='Bill Description:').pack()
        ttk.Entry(self.right_frame, textvariable=bill_desc).pack()
        ttk.Label(self.right_frame, text='Bill Amount:').pack()
        ttk.Entry(self.right_frame, textvariable=bill_amt).pack()
        ttk.Label(self.right_frame, text='Due Date:').pack()
        ttk.Entry(self.right_frame, textvariable=bill_dd).pack()
        ttk.Button(self.right_frame, text='Add Bill',
                   command=lambda: self.__ba_helper(bill_name.get(), bill_desc.get(), bill_amt.get(), bill_dd.get())).pack()

    def __ba_helper(self, billname, billdesc, amount, billdd):
        newbill = (billname, billdesc, int(amount), billdd)
        if bill_entry(newbill):
            self.__clear_frame(self.right_frame)
            ttk.Label(self.right_frame, text='The bill has been added').pack()
            ttk.Button(self.right_frame, text='Return', command=self._bill_add).pack()

    def _bill_list(self):
        """
        Class helper method for fetching and displaying the bill data
        """
        self.__clear_frame(self.right_frame)
        bills = bill_list()
        self.__bill_table(bills, self.right_frame)

    def _search(self):
        """
        Class helper method containing the logic for displaying and choosing bill search functionality
        """
        self.__clear_frame(self.right_frame)
        self.search_options = ttk.Frame(self.right_frame)
        self.search_results = ttk.Frame(self.right_frame)
        self.search_options.pack(side='top', fill='both')
        self.search_results.pack(side='bottom', fill='both')
        ttk.Label(self.search_options, text='Search by:').pack(side='top', anchor='nw')
        ttk.Button(self.search_options, text='Date', command=self._search_date).pack(side='left', anchor='nw')
        ttk.Button(self.search_options, text='Name', command=self._search_name).pack(side='left', anchor='nw')
        ttk.Button(self.search_options, text='Bill ID', command=self._search_billid).pack(side='left', anchor='nw')

    def _search_date(self):
        """
        Class helper method for displaying search-by-date
        """
        if len(self.search_options.winfo_children()) > 4:
            self.__search_clear()
        date = tk.StringVar()
        ttk.Button(self.search_options, text='Search', command=lambda: self.__sd_helper(date.get())).pack(side='right',
                                                                                                          anchor='ne')
        ttk.Entry(self.search_options, textvariable=date).pack(side='right', anchor='ne', padx=5, pady=2)
        ttk.Label(self.search_options, text='Enter date (e.g. 2024-04-14):').pack(side='right', anchor='ne', pady=2)

    def __sd_helper(self, date):
        self.__clear_frame(self.search_results)
        query = Search()
        query.set_query(date)
        resp = query.search_date()
        bills = []
        for bill in resp:
            amount = format(convert_from_storage(bill[4]), '.2f')
            bills.append([bill[0], bill[2], amount, bill[5], bill[3]])
        self.__bill_table(bills, self.search_results)

    def _search_name(self):
        """
        Class helper method for displaying search-by-name
        """
        if len(self.search_options.winfo_children()) > 4:
            self.__search_clear()
        name = tk.StringVar()
        ttk.Button(self.search_options, text='Search', command=lambda: self.__sn_helper(name.get())).pack(side='right',
                                                                                                          anchor='ne')
        ttk.Entry(self.search_options, textvariable=name).pack(side='right', anchor='ne', padx=5, pady=2)
        ttk.Label(self.search_options, text='Enter the bill name:').pack(side='right', anchor='ne', pady=2)

    def __sn_helper(self, name):
        self.__clear_frame(self.search_results)
        query = Search()
        query.set_query(name)
        resp = query.search_name()
        bills = []
        for bill in resp:
            amount = format(convert_from_storage(bill[4]), '.2f')
            bills.append([bill[0], bill[2], amount, bill[5], bill[3]])
        self.__bill_table(bills, self.search_results)

    def _search_billid(self):
        """
        Class helper method for displaying search-by-bill ID
        """
        if len(self.search_options.winfo_children()) > 4:
            self.__search_clear()
        billid = tk.StringVar()
        ttk.Button(self.search_options, text='Search', command=lambda: self.__sid_helper(billid.get(), self.search_results)).pack(side='right',
                                                                                                          anchor='ne')
        ttk.Entry(self.search_options, textvariable=billid).pack(side='right', anchor='ne', padx=5, pady=2)
        ttk.Label(self.search_options, text='Enter the bill ID:').pack(side='right', anchor='ne', pady=2)

    def __sid_helper(self, billid, frame):
        self.__clear_frame(frame)
        query = Search()
        query.set_query(int(billid))
        resp = query.search_billID()
        bills = []
        amount = format(convert_from_storage(resp[0][4]), '.2f')
        bills.append([resp[0][0], resp[0][2], amount, resp[0][5], resp[0][3]])
        self.__bill_table(bills, frame)

    def __search_clear(self):
        """
        Clears out the last three added items to the search_options frame,
        which will always be the specific search entry/labels
        """
        for i in range(3):
            self.search_options.winfo_children()[-1].destroy()

    def _remove_bill(self):
        """
        Class helper method for displaying the remove bill section
        """
        self.__clear_frame(self.right_frame)
        ttk.Label(self.right_frame, text='Enter the ID of the bill to remove:').pack()
        billid = tk.StringVar()
        ttk.Entry(self.right_frame, textvariable=billid).pack()
        ttk.Button(self.right_frame,text='Search', command=lambda: self.__rb_helper(int(billid.get()))).pack()

    def __rb_helper(self, billid):
        self.__clear_frame(self.right_frame)
        query = Search()
        query.set_query(int(billid))
        resp = query.search_billID()
        if resp:
            bills = []
            amount = format(convert_from_storage(resp[0][4]), '.2f')
            bills.append([resp[0][0], resp[0][2], amount, resp[0][5], resp[0][3]])
            bill = (f'Bill ID: {resp[0][0]}\n'
                    f'Name: {resp[0][2]}\n'
                    f'Amount: {amount}\n'
                    f'Due Date: {resp[0][5]}\n'
                    f'Description: {resp[0][3]}')
            ttk.Label(self.right_frame, text=bill).pack()
            ttk.Label(self.right_frame, text='Delete this entry?').pack()
            ttk.Button(self.right_frame, text='Delete', command=lambda: self.__rb(billid)).pack()
            ttk.Button(self.right_frame, text='Cancel', command= self._remove_bill).pack()
        else:
            ttk.Label(self.right_frame, text='Entry does not exist').pack()
            ttk.Button(self.right_frame, text='Return', command=self._remove_bill).pack()

    def __rb(self, billid):
        remove_bill(billid)
        self.__clear_frame(self.right_frame)
        ttk.Label(self.right_frame, text='The bill has been deleted').pack()
        ttk.Button(self.right_frame, text='Return', command=self._remove_bill).pack()


    def _settings(self):
        """
        Class helper method for displaying the settings/options page
        """
        self.__clear_frame(self.right_frame)
        default_font = get_font_name()
        settings_header = ttk.Label(self.right_frame, text='Implementation Options')
        settings_header.config(font=font.Font(family=default_font['family'], size=11, underline=True, weight='bold'))
        settings_header.pack(side='top')
        # database reset option
        description_delete = ('Deletes and resets the database for testing purposes. Creates a new database pre-filled with test data.\n'
                       'Note: If you have any data you wish to keep, please create a backup of the database file first')
        title_label = ttk.Label(self.right_frame, text='Reset Database')
        title_label.config(font=font.Font(family=default_font['family'], size=10, weight='bold'))
        title_label.pack(side='top', anchor='nw')
        desc_label = ttk.Label(self.right_frame, text=description_delete)
        desc_label.pack(side='top', anchor='nw')
        ttk.Button(self.right_frame, text='Reset Database', command=self.__reset_db_confirm).pack(side='top', anchor='ne')
        # database backup option
        description_backup = 'Creates a backup of the current database file (if it exists) at a location of your choosing'
        backup_label = ttk.Label(self.right_frame, text='Database backup')
        backup_label.config(font=font.Font(family=default_font['family'], size=10, weight='bold'))
        backup_label.pack(side='top', anchor='nw')
        backup_desc_label = ttk.Label(self.right_frame, text=description_backup)
        backup_desc_label.pack(side='top', anchor='nw')
        ttk.Button(self.right_frame, text='Backup Database', command=self.__backup_db).pack(side='top', anchor='ne')

    def __reset_db_confirm(self):
        """
        'Private' method for resetting the database. Would really just exist for dev/impl ops
        """
        if messagebox.askquestion('Reset Database', 'You cannot undo this once it has been done.\n'
                                                    'Are you sure you want to reset the database?') == 'yes':
           if reset_database():
               messagebox.showinfo('Reset Database', 'The database has been reset')
        else:
            messagebox.showinfo('Reset Database', 'The database was not reset')

    def __backup_db(self):
        """
        'Private' method for backing up the current database. Would be unmanageable at larger database volumes
        but works fine for dev/impl purposes
        """
        messagebox.showinfo('Database Backup', 'Choose a location to place the database backup')
        save_dir = filedialog.askdirectory()
        if os.path.isfile(save_dir + '\\local.db'):
            answer = messagebox.askquestion('Database Backup', 'This location already has a database file\n'
                                                          'Are you sure you wish to overwrite it?')
            if answer == 'yes':
                if backup_database(save_dir):
                    messagebox.showinfo('Database Backup', 'Database backup successful')
            else:
                messagebox.showinfo('Database Backup', 'The database file was not copied')
        else:
            if backup_database(save_dir):
                messagebox.showinfo('Database Backup', 'Database backup successful')

    def __close(self):
        """
        'Private' method used to verify the user wants to quit the program
        """
        if messagebox.askquestion('Quit', 'Are you sure you want to quit?') == 'yes':
            sys.exit(0)

    def __clear_frame(self, frame):
        """
        'Private' method used for clearing the right frame when selecting different options
        """
        for widget in frame.winfo_children():
            widget.destroy()
        frame.grid_forget()

    def __bill_table(self, bills, frame):
        if not bills:
            no_results = ttk.Label(self.search_results, text='The search returned no results')
            no_results.config(font=font.Font(family=get_font_name()['family'], size=12, weight='bold'))
            no_results.pack(side='top', anchor='center')
        else:
            columns = ('bill_id', 'name', 'amt', 'due_date', 'desc')
            table = ttk.Treeview(frame, columns=columns, show='headings')
            table.column('bill_id', width=75)
            table.column('name', width=150)
            table.column('amt', width=75)
            table.column('due_date', width=100)
            table.column('desc', width=275)
            table.heading('bill_id', text='Bill ID')
            table.heading('name', text='Name')
            table.heading('amt', text='Amount')
            table.heading('due_date', text='Due Date')
            table.heading('desc', text='Description')
            for bill in bills:
                table.insert("", tk.END, values=(bill[0], bill[1], bill[2], bill[3], bill[4]))
            vsb = ttk.Scrollbar(frame, orient='vertical', command=table.yview)
            vsb.pack(side='right', fill='y')
            table.pack(side='right', fill='both', expand=True)
            table.configure(yscrollcommand=vsb.set)


if __name__ == '__main__':
    # instantiates the GUI object and starts the tkinter mainloop
    app = GUI()
    app.mainloop()