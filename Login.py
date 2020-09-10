from datetime import date, datetime
import datetime as dt
import mysql.connector
from flask import Flask, render_template, redirect, url_for, request


conn = mysql.connector.connect(host='localhost',
                               database='library',
                               user='root',
                               password='')
cursor = conn.cursor()

app = Flask(__name__)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        if (request.form['books'] == 'Book Name'):
            cursor.execute("Select * from books where title LIKE %s", (keyword,))
            pc = cursor.fetchall()
        elif(request.form['books'] == 'Author Name'):
            cursor.execute("Select * from books where author LIKE %s", (keyword,))
            pc = cursor.fetchall()
        else:
            cursor.execute("Select * from books where ISBN LIKE %s", (keyword,))
            pc = cursor.fetchall()
        return render_template('list.html', data=pc)
    return render_template('SearchBook.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        ISBN = request.form['ISBN']
        cursor.execute("Insert into books(title,author,ISBN,availability) values (%s,%s,%s, 'Yes')",
                       (title, author, ISBN))
        conn.commit()
        return redirect(url_for('main'))

    return render_template('AddBook.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        ISBN = request.form['ISBN']
        cursor.execute("Delete from books where title= %s AND author = %s AND ISBN = %s", (title, author, ISBN))
        conn.commit()
        return redirect(url_for('main'))

    return render_template('DeleteBook.html')

@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if request.method == 'POST':
        id = request.form['id']
        isbn = request.form['ISBN']
        number_of_books = 0
        number_of_books = cursor.callproc('GetBorrowedBooks', (id, number_of_books))
        if number_of_books[1] == 8:
            return 'Cannot borrow more books!'

        cursor.execute("Select * from books where availability = 'Yes' and ISBN = %s", (isbn,))
        pc = cursor.fetchall()

        if pc:
            book_row = pc[0]
            now = datetime.now()
            twoweeks = dt.timedelta(days=14)
            idate = now.strftime('%Y-%m-%d %H:%M:%S')
            rdate = now.strptime(idate, '%Y-%m-%d %H:%M:%S') + twoweeks
            cursor.execute("Insert into borrowed_books(TC, title, ISBN, author, issue_date, return_date) values (%s,%s,%s,%s,%s,%s)",
                (id, book_row[0], book_row[2], book_row[1], idate, rdate))
            conn.commit()
            return redirect(url_for('main'))
        else:
            return 'Book is not available'
    return render_template('IssueBook.html')

@app.route('/return', methods=['GET', 'POST'])
def returnbook():
    if request.method == 'POST':
        isbn = request.form['ISBN']
        cursor.execute("Delete from borrowed_books where ISBN = %s", (isbn,))
        conn.commit()
        return redirect(url_for('main'))
    return render_template('ReturnBook.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        tc = request.form['tc']


        cursor.execute('Select * from borrowed_books where TC= %s ', (tc,))
        pc = cursor.fetchall()
        return render_template('list2.html', data=pc)
    return render_template('CheckStatus.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if (request.form['options'] == 'search'):
            return redirect(url_for('search'))
        elif (request.form['options'] == 'add'):
            return redirect(url_for('add'))
        elif (request.form['options'] == 'delete'):
            return redirect(url_for('delete'))
        elif (request.form['options'] == 'issue'):
            return redirect(url_for('issue'))
        elif (request.form['options'] == 'return'):
            return redirect(url_for('returnbook'))
        else:
            return redirect(url_for('check'))

    return render_template('MainPage.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        cursor.execute('Select * from `admin` where user= %s AND password = %s ', (user, password,))
        pc = cursor.fetchone()
        if pc:
            return redirect(url_for('main'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)








