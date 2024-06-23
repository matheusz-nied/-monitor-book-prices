import os
import sqlite3

def get_db_connection():
    print("Running get_db_connection")
    print("__file__:", __file__)  # Print para depurar a variável __file__
    
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print("Path:", dir_path)
        
        db_path = os.path.join(dir_path, 'database.db')
        print("Database path:", db_path)
        
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file '{db_path}' not found.")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print("Connection:", conn)
        return conn
    
    except Exception as e:
        print("Error in get_db_connection:", e)
        raise


