import sqlite3

def handle_db_lock(database_name):
   try:
       connection = sqlite3.connect(database_name)
       cursor = connection.cursor()
       cursor.execute("SELECT 1")
       cursor.close()
       
   except sqlite3.OperationalError as e:
       print(f"OperationalError: {e}")
       if 'database is locked' in str(e):
           print("Database is locked. Trying to reconnect...")
           connection.close()
           time.sleep(5)
           handle_db_lock(database_name)
       else:
           raise e
       
   else:
       print("Successfully connected to the database.")
       connection.close()
