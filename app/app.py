import asyncio
from threading import Thread
from time import sleep
from uu import Error
from service.verifyPrice import verifyPrice
from database.database import get_db_connection
from flask import Flask, render_template, request, flash, redirect, url_for,Response
from werkzeug.exceptions import abort
import sqlite3
from service.scraping import get_book_data
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['STATIC_FOLDER'] = 'static'

@app.route('/')
def index(): 
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/<int:book_id>')
def book(book_id):
    book = get_book(book_id)
    return render_template('book-detail.html', book=book)

@app.route('/create', methods=('GET', 'POST'))
async def create():
    api_key = os.getenv("SECRET_KEY")

    try:        
        if request.method == 'POST':
            url = request.form['url']
            secret_key = request.form['secret-key']

            if secret_key != api_key:
                flash('Wrong secret key!')
                return render_template('create.html')
            if not url:
                flash('Title is required!')
            else:
                conn = get_db_connection()
                cursor = conn.execute('INSERT INTO books (url) VALUES (?)', (url,))
                conn.commit()
                book_id = cursor.lastrowid
                scraping_thread = Thread(target=asyncio.run, args=(create_book(book_id),))
                scraping_thread.daemon = True 
                scraping_thread.start()
                conn.close()
                return redirect(url_for('index'))
        return render_template('create.html')    
    except Exception as error:
        print(error)
        flash('Some error ha ocurred!: ', error)
        return render_template('create.html')

@app.route('/<int:id>', methods=('GET', 'POST'))
def edit(id):
    book = get_book(id)
    api_key = os.getenv("SECRET_KEY")

    if request.method == 'POST':
        url = request.form['url']
        secret_key = request.form['secret-key']
        print(secret_key, api_key)

        if secret_key != api_key:
            flash('Wrong secret key!')
            return render_template('book-detail.html', book=book)
        if not url:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE books SET url = ?'
                         ' WHERE id = ?',
                         (url, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('book-detail.html', book=book)

@app.route('/book/delete/<int:id>', methods=('POST',))
def delete(id):
    api_key = os.getenv("SECRET_KEY")
    book = get_book(id)

    try:
        secret_key = request.get_json()['secret_key']
        if secret_key != api_key:
            flash('Wrong secret key!')
            return Response(status=401)
    except Exception as error:
            flash('Wrong secret key!')
            return Response(status=401)
    if request.method == 'POST':
        if secret_key == api_key:
            secret_key = request.get_json()['secret_key']

            conn = get_db_connection()
            conn.execute('DELETE FROM books WHERE id = ?', (id,))
            conn.commit()
            conn.close()

            flash('"{}" was successfully deleted!'.format(book['name']))
            return redirect(url_for('index'))
    return render_template('index.html', book=book)

async def create_book(book_id):
    print("Dentro do create_book")
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    updated_book = await get_book_data(book['url'])
    conn.execute('UPDATE books SET url = ? , name = ?, url_image = ?, author = ?, price = ? WHERE id = ?', (updated_book.url, updated_book.name, updated_book.url_image, updated_book.author, updated_book.price, book['id']))
    conn.commit()
    conn.close()

def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    return book
def run_scraping():
    print("Running scraping")
    asyncio.run(background_scraping())

def background_scraping():
    print( 'running background_scraping ' )

    while True:
        try:

            print( 'running while ' )
            conn = get_db_connection()
            print( 'running get_db_connection ' )

            books = conn.execute('SELECT * FROM books').fetchall()
            print( 'running thread scraping in ', len(books), ' books' )
            for book in books:
                updated_book = asyncio.run(get_book_data(book['url']))
                conn.execute('UPDATE books SET url = ? , name = ?, url_image = ?, author = ?, price = ? WHERE id = ?',
                            (updated_book.url, updated_book.name, updated_book.url_image, updated_book.author, updated_book.price, book['id']))
                conn.commit()
                verifyPrice(book, updated_book)
            conn.close()
            print("Sleeping")
            sleep(1)  

        except Exception as error:
            print(error)
        finally:
            conn.close

scraping_thread = Thread(target=run_scraping)
scraping_thread.daemon = True 
scraping_thread.start()
print("Ja devia ter startado")

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print("Error in the app:", e)
