class Parser:
    """Interface for classes which can parse files."""
    def getExtensions(self):
        """Returns a list of file extensions (without leading dot) that
           can be parsed."""
        raise NotImplementedException()
    def canParser(self, uri):
        """Returns if the given uri can be parsed.
           TODO this might change so the parser must have
           a stream of some sort provided."""
        raise NotImplementedException()

