import sqlite3
import numpy as np
import matplotlib as mpl
from prettytable.prettytable import from_db_cursor
mpl.use ('TKAgg')
import matplotlib.pyplot as plt
import yaml

def sql_graph_output():

    con = sqlite3.connect ('sqldatabase_test.db') # create connection object and database file
    cur = con.cursor() # create a cursor for connection object
    
    a_yaml_file = open('sql_config.yml')
    a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    text_table = []
    drbd = []
    values = []

    for i in range(len(a['Table_hist'])):
        sql_sentence = 'SELECT Text_Table_Name, DRBD_Type,' + ' ' + a['Select_Data_hist'] + ' ' + 'FROM Index_table,' +  a['Table_hist'][i] \
                + ' ' + 'WHERE Readwrite_type = ' + a['Readwrite_hist']\
                + ' ' + 'AND Number_of_Job = ' + a['Number_of_Job_hist']\
                + ' ' + 'AND IOdepth = ' + a['IOdepth_hist']\
                + ' ' + 'AND blocksize = ' + a['Blocksize_hist']\
                + ' ' + 'AND Index_table.Text_Table_Name =' + ' ' + a['Table_hist'][i] + '.table_name' \
    

        sql_result = cur.execute(sql_sentence)
    
        for row in sql_result:
            text_table.append(row[0])
            drbd.append(row[1])
            values.append(row[2])
            print(row)

    print (sql_sentence)
    print (text_table)    
    print (values)
    print (drbd)

    
    plt.figure(figsize=(20,20), dpi = 100)
    bar_width = 0.3

    for i in range(len(drbd)):
        x_data = drbd[i]
        # print (x_data)
        y_data = values[i]
        # print (y_data)
        plt.bar(x_data, y_data, label = text_table[i], width = bar_width)
        
    plt.xlabel ('DRBD Type')
    plt.ylabel (a['Select_Data_hist'])
    plt.xticks (rotation = 30)
    
    for x,y in zip(drbd,values):
        plt.text(x, y+0.05, '%.2f' % y, ha = 'center', va = 'bottom', fontsize = 11)

    plt.title(a['Select_Data_hist'] + ' ' + 'under Different DRBD Type (Readwrite type = ' + a['Readwrite_hist'] + ', Blockszie =' + a['Blocksize_hist'] + ')')
    plt.legend()
    plt.grid()
    
    # for i in range(len(a['Table_hist'])):
    #     plt.savefig(a['Table_hist'][i]- a['Select_Data_hist'].png)
    # plt.savefig(a['Table_Name_2hist_1']-a['Table_Name_2hist_1']-a['Select_Data_2hist'].png)
    plt.show()

    cur.close()
    con.commit()
    con.close()

if __name__ == '__main__':
    sql_graph_output()