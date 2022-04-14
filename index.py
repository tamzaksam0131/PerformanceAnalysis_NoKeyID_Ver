import sqlite3
from prettytable.prettytable import from_db_cursor

def sql_print_index():
    
    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    cur.execute('SELECT * From Index_Table')
        
    x = from_db_cursor(cur)
    print (x)

    cur.close()
    con.commit()
    con.close()

if __name__ == '__main__':
    sql_print_index()