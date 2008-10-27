class UriFilter:
    """Base for classes which can filter uris."""
    def __init__(self):
        self.next = None
    def getNext(self):
        """Returns the next filter in the chain or `None` if none exists."""
        return self.next
    def addFilter(self, nextFilter):
        """Adds the given filter to the end of the filter chain."""
        if self.next == None:
            self.next = nextFilter
        else:
            self.next.addFilter(nextFilter)
    def match(self, uri):
        """Returns if the given `url` matches (i.e. it may be used)
        or not (i.e. the uri must not be used).
        This method must be implemented by all filters."""
        raise NotImplementedError()

class NullUriFilter(UriFilter):
    """`UrlFilter`which will accept any uri given to it. This is good for testing but not
    that good for production code."""
    def match(self, uri):
        """Returns if the given `url` matches (i.e. it may be used)
        or not (i.e. the uri must not be used).
        This method must be implemented by all filters."""
        return True

