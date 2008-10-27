from parser import *

class TextFileParser(Parser):
    def __init__(self, inputstream)
    """Interface for classes which can parse files."""
    def getExtensions(self):
        """Returns a list of file extensions (without leading dot) that
           can be parsed."""
       return ["txt", "nfo"]
    def canParse(self, inputstream):
        """Returns if the given uri can be parsed.
           TODO this might change so the parser must have
           a stream of some sort provided."""
        raise NotImplementedException()
    def __iter__(self):
        """The class iterator which returns keywords."""
        pass

