import os
import os.path

from urifilter import *
from urimetadata import UriMetadata
from inputstream import *

class FilesystemIterator:
    """Lets you iterate over a file system, one element at the time
       by returning instances of `UriMetadata`.
       """
    def __init__(self, startpath, urifilter = None):
        """Creates a new instance.
           -`startpath`: The path to the start folder.
           -`urifilter`: Filter, which must derive `UriFilter`.
        """
        if urifilter == None:
            urifilter = NullUriFilter()
        self.startpath = startpath
        self.urifilter = urifilter
    def file2meta(self, filepath):
        """Converts the given `filepath` to an instance of
           `UriMetadata`."""
        if os.path.isfile(filepath):
            inputstream = FileInputStream(filepath)
            inputstream.open()
        else:
            inputstream = None
        meta = UriMetadata("file", filepath, inputstream)
        path, basename = os.path.split(filepath)
        name, ext = os.path.splitext(basename)
        sizeBytes = os.path.getsize(filepath)
        createDate = os.path.getctime(filepath)
        modDate = os.path.getmtime(filepath)
        meta.setFileInfo(path, name, ext, sizeBytes, createDate, modDate)
        return meta

    def __iter__(self):
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
                    yield self.file2meta(fullpath)
                elif os.path.isdir(fullpath):
                    yield self.file2meta(fullpath)
                    for otherfile in FilesystemIterator(fullpath, self.urifilter):
                        yield otherfile #UriMetadata is already returned, so no convert.
                else:
                    print "Unsupported type: " + fullpath
            except OSError, err:
                print str(err)

# For testing, only run when class is run as a program.
if __name__ == "__main__": 
    startpath = "/home/tryl"
    for file in FilesystemIterator(startpath, NullUriFilter()):
        print file

