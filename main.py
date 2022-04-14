# coding: utf-8
import index as index
import sql_input as sqlin
import sql_select as sqlsel
import sql_chart as sqlchart
import sql_histogram as sqlhis
import sql_deviation as sqldevi
import sql_view as sqlview
import sql_manage as sqlman
import yaml
import sqlite3

# typein = input("(input/analysis/graph/deviation):")

def main():
    # a_yaml_file = open('sql_config.yml')
    # a = yaml.load(a_yaml_file, Loader = yaml.FullLoader)

    try:
        index.sql_print_index()
    except sqlite3.OperationalError:
        print("Please input FIO result text file name and other information in Yaml configuraion for input.py first AND THEN ENTER input in the next question")

    typein = input("What kind of function do you want to use? (view/input/analysis/graph/deviation/manage):")
    # typein = a['typein']
    if typein == "input":
        sqlin.inputfile()
        sqlin.handle_mbps()
        sqlin.handle_iops()
        sqlin.sql_index_input()
        sqlin.sql_text_input()
    
    elif typein == "analysis":
        index.sql_print_index()
        number_of_table = input("How many tables do you want to analyze with? (Enter: many / 2):")
        # number_of_table = a['number of table']
        if number_of_table  == "many":
            sqlsel.sql_analysis_output()
        if number_of_table  == "2":
            sqlsel.sql_analysis_output_2()
    
    elif typein == "graph":
        index.sql_print_index()
        graph = input("What kind of graph do you want to create? (Enter: chart / histogram):")
        if graph == "chart":
            kind = input("Do you want to create chart with drbd type or readwrite type?(Enter: dt / rw):")
            if kind == "dt":
                sqlchart.sql_graph_output()
            if kind == "rw":
                sqlchart.sql_print_drbd()
                sqlchart.sql_graph_output_rw()
        if graph == "histogram":
            sqlhis.sql_graph_output()

    
    elif typein == "deviation":
        deviation = input("What kind of deviation do you want to create? (Enter: multiple standards / 1 standard)")
        if deviation == "multiple standards":
            sqldevi.sql_print_standard_drbd()
            sqldevi.sql_pick_standard_values()
            sqldevi.sql_print_example_drbd()
            sqldevi.sql_pick_example_values()
            sqldevi.draw()
        if deviation == "1 standard":
            sqldevi.sql_print_standard_drbd()
            sqldevi.sql_pick_standard_values_1()
            sqldevi.sql_print_example_drbd()
            sqldevi.sql_pick_example_values()
            sqldevi.draw_1standard()

    elif typein == "view":
        index.sql_print_index()
        sqlview.sql_test()
    
    elif typein == "manage":
        index.sql_print_index()
        sqlman.drop_table()
        sqlman.drop_row()
    
    elif typein not in ["input", "analysis", "graph", "deviation", "view", "manage"]:
        print("Not a vaild keyword. Please Enter again.")
        main()

if __name__ == '__main__':
    main()