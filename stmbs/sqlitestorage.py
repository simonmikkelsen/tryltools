from pysqlite2 import dbapi2 as sqlite
import os.path

from storage import *

class SqliteStorage(SearchStorage):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = None
        self.commitCount = 0

    def startStoringMany(self):
        """Tells the class that now a lot of files will be stored.
           the class can then optimize for this."""
        self.assureSchemaExists()
        self.assureOpenConnection()
    def stopStoringMany(self):
        """Tells the class that there will not be stored a lot of files
           now. Should close for `startStoringMany`."""
        self.closeConnection()
    def store(self, uriMetadata):
        """Stores the given metadata represented by the given object.
           -`uriMetadata`: Metadata to store, as an instance of `UriMetadata`.
        """
        self.curs.execute("""INSERT INTO object (protocol, identifier)
            VALUES (?, ?)""",
             [uriMetadata.getProtocol(), uriMetadata.getGlobalIdentifier()] )
        if self.commitCount % 1000 == 0:
            self.conn.commit()
        self.commitCount += 1
    def find(self, filepart):
        self.curs.execute("SELECT * FROM object WHERE identifier LIKE ?",['%%%s%%' % filepart])
        return self.curs.fetchall()
    def assureOpenConnection(self):
        """Makes sure the connection to the database is open."""
        if self.conn == None:
            self.conn = sqlite.connect(self.dbfile)
            self.curs = self.conn.cursor()
    def closeConnection(self):
        """Closes the connection and handles if its already closed."""
        try:
            if self.curs != None:
                self.curs.close()
            if self.conn != None:
                self.conn.close()
        except:
            pass #Ignore all errors while closing up.
        finally:
            self.curs = None
            self.conn = None
    def assureSchemaExists(self):
        """Creates a new schema if the database does not exist."""
        if os.path.isfile(self.dbfile):
            return
        #There is no file: Create the db schema.
        self.assureOpenConnection()
        self.curs.execute("""CREATE TABLE object (id INTEGER PRIMARY KEY,
                                                  protocol VARCHAR(10),
                                                  identifier VARCHAR(512))""")
        self.curs.execute("""CREATE UNIQUE INDEX objindex ON object (protocol, identifier) """)
        self.curs.execute("""CREATE UNIQUE INDEX objidindex ON object (id) """)
        self.curs.execute("""CREATE TABLE keyword (id INTEGER PRIMARY KEY,
                                                 word VARCHAR(50),
                                                 refcount INTEGER)""")
        self.curs.execute("""CREATE UNIQUE INDEX keyindex ON keyword (word, refcount)""")
        self.curs.execute("""CREATE TABLE key_obj (keyid INTEGER, objid INTEGER,
                                                PRIMARY KEY (keyid, objid))""")
if __name__ == "__main__":
    s = SqliteStorage(":memory:")
    s.startStoringMany()
    s.closeConnection()

