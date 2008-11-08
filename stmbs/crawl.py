#!/usr/bin/python
"""Program used to crawl the file system (and other resources) to find
   new and interesting files."""

import os.path

from filesystemiterator import *
from urifilter import *
from storage import *
from sqlitestorage import *
from urimetadata import *
from parser import *
from typeregistry import *

typereg = TypeRegistry()
typereg.registerFactory(TextParserFactory())

storage = "test2.db"
s = SqliteStorage(storage)
s.startStoringMany()
print "Load"
#for data in FilesystemIterator("/home/tryl/almen/"):
for data in FilesystemIterator("/home/tryl/almen/programmer/release/"):
    s.storeUri(data)
    if os.path.isfile(data.getGlobalIdentifier()):
        parser = typereg.findParser(data)
        if parser:
            print data
            for word in parser:
                s.storeKeyword(data, word)
                #print word, " ", 
    #print data
print "Find"
s.findWord("hold")
print s.findInFilename("crawl")
s.closeConnection()
