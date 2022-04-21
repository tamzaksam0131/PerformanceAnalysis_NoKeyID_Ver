import sqlite3
import numpy as np
import matplotlib
matplotlib.use ('TKAgg')
import matplotlib.pyplot as plt
import yaml
from prettytable import from_db_cursor

def sql_graph_output():

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)
    sql_sentence = 'SELECT'+ ' ' +'DRBD_Type, blocksize, '+ a['Select_Data']+' '+'FROM'+' '+a['Table_Names'] +' '+'WHERE'+' '+ 'Readwrite_type =' + a['ReadWrite_Type'] + ' ' + 'AND' + ' ' + 'Number_of_Job =' + a['Number_of_Job'] + 'AND' + ' '+ 'IOdepth =' + a['IOdepth']
    sql_result = cur.execute(sql_sentence)
    
    # for row in sql_result:
    #     print (row)

    # blocksize_range = ['1k', '2k','4k','8k','16k','32k','64k','128k','256k','512k','1M','2M']
    
    values = []
    drbd = []
    all_blocksize = []
    
    for row in sql_result:
        values.append(row[2])
        all_blocksize.append(row[1])
        drbd.append(row[0])
    print (values)
    # print (drbd_type)
    # print (all_blocksize)
    blocksize_range = list(set(all_blocksize))
    blocksize_range.sort(key=all_blocksize.index)
    # print (blocksize_range)

    
    number_of_drbd = len(values) // len(blocksize_range)
    # print (number_of_drbd)
    
    values2 = []
    drbd_type = []
    for i in range(number_of_drbd):
        values2.append(values[:len(blocksize_range)])
        values = values[len(blocksize_range):]
        drbd_type.append(drbd[len(blocksize_range)*i])
    print (values2)

    plt.figure(figsize=(20,20), dpi = 100)
    plt.xlabel ('Block Size')
    plt.ylabel (a['Select_Data'])
    # plt.ylabel (f'{Select_Data}')
    
    for j in range(number_of_drbd):
        x = blocksize_range
        y = values2[j]
        plt.plot(x,y, label = drbd_type[j])
    
    plt.title(a['Table_Names'] + '-' + a['Select_Data'] + '-' + a['ReadWrite_Type'])
    # plt.title(f"{Table_Names}-{ReadWrite_Type}-{Select_Data}")
    plt.legend()
    plt.grid()

    file_name = a['Table_Names'] + '-' + a['ReadWrite_Type'] + '-' + a['Select_Data'] + ' ' + 'chart'
    # plt.savefig(file_name)
    plt.show()
    
    cur.close()
    con.commit()
    con.close()

def sql_print_drbd():

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)
    
    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    sql_sentence = 'SELECT DRBD_Type From' + ' ' + a['Table_Names_rw']
    data = cur.execute(sql_sentence)

    for row in set(data):
        print (row[0])

    cur.close()
    con.commit()
    con.close()

def sql_graph_output_rw():

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object


    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    drbd = input ("Please enter the drbd type:")

    sql_sentence = 'SELECT'+ ' ' +'Readwrite_type, blocksize, '+ a['Select_Data_rw']+' '+'FROM'+' '+a['Table_Names_rw'] +' '+'WHERE'+' '+ 'DRBD_type =' + '"'+ drbd + '"' + ' ' + 'AND' + ' ' + 'Number_of_Job =' + a['Number_of_Job_rw'] + 'AND' + ' '+ 'IOdepth =' + a['IOdepth_rw']
    sql_result = cur.execute(sql_sentence)
    
    values = []
    readwrite = []
    all_blocksize = []
    
    for row in sql_result:
        values.append(row[2])
        all_blocksize.append(row[1])
        readwrite.append(row[0])
    # print (values)
    # print (drbd_type)
    # print (all_blocksize)
    blocksize_range = list(set(all_blocksize))
    blocksize_range.sort(key=all_blocksize.index)
    # print (blocksize_range)

    
    number = len(values) // len(blocksize_range)
    # print (number_of_drbd)
    
    values2 = []
    readwrite_type = []
    for i in range(number):
        values2.append(values[:len(blocksize_range)])
        values = values[len(blocksize_range):]
        readwrite_type.append(readwrite[len(blocksize_range)*i])
    print (values2)

    plt.figure(figsize=(20,20), dpi = 100)
    plt.xlabel ('Block Size')
    plt.ylabel (a['Select_Data'])
    # plt.ylabel (f'{Select_Data}')
    
    for j in range(number):
        x = blocksize_range
        y = values2[j]
        plt.plot(x,y, label = readwrite_type[j])
    
    plt.title(a['Table_Names_rw'] + '-' + a['Select_Data_rw'] + '-' + drbd)
    # plt.title(f"{Table_Names}-{ReadWrite_Type}-{Select_Data}")
    plt.legend()
    plt.grid()

    file_name = a['Table_Names_rw'] + '-' + drbd + '-' + a['Select_Data_rw'] + ' ' + 'chart'
    # plt.savefig(file_name)
    plt.show()
    
    cur.close()
    con.commit()
    con.close()


if __name__ == '__main__':
    sql_graph_output()
    sql_print_drbd()
    sql_graph_output_rw()