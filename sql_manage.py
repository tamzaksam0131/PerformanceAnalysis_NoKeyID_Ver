import sqlite3
from prettytable.prettytable import from_db_cursor
from matplotlib.pyplot import table

TABLE_NAME = ''

def drop_table():
    drop = input('Please Enter the name of the table you want to delete:')
    
    global TABLE_NAME
    TABLE_NAME = drop

    while drop == 'Index_Table':
        print ('Index Table could not be delected')
        drop = input('Please Enter the name of the table you want to delete:')
        
    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    sql_sentence_table = f'DROP TABLE {drop}'
    # sql_sentence_row = f'DELECT FROM Index_Table WHERE Text_Table_Name = {drop}'
    
    cur.execute(sql_sentence_table)
    # cur.execute(sql_sentence_row)

    cur.close()
    con.commit()
    con.close()

def drop_row(): 
    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object
    
    sql_sentence_row = f'DELETE FROM Index_Table WHERE Text_Table_Name = "{TABLE_NAME}"'
    cur.execute(sql_sentence_row)
    
    cur.execute('SELECT * from Index_Table')
    # column_list = []
    # for column in data.description:
    #     column_list.append(column[0])
    # print(column_list)
    
    # for row in data:
    #     print (row)
    x = from_db_cursor(cur)
    print (x)

    cur.close()
    con.commit()
    con.close()

if __name__ == '__main__':
    drop_table()
    drop_row()