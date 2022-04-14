import sqlite3
from sqlite3.dbapi2 import ProgrammingError
import numpy as np
import matplotlib as mpl
mpl.use ('TKAgg')
import matplotlib.pyplot as plt
import yaml

STANDARD_VALUES = []
LONG_STANDARD_VALUES = []
EXAMPLE_VALUES = []
RATIO_PER = []

# value = ""
# Standard_table_name = ""
STANDARD_DRBD = ""
# Standard_readwrite_Type = ""
# Standard_blocksize = ""
# Example_table_name = ""
EXAMPLE_DRBD = ""
# Example_readwrite_Type = ""

def sql_print_standard_drbd():

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)
    
    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    SQL_sentence = 'SELECT DRBD_Type From' + ' ' + a['Table_Name_devi_1']
    data = cur.execute(SQL_sentence)

    # for column in data.description:
    #     print(column[0],end=" ")
    
    # print()
    for row in set(data):
        print (row[0])
        # print (type(row))

    cur.close()
    con.commit()
    con.close()

def sql_pick_standard_values():

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    drbd_type_1 = input ('Please Enter the drbd type(Standard):')
 
    global STANDARD_DRBD
    STANDARD_DRBD = drbd_type_1

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)
    SQL_Sentence = 'SELECT' + ' ' + a['Standard_Value'] + ' ' + 'From' + ' ' + a['Table_Name_devi_1'] \
                + ' ' + 'WHERE Readwrite_type = ' + ' ' + a['ReadWrite_Type_Stan'] \
                + ' ' + 'AND DRBD_Type = ' + ' ' + '"' + drbd_type_1 + '"' \
                + ' ' + 'AND blocksize = ' + ' ' + a['Blocksize_Stan']    
    sql_result_1 = cur.execute(SQL_Sentence)
    for row in sql_result_1:
        # print (row)
        STANDARD_VALUES.append(row[0])
    print (STANDARD_VALUES)

    cur.close()
    con.commit()
    con.close()

def sql_print_example_drbd():

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    sql_sentence = 'SELECT DRBD_Type From' + ' ' + a['Table_Name_devi_2']
    data = cur.execute(sql_sentence)

    # for column in data.description:
    #     print(column[0],end=" ")
    
    # print()
    for row in set(data):
        print (row[0])

    cur.close()
    con.commit()
    con.close()

def sql_pick_example_values():
    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object

    # value_2 = input('Please Enter the Compared value you want(IOPS / MBPS):')
    # Table_Names_2 = input ('Please Enter the Text Table Name(Compared):')
    # Readwrite_Type_2 = input ('Please Enter the readwrite type(Compared):')
    drbd_type_2 = input ('Please Enter the drbd type(Compared):')

    # global Example_table_name
    # Example_table_name = Table_Names_2
    # global Example_readwrite_Type
    # Example_readwrite_Type = Readwrite_Type_2
    global EXAMPLE_DRBD
    EXAMPLE_DRBD = drbd_type_2

    # sql_result_2 = cur.execute(rf'SELECT {value_2} From {Table_Names_2} WHERE Readwrite_type = "{Readwrite_Type_2}" AND DRBD_Type = "{DRBD_Type_2}"')
    # # sql_result_2 = cur.execute('SELECT IOPS From Guangzhou_20210924_RAM WHERE Readwrite_type = "write" AND DRBD_Type = "drbd1002"')

    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)
    sql_sentence = 'SELECT' + ' ' + a['Example_Value'] + ' ' + 'From' + ' ' + a['Table_Name_devi_2'] \
                + ' ' + 'WHERE Readwrite_type = ' + ' ' + a['ReadWrite_Type_Ex'] \
                + ' ' + 'AND DRBD_Type = ' + ' ' + '"' + drbd_type_2 + '"'
    
    sql_result_2 = cur.execute(sql_sentence)
    for row in sql_result_2:
        # print (row)
        EXAMPLE_VALUES.append(row[0])
    print (EXAMPLE_VALUES)

    cur.close()
    con.commit()
    con.close()

def draw():
    a_yaml_file = open('sql_config.yml')
    ayaml = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    LONG_STANDARD_VALUES = STANDARD_VALUES * 12
    diffence = [EXAMPLE_VALUES - LONG_STANDARD_VALUES for EXAMPLE_VALUES, LONG_STANDARD_VALUES in zip (EXAMPLE_VALUES, LONG_STANDARD_VALUES)]
    print (diffence)
    ratio = [diffence / LONG_STANDARD_VALUES for diffence, LONG_STANDARD_VALUES in zip (diffence, LONG_STANDARD_VALUES)]

    RATIO_PER = [round(i*100,2) for i in ratio]
    # print (ratio)
    print (RATIO_PER)

    blocksize_range = ['1k', '2k','4k','8k','16k','32k','64k','128k','256k','512k','1M','2M']
    
    plt.figure(figsize=(50,50), dpi = 100)
    bar_width = 0.3
    
    for i in range(len(blocksize_range)):
        # print (i)
        x_data = blocksize_range[i]
        # print (x_data)
        y_data = RATIO_PER[i]
        # print (y_data)
        plt.bar(x_data, y_data, width = bar_width)

    plt.xlabel ('Blocksize')
    plt.ylabel ('Rate of difference (Percentage)')
    plt.xticks (rotation = 30)
    for a,b in zip(blocksize_range,RATIO_PER):
        plt.text(a, b+0.05, '%.2f' % b, ha = 'center', va = 'bottom', fontsize = 11)
    
    plt.title(ayaml['Standard_Value'] + ' ' + 'difference(%)' + ' ' + ayaml['Table_Name_devi_1'] + '(' + STANDARD_DRBD +','+ayaml['ReadWrite_Type_Stan']+ ayaml['Blocksize_Stan'] + ')'+ ' ' + 'vs.' + ayaml['Table_Name_devi_2'] + '(' + EXAMPLE_DRBD +','+ayaml['ReadWrite_Type_Ex'] + ')')
    plt.grid()
    
    # file_name = ayaml['Standard_Value_1'] + ' ' + 'difference(%)' + ' ' + ayaml['Table_Name_devi_Stan'] + '(' + ayaml['DRBD_Type_1Stan']+','+ayaml['ReadWrite_Type_1Stan']+ ayaml['Blocksize_Stan'] + ')'+ ' ' + 'vs.' + ayaml['Table_Name_devi_Ex'] + '(' + ayaml['DRBD_Type_1Ex']+','+ayaml['ReadWrite_Type_1Ex'] + ')'
    # plt.savefig(file_name)
    plt.show()

if __name__ == '__main__':
    sql_print_standard_drbd()
    sql_pick_standard_values()
    sql_print_example_drbd()
    sql_pick_example_values()
    draw()