from twisted.enterprise import adbapi

def setRowFactory(connection):
    import sqlite3
    connection.row_factory = sqlite3.Row


filename = "hof3.sqlite"
dbpool = adbapi.ConnectionPool("sqlite3", filename, check_same_thread=False, cp_openfun=setRowFactory)
