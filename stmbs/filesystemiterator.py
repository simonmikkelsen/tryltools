import os
import os.path

from urifilter import *

class FilesystemIterator:
    """Lets you iterate over a file system, one element at the time."""
    def __init__(self, startpath, urifilter = None):
        """Creates a new instance.
           -`startpath`: The path to the start folder.
           -`urifilter`: Filter, which must derive `UriFilter`.
        """
        if urifilter == None:
            urifilter = NullUriFilter()
        self.startpath = startpath
        self.urifilter = urifilter
    def __iter__(self):
        return self.next()
    def next(self):
        """This class iterator method, which returns the next file or dir."""
        files = []
        try:
            files = os.listdir(self.startpath)
        except OSError, err:
            print str(err)
        for file in files:
            try:
                fullpath = os.path.join(self.startpath, file)
                if not self.urifilter.match(fullpath):
                    continue
                if os.path.isfile(fullpath) or os.path.islink(fullpath):
                    yield fullpath
                elif os.path.isdir(fullpath):
                    yield fullpath
                    for otherfile in FilesystemIterator(fullpath, self.urifilter):
                        yield otherfile
                else:
                    print "Unsupported type: " + fullpath
            except OSError, err:
                print str(err)

# For testing, only run when class is run as a program.
if __name__ == "__main__": 
    startpath = "/home/tryl"
    for file in FilesystemIterator(startpath, NullUriFilter()):
        print file

