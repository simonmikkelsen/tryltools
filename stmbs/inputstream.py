class InputStream:
    """General input stream which is independent of input source."""
    def close(self):
        """Signal that the stream is not to be used anymore."""
        raise NotImplementedError()
    def isOpen(self):
        """Returns if the stream is open."""
        raise NotImplementedError()
    def rewind(self):
        """Rewinds the stream, so it will return matrial from the start.
           This feature is so parsers can take a look at some material and
           determine if they can parse it.
           To save a parser should not expect to be able to use this method
           if more than 4 KB of data has been read, in which case a 
           `CannotRewindException` might be raised."""
        raise NotImplementedError()
    def read(self, count):
        """Read and return at most this number of bytes.
           When there is not more data, nothing is returned.
           -`count`: The largest number of bytes to read at the time.
                     Why not just read the next line? Have you ever seen
                     a 100 MB XML file with no newlines? I have.
           -`readline`: Return at most the next line."""
        raise NotImplementedError()
    def readline(self, count):
        """Read and return at most this number of bytes or one line
           whichever comes first.
           When there is not more data, nothing is returned.
           -`count`: The largest number of bytes to read at the time.
                     Why not just read the next line? Have you ever seen
                     a 100 MB XML file with no newlines? I have.
        """
        raise NotImplementedError()

class CannotRewindException(StandardError):
    """Raised if somebody tries to rewind an input stream when the beginning
       of the buffer has been disguarded and cannot be recovered."""
    pass

class FileInputStream(InputStream):
    """`InputStream` which reads from a file system."""
    def __init__(self, filepath):
        """Creates a new instance.
           -`filepath`: Path to the file."""
        self.uri = filepath 
        self.filepointer = None
 
    def open(self):
        """Opens the input stream using the uri given to the constructor.."""
        self.filepointer = open(self.uri)
    def close(self):
        """Signal that the stream is not to be used anymore."""
        if self.filepointer != None:
            if not self.filepointer.closed:
                self.filepointer.close()
            self.filepointer = None
    def isOpen(self):
        """Returns if the stream is open."""
        return self.filepointer != None and not self.filepointer.closed
    def rewind(self):
        """Rewinds the stream, so it will return matrial from the start.
           This feature is so parsers can take a look at some material and
           determine if they can parse it.
           To save a parser should not expect to be able to use this method
           if more than 4 KB of data has been read, in which case a 
           `CannotRewindException` might be raised."""
        self.filepointer.seek(0)
    def read(self, count):
        """Read and return at most this number of bytes.
           When there is not more data, nothing is returned.
           -`count`: The largest number of bytes to read at the time.
                     Why not just read the next line? Have you ever seen
                     a 100 MB XML file with no newlines? I have.
        """
        return self.filepointer.read(count) 
    def readline(self, count):
        """Read and return at most this number of bytes or one line
           whichever comes first.
           When there is not more data, nothing is returned.
           -`count`: The largest number of bytes to read at the time.
                     Why not just read the next line? Have you ever seen
                     a 100 MB XML file with no newlines? I have.
        """
        return self.filepointer.readline(count)
