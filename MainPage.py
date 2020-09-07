from tkinter import *
from tkinter import messagebox
import os
import sys
from tkinter import ttk

import mysql.connector
from mysql.connector import Error

py=sys.executable

#creating window
class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg='gray')
        self.canvas = Canvas(width=1366, height=768, bg='gray')
        self.canvas.pack()
        self.maxsize(1320, 768)
        self.minsize(1320,768)
        self.state('zoomed')
        self.title('LIBRARY MANAGEMENT SYSTEMS')
        self.a = StringVar()
        self.b = StringVar()
        self.mymenu = Menu(self)
        #calling scripts
        def a_s():
            os.system('%s %s' % (py, 'Add_Student.py'))

        def a_b():
            os.system('%s %s' % (py, 'Add_Books.py'))

        def r_b():
            os.system('%s %s' % (py, 'remove_book.py'))

        def r_s():
            os.system('%s %s' % (py, 'Remove_student.py'))

        def ib():
            os.system('%s %s' % (py, 'BarrowBook.py'))

        def ret():
            os.system('%s %s' % (py, 'AddBook.py'))

        def sea():
            os.system('%s %s' % (py,'Search.py'))

        def log():
            conf = messagebox.askyesno("Confirm", "Are you sure you want to Logout?")
            if conf:
                self.destroy()
                os.system('%s %s' % (py, 'Main.py'))



        # def handle(event):
        #     if self.listTree.identify_region(event.x,event.y) == "separator":
        #         return "break"
        def add_user():
            os.system('%s %s' % (py, 'Reg.py'))
        def rem_user():
            os.system('%s %s' % (py, 'Rem.py'))
        def sest():
            os.system('%s %s' % (py,'DeleteBook.py'))

        #creating table

        self.listTree = ttk.Treeview(self,height=14,columns=('TC','Title','ISBN', 'Author', 'Issue Date', 'Return Date'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set,xscrollcommand=self.hsb.set)
        self.listTree.heading("TC", text='TC')
        self.listTree.column("TC", width=100,minwidth=100,anchor='center')
        self.listTree.heading("Title", text='Title')
        self.listTree.column("Title", width=200, minwidth=200,anchor='center')
        self.listTree.heading("ISBN", text='ISBN')
        self.listTree.column("ISBN", width=125, minwidth=125,anchor='center')
        self.listTree.heading("Author", text='Author')
        self.listTree.column("Author", width=125, minwidth=125, anchor='center')
        self.listTree.heading("Issue Date", text='Issue Date')
        self.listTree.column("Issue Date", width=125, minwidth=125, anchor='center')
        self.listTree.heading("Return Date", text='Return Date')
        self.listTree.column("Return Date", width=125, minwidth=125, anchor='center')

        self.listTree.place(x=90,y=360)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))

        list1 = Menu(self)
        list1.add_command(label="Student", command=a_s)
        list1.add_command(label="Book", command=a_b)

        list3 = Menu(self)
        list3.add_command(label = "Add User",command = add_user)
        list3.add_command(label = "Remove User",command = rem_user)


        self.mymenu.add_cascade(label='Add', menu=list1)
        self.mymenu.add_cascade(label = 'Admin Tools', menu = list3)

        self.config(menu=self.mymenu)

        def ser():
            if(len(self.studid.get())==0):
                messagebox.showinfo("Error", "Empty Field!")
            else:
                conn = mysql.connector.connect(host='localhost',
                                               database='library',
                                               user='root',
                                               password='')
                cursor = conn.cursor()
                searched = self.studid.get()
                cursor.execute('Select * from `borrowed_books` where TC= %s ', (searched,))
                pc = cursor.fetchall()
                print(pc)
                if pc:
                   self.listTree.delete(*self.listTree.get_children())
                   for row in pc:
                       self.listTree.insert("",'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))


        def check():

            conn = mysql.connector.connect(host='localhost',
                                           database='library',
                                           user='root',
                                           password='')
            mycursor = conn.cursor()
            mycursor.execute("Select * from admin")
            z = mycursor.fetchone()
            if not z:
                messagebox.showinfo("Error", "Please Register A user")
                x = messagebox.askyesno("Confirm","Do you want to register a user")
                if x:
                    self.destroy()
                    os.system('%s %s' % (py, 'Reg.py'))
            else:
                #label and input box
                self.label3 = Label(self, text='LIBRARY MANAGEMENT SYSTEM',fg='black',bg="gray" ,font=('Courier new', 30, 'bold'))
                self.label3.place(x=350, y=22)
                self.label4 = Label(self, text="Enter your ID number",bg="gray", font=('Courier new', 18, 'bold'))
                self.label4.place(x=130, y=107)
                self.studid = Entry(self, textvariable=self.a, width=90)
                self.studid.place(x=405, y=110)
                self.srt = Button(self, text='Search', width=15, font=('arial', 10),command = ser).place(x=1000, y=106)
                self.label5 = Label(self, text="ENTER THE BOOK ID",bg="gray", font=('Courier new', 18, 'bold'))
                self.label5.place(x=75, y=150)
                self.bookid = Entry(self, textvariable=self.b, width=90)
                self.bookid.place(x=405, y=160)
                self.label6 = Label(self, text="INFORMATION DETAILS",bg="gray",  font=('Courier new', 15, 'underline', 'bold'))
                self.label6.place(x=560, y=300)
                self.button = Button(self, text='Delete A Book', width=25, font=('Courier new', 10), command=sest).place(x=240,y=250)
                self.button = Button(self, text='Search Book', width=25, font=('Courier new', 10), command=sea).place(x=520,y=250)
                self.brt = Button(self, text="Issue Book", width=15, font=('Courier new', 10), command=ib).place(x=800, y=250)
                self.brt = Button(self, text="Add A Book ", width=15, font=('Courier new', 10), command=ret).place(x=1000, y=250)
                self.brt = Button(self, text="LOGOUT", width=15,bg="red", font=('Courier new', 10), command=log).place(x=1150, y=105)

        check()

MainWin().mainloop()
