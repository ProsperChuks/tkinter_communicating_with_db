# __Finished and Compiled by Prosper Chuks on
# __06/4/2018

from tkinter import *
from tkinter import ttk
import sqlite3

class record():

    #Success or Error Message
    global message

    #Database Name
    db_name = 'database.db'

    #Building the GUI
    def __init__(self, master):

        self.master = master
        self.master.title('Student Info')
        # self.master.iconbitmap(r'C:\Users\Prosper\AppData\Local\Programs\Python\Python36-32\DLLs\logo.ico')
        self.master.resizable(False, False)
        self.master.geometry('720x500')

        frame = Frame(master).pack()

        Label(frame, text='Name').pack()
        self.name = Entry(frame)
        self.name.pack()

        Label(frame, text='Exam Number').pack()
        self.num = Entry(frame)
        self.num.pack()

        self.run = Button(frame, text='Add Record', command=self.add,
                          relief=GROOVE, width=10, height=1)
        self.run.pack()

        self.message = Label(frame, text='', fg='red')
        self.message.pack()

        self.tree = ttk.Treeview(height=10, column=2)
        self.tree.pack()
        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading(2, text='Exam Number', anchor=W)

        self.run2 = Button(frame, text='Delete Record', command=self.delete,
                          relief=GROOVE, width=10, height=1)
        self.run2.pack()

        self.but = Button(frame, text='Exit', command = master.destroy,
               relief=GROOVE, width=10, height=1)
        self.but.pack()

        # self.run3 = Button(frame, text='Edit Record', command=self.edit,
        #                   relief=GROOVE, width=10, height=1)
        # self.run3.pack()

        self.view_records()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def view_records(self):
        records = self.tree.get_children()
        for elements in records:
            self.tree.delete(elements)
        query = 'SELECT * FROM login_details ORDER BY examNumber DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    def validate(self):

        return len (self.name.get()) != 0 and len (self.num.get())


    def add(self):
        
        if self.validate():
            query = 'INSERT INTO login_details VALUES (NULL, ?, ?)'
            parameters = (self.name.get(), self.num.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Record added Successfully {0}'.format(self.name.get())
            self.name.delete(0, END)
            self.num.delete(0, END)
        else:
            self.message['text'] = 'No Record Inserted'
        self.view_records()


    def delete(self):

        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a record to delete'
            return

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM login_details WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record Deleted Successfully {0}'.format(name)
        self.view_records()

    # def edit(self):
    #     self.message['text'] = ''
    #     try:
    #         self.tree.item (self.tree.selection())['values'][0]
    #     except IndexError as e:
    #         self.message['text'] = 'Select a record to edit'
    #         return
        
    #     name = self.tree.item(self.tree.selection())['text']
    #     old_data = self.tree.item(self.tree.selection())['values'][0]

    #     self.new = Toplevel()
    #     self.new.title('Edit Data')
    #     self.new.geometry('300x250')
    #     self.new.iconbitmap(r'C:\Users\Prosper\AppData\Local\Programs\Python\Python36-32\DLLs\logo.ico')

    #     Label(self.new, text='Old Name:').pack()
    #     Entry(self.new, textvariable=StringVar(self.new, value=name), state='readonly').pack()
    #     Label(self.new, text='New Name').pack()
    #     new_name = Entry(self.new).pack()

    #     Label(self.new, text='Old Number:').pack()
    #     Entry(self.new, textvariable=StringVar(self.new, value=old_data), state='readonly').pack()
    #     Label(self.new, text='New Number').pack()
    #     new_num = Entry(self.new).pack()

    #     Button(self.new, text='save changes', command = lambda: self.edit_records(new_name, name, new_num, old_data),
    #            relief=GROOVE, width=10, height=1).pack()

    #     self.new.mainloop()

    # def edit_records(self, new_name, name, new_num, old_data):
    #     query = "UPDATE login_details SET name = ? examNumber = ?, WHERE name = ?"
    #     parameters = (new_name, name, new_num, old_data)
    #     self.run_query(query, parameters)
    #     self.new.destroy()
    #     self.message['text'] = 'Changes Made!'.format(name)
    #     self.view_records()



if __name__=='__main__':
    master = Tk()
    app = record(master)
    master.mainloop()
