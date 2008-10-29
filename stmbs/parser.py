# -*- coding: latin-1 -*-
import string
import re

from inputstream import *

class Parser:
    """Interface for classes which can parse files."""
    def getExtensions(self):
        """Returns a list of file extensions (without leading dot) that
           can be parsed."""
        raise NotImplementedException()
    def canParse(self, inputstream):
        """Returns if the given uri can be parsed.
           This method must not modify the rest of the object, as it
           can be invoked any number of times without `reset` being
           invoked.
           -`inputstream`: `InputStream` to read from.
        """
        raise NotImplementedException()

class SimpleTextFileParser(Parser):
    def __init__(self, inputstream):
        """Simple class for parsing text files. It does not handle encoding and
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
    def getExtensions(self):
        """Returns a list of file extensions (without leading dot) that
           can be parsed."""
        return ["txt", "nfo"]
    def canParse(self, inputstream):
        """Returns if the given uri can be parsed.
           This method must not modify the rest of the object, as it
           can be invoked any number of times without `reset` being
           invoked.
           -`inputstream`: `InputStream` to read from.
        """
        # If the extension isn't text, ignore it.
        return False
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
