#import sqlite
from pysqlite2 import dbapi2 as sqlite

conn = sqlite.connect("test3.db")
curs = conn.cursor()
curs.execute('CREATE TABLE names (id INTEGER PRIMARY KEY, name VARCHAR(50), email VARCHAR(50))')
curs.execute('insert into names (name, email) values("Simon", "simon@mydomain.dk")')
curs.execute('select * from names where name = "Simon"')
print curs.fetchall()

curs.close()
conn.close()

