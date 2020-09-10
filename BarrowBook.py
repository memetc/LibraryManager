from datetime import date, datetime
import datetime as dt
from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import os
import sys

py = sys.executable


# creating window
class issue(Tk):
    def __init__(self):
        super().__init__()
        self.title('Library Admisintration')
        self.maxsize(440, 300)

        self.canvas = Canvas(width=1366, height=768, bg='gray')
        self.canvas.pack()
        c = StringVar()
        d = StringVar()

        # verifying input
        def isb():
            if (len(c.get())) == 0:
                messagebox.showinfo('Error', 'Empty field!')
            elif (len(d.get())) == 0:
                messagebox.showinfo('Error', 'Empty field!')
            else:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='library',
                                                        user='root',
                                                        password='')
                    book = c.get()
                    stud = d.get()
                    self.mycursor = self.conn.cursor()
                    number_of_books = 0
                    number_of_books = self.mycursor.callproc('GetBorrowedBooks', (stud, number_of_books))
                    print(number_of_books[1])

                    if  number_of_books[1] ==  8:
                        messagebox.showinfo('Error', 'You cannot borrow more books')
                        self.destroy()

                    self.mycursor.execute("Select * from books where availability = 'YES' and ISBN = %s",(book,))
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        book_row = self.pc[0]
                        print("success")
                        now = datetime.now()
                        twoweeks = dt.timedelta(days=14)
                        idate = now.strftime('%Y-%m-%d %H:%M:%S')
                        rdate = now.strptime(idate, '%Y-%m-%d %H:%M:%S') + twoweeks
                        self.mycursor.execute("Insert into borrowed_books(TC, title, ISBN, author, issue_date, return_date) values (%s,%s,%s,%s,%s,%s)",(stud,book_row[0],book_row[2], book_row[1], idate, rdate))
                        self.conn.commit()
                        self.mycursor.execute("Update books set availability = 'NO' where ISBN = %s", (book,))
                        self.conn.commit()
                        messagebox.showinfo("Success", "Successfully Issue!")
                        print("books borrowed: ", int(self.mycursor.callproc('GetBorrowedBooks', (stud,))))
                        ask = messagebox.askyesno("Confirm", "Do you want to add another?")
                        if ask:
                            self.destroy()
                            os.system('%s %s' % (py, 'BarrowBook.py'))
                        else:
                            self.destroy()
                    else:
                        messagebox.showinfo("Oop's", "Book id " + c.get() + " is not available")

        # label and input box
        Label(self, text='Book Issuing', bg='gray', font=('Courier new', 24)).place(x=135, y=40)
        Label(self, text='Book ID:', bg='gray', font=('Courier new', 15), fg='black').place(x=55, y=100)
        Entry(self, textvariable=c, width=40).place(x=160, y=106)
        Label(self, text='Student ID:', bg='gray', font=('Courier new', 15), fg='black').place(x=20, y=150)
        Entry(self, textvariable=d, width=40).place(x=160, y=158)
        Button(self, text="ISSUE", width=20, command=isb).place(x=200, y=200)


issue().mainloop()