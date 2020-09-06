from tkinter import *
from tkinter import messagebox
import os
import mysql.connector
from mysql.connector import Error

py = sys.executable


# creating window
class Lib(Tk):
    def __init__(self):
        super().__init__()
        self.a = StringVar()
        self.b = StringVar()
        self.c = StringVar()
        self.maxsize(1200, 700)
        self.minsize(1200, 700)
        self.configure(bg="gray")
        self.title("Add A Book")

        # verifying input
        def chex():
            if len(self.book_title.get()) < 0:
                messagebox.showinfo(" INVALID USERNAME OR PASSWORD")
            elif len(self.author_name.get()) < 0:
                messagebox.showinfo(" INVALID USERNAME OR PASSWORD")
            else:

                conn = mysql.connector.connect(host='localhost',
                                               database='library',
                                               user='root',
                                               password='')
                cursor = conn.cursor()
                title = self.book_title.get()
                author = self.author_name.get()
                ISBN = self.isbn_code.get()
                cursor.execute("Insert into books(title,author,ISBN,is_borrowed) values (%s,%s,%s, 'No')", (title, author, ISBN))
                conn.commit()
                self.destroy()
                conn.close()




        def check():

            self.label = Label(self, text="Add A Book", bg='gray', fg='black', font=("courier-new", 24, 'bold'))
            self.label.place(x=550, y=90)
            self.label1 = Label(self, text="Title", bg='gray', fg='black', font=("courier-new", 18, 'bold'))
            self.label1.place(x=370, y=180)
            self.book_title = Entry(self, textvariable=self.a, width=45)
            self.book_title.place(x=480, y=190)
            self.label2 = Label(self, text="Author", bg='gray', fg='black', font=("courier-new", 18, 'bold'))
            self.label2.place(x=340, y=250)
            self.author_name = Entry(self, textvariable=self.b, width=45)
            self.author_name.place(x=480, y=255)

            self.label3 = Label(self, text="ISBN", bg='gray', fg='black', font=("courier-new", 18, 'bold'))
            self.label3.place(x=340, y=315)
            self.isbn_code = Entry(self, textvariable=self.c, width=45)
            self.isbn_code.place(x=480, y=320)

            self.butt = Button(self, text="Add", bg='white', font=10, width=8, command=chex).place(x=580, y=350)
            self.label4 = Label(self, text="LIBRARY MANAGEMENT SYSTEM", bg='gray', fg='black',font=("courier-new", 24, 'bold'))
            self.label4.place(x=350, y=30)

        check()


Lib().mainloop()
