"""
Incomplete GUI for ease of use
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys

from input import bill_entry, bill_list, remove_bill
from search.search import Search


class GUI(tk.Tk):

    def __init__(self):
        """
        Instantiates the GUI base window
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

        self.landing_page()

    def landing_page(self):
        """
        Main menu displayed in the left_frame
        """
        ttk.Button(self.left_frame, text='Add Bill', command=self._bill_add).pack(side='top')
        ttk.Button(self.left_frame, text='List Bills', command=self._bill_list_table).pack(side='top')
        ttk.Button(self.left_frame, text='Search Bills', command=self._search).pack(side='top')
        ttk.Button(self.left_frame, text='Remove Bill', command=self._remove_bill).pack(side='top')
        ttk.Button(self.left_frame, text='Quit', command=self._close).pack(side='bottom')
        ttk.Button(self.left_frame, text='Settings', command=self._settings).pack(side='bottom')

    # TODO: need to finish this one too
    def _bill_add(self):
        """
        Class helper method for adding a new bill
        """
        self.__clear_frame()
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

    def _bill_list_table(self):
        """
        Class helper method for fetching and displaying the bill data
        """
        self.__clear_frame()
        bills = bill_list()
        columns = ('bill_id', 'name', 'amt', 'due_date', 'desc')
        table = ttk.Treeview(self.right_frame, columns=columns, show='headings')
        table.column('bill_id', width=75)
        table.column('name',width=150)
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
        vsb = ttk.Scrollbar(self.right_frame, orient='vertical', command=table.yview)
        vsb.pack(side='right', fill='y')
        table.pack(side='right', fill='both')
        table.configure(yscrollcommand=vsb.set)

    def _search(self):
        """
        Class helper method containing the logic for displaying bill search functionality
        """
        self.__clear_frame()
        ttk.Label(self.right_frame, text='Search by:').grid(column=1,row=0, sticky='W')
        ttk.Button(self.right_frame, text='Date').grid(column=1, row=1, sticky='W')
        ttk.Button(self.right_frame, text='Name').grid(column=1, row=2, sticky='W')
        ttk.Button(self.right_frame, text='Bill ID').grid(column=1, row=3, sticky='W')

    # TODO: search GUI needs to be completed
    def _search_date(self):
        pass

    def _search_name(self):
        pass

    def _search_billid(self):
        pass

    def _remove_bill(self):
        pass

    # TODO: Settings needs to be completed
    def _settings(self):
        pass

    def _close(self):
        """
        Class helper method used to verify the user wants to quit the program
        """
        if messagebox.askquestion('Quit', 'Are you sure you want to quit?') == 'yes':
            sys.exit(0)

    def __clear_frame(self):
        """
        'Private' method used for clearing the right frame
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.right_frame.grid_forget()


if __name__ == '__main__':
    app = GUI()
    app.mainloop()