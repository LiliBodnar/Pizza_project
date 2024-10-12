import MySQLdb

def connect():
    # Establish the database connection
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Happy_Unicorn312",
        db="PizzaProject"
    )

def execute_query(query, params=None):
    db = connect()
    cursor = db.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        db.commit()
    except MySQLdb.Error as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

def fetch_results(query, params=None):
    db = connect()
    cursor = db.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except MySQLdb.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        db.close()
