import pymysql

def sql_test():
    
    # a_yaml_file = open('sql_config.yml')
    # a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    con = pymysql.connect (host='localhost',
                     user='testuser',
                     password='test123',
                     database='TESTDB') # create connection object and database file
    
    cur = con.cursor() # create a cursor for connection object

    sql_sentence = "SELECT VERSION()"
    print (sql_sentence)

    data = cur.fetchone(sql_sentence)
    
    print("Databaes Version is: %s" % data)

    cur.close()
    con.commit()
    con.close()

if __name__ == '__main__':
    sql_test()