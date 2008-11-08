# -*- coding: latin-1 -*-
import string
import re

from inputstream import *
from urimetadata import *

class ParserFactory:
    """Creates instances of `Parser`s and determines if a parser can
       parse some data. One `ParserFactory` can represent one or more
       parsers.
    """
    def findParser(self, urimetadata):
        """Returns a parser suiteable for the given uri or `None`
           if this factory does not think it can find one.
           It is up to the parser to use which data it finds most suitable
           and all arguments can be `None`. In the latter case `None` should
           also be returned, but hey - the parser might just be that magic
           that can get something from nothing.
           -`urimetadata`: Uri to get parser from or `None`.
        """
        raise NotImplementedError()

class Parser:
    def __iter__(self):
        """Each call returns the next parsed word."""
        raise NotImplementedError()

class TextParserFactory(ParserFactory):
    def findParser(self, urimetadata):
        """Returns a parser suiteable for the given uri or stream or `None`
           if this parser does not think it can find one.
           It is up to the parser to use which data it finds most suitable
           and all arguments can be `None`. In the latter case `None` should
           also be returned, but hey - the parser might just be that magic
           that can get something from nothing.
           -`urimetadata`: Uri to get parser from or `None`.
        """
        if urimetadata == None:
            return None
        ext = urimetadata.getFileExtension()
        mime = urimetadata.getMimeType()
        if ext in [".txt", ".nfo"] or mime in ["text/plain"]:
            return SimpleTextParser(urimetadata.getInputstream())
        return None

class SimpleTextParser(Parser):
    def __init__(self, inputstream):
        """Simple class for parsing text. It does not handle encoding and
           may give bad results for some non english and non danish languages.
           But it's simple and a good start.
           -`inputstream`: `InputStream` to read from."""
        self.inputstream = inputstream

        # Read buffer size
        self.readBufferSize = 4090

        # List of chars which can be part of a word.
        wordChars = string.ascii_lowercase + 'æøåöäëñõãiüéáèàóòýíìúùũ'
        self.reNonWord = re.compile("[^"+re.escape(wordChars)+"]+")
        self.readBuffer = ""
    def __iter__(self):
        """The class iterator which returns keywords."""
        readInput = lambda: self.inputstream.readline(self.readBufferSize)
        read = readInput()
        while len(read) > 0:
            self.readBuffer += read.lower()
            words = self.reNonWord.split(self.readBuffer)
            self.readBuffer = words.pop()
            for w in words:
                yield w
            read = readInput()
        if len(self.readBuffer) > 0:
            yield self.readBuffer
        self.readBuffer = ""

# Test - only run when the file is run standalone.
if __name__ == "__main__":
    from inputstream import *
    from urimetadata import *
    uriMeta = UriMetadata("file", "test.txt")
    stream = FileInputStream(uriMeta)
    stream.open()
    parser = SimpleTextFileParser(stream)
    for word in parser:
        print word
