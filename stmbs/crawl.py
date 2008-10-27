#!/usr/bin/python
"""Program used to crawl the file system (and other resources) to find
   new and interesting files."""

import os.path
from filesystemiterator import *
from urifilter import *
from storage import *
from sqlitestorage import *
from urimetadata import *

storage = "test2.db"
s = SqliteStorage(storage)
s.startStoringMany()
print "Load"
for file in FilesystemIterator("/home/tryl/almen/"):
    data = UriMetadata("file", file)
    s.store(data)
    #print data
print "Find"
print s.find("crawl")
s.closeConnection()
