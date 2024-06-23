import os
import sqlite3
dir_path = os.path.dirname(os.path.realpath(__file__))

connection = sqlite3.connect(dir_path + '/database.db')


with open(dir_path + '/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

url_to_insert = "https://www.amazon.com.br/gp/product/8595070644/ref=ox_sc_saved_image_5?smid=A1ZZFT5FULY4LN&psc=1"
cur.execute("INSERT INTO books (url) VALUES (?)", (url_to_insert,))



connection.commit()
connection.close()