from pysqlite2 import dbapi2 as sqlite
import os.path

from storage import *

class SqliteStorage(SearchStorage):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = None
        self.commitCount = 0
        self.lastObjId = None
        self.lastUriMeta = None

    def startStoringMany(self):
        """Tells the class that now a lot of files will be stored.
           the class can then optimize for this."""
        self.assureSchemaExists()
        self.assureOpenConnection()
    def stopStoringMany(self):
        """Tells the class that there will not be stored a lot of files
           now. Should close for `startStoringMany`."""
        self.closeConnection()
    def storeUri(self, uriMetadata):
        """Stores the given metadata represented by the given object.
           -`uriMetadata`: Metadata to store, as an instance of `UriMetadata`.
        """
        self.curs.execute("""INSERT INTO object (protocol, identifier)
            VALUES (?, ?)""",
             [uriMetadata.getProtocol(), uriMetadata.getGlobalIdentifier()] )
        if self.commitCount % 1000 == 0:
            self.conn.commit()
        self.commitCount += 1
    def storeKeyword(self, uriMetadata, keyword):
        """Stores the given keyword as belonging to the given
           uri. The uri must have been stored using `storeUri` before
           calling this method.
           """
        # Make sure the word is inserted and we have the ID.
        self.curs.execute("""SELECT id from keyword WHERE word = ?""", [keyword])
        wordIdArr = self.curs.fetchone()
        if wordIdArr:
            wordId = wordIdArr[0]
        else:
            self.curs.execute("""INSERT INTO keyword (word) VALUES (?)""", [keyword])
            wordId = self.curs.lastrowid

        #Find the ID of the object.
        if self.lastUriMeta and self.lastUriMeta == uriMetadata and self.lastObjId:
            objId = self.lastObjId
        else:
            self.curs.execute("""SELECT id FROM object WHERE protocol = ? AND identifier = ?""",
                              [uriMetadata.getProtocol(), uriMetadata.getGlobalIdentifier()])
            objIdArr = self.curs.fetchone()
            if not objIdArr:
                raise RuntimeError("Expected to find an object for ", uriMetadata, ".")
            objId = objIdArr[0]
            self.lastObjId = objId
            self.lastUriMeta = uriMetadata
        self.curs.execute("""INSERT OR IGNORE INTO key_obj (keyid, objid) VALUES(?, ?)""",
                             [wordId, objId])
        
    def findInFilename(self, filepart):
        self.curs.execute("SELECT * FROM object WHERE identifier LIKE ?",['%%%s%%' % filepart])
        return self.curs.fetchall()
    def findWord(self, word):
        self.curs.execute("SELECT id FROM keyword WHERE word = ?", [word])
        #ids = self.curs.fetchall()
        #filenames = []
        #self.curs.execute("SELECT key_obj.objid FROM keyword, key_obj WHERE keyword.id = key_obj.keyid")
        #self.curs.execute("SELECT object.protocol, object.identifier FROM keyword, key_obj, object WHERE keyword.word = ? AND keyword.id = key_obj.keyid AND key_obj.keyid = object.id", [word])
        print "GO ", word
        print self.curs.fetchall()
        print "Done."
        #for i in ids:
            
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
        self.curs.execute("""CREATE UNIQUE INDEX keyindex ON keyword (id, word)""")
        self.curs.execute("""CREATE TABLE key_obj (keyid INTEGER, objid INTEGER,
                                                PRIMARY KEY (keyid, objid))""")
if __name__ == "__main__":
    s = SqliteStorage(":memory:")
    s.startStoringMany()
    s.closeConnection()

