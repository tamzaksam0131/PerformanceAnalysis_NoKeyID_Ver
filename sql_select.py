import sqlite3
import csv
from prettytable.prettytable import from_db_cursor
import yaml

def sql_analysis_output():

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    for i in range(len(a['table'])):

        sql_sentence = 'SELECT' + ' ' +  a['wanted data'] + ' ' + 'From' + ' ' + a['table'][i]+' '+'where'+' '+a['statement']
        # print (sql_sentence)
    
        cur.execute(sql_sentence)
        
        x = from_db_cursor(cur)

        print (a['table'][i])
        print (x)
    

        Excel_filename = input ('Please Enter the name of the Excel file will be created:')
        
        cur.execute(sql_sentence)
        with open(f"{Excel_filename}.csv","w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="\t")
            csv_writer.writerow([i[0] for i in cur.description])
            csv_writer.writerows(cur)

    cur.close()
    con.commit()
    con.close()

def sql_analysis_output_2():

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object
    
    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)
    sql_sentence = 'SELECT'+' '+a['wanted data1']+' '+'FROM'+' '+a['table1'] +' '+'where'+' '+a['statement1'] +' '+ 'UNION ALL' + ' ' + 'SELECT'+' '+a['wanted data2']+' '+'from'+' '+a['table2'] +' '+'where'+' '+a['statement2']
   
    cur.execute((sql_sentence))
    
    x = from_db_cursor(cur)
    print(x)

    excel_filename = input ('Please Enter the name of the Excel file will be created:')
    
    cur.execute(sql_sentence)
    with open(f"{excel_filename}.csv","w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)

    cur.close()
    con.commit()
    con.close()

if __name__ == '__main__':
    sql_analysis_output()
    sql_analysis_output_2()