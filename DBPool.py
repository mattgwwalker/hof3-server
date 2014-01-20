from twisted.enterprise import adbapi

filename = "hof3.sqlite"
dbpool = adbapi.ConnectionPool("sqlite3", filename, check_same_thread=False)
