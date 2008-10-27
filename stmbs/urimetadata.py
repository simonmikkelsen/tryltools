
class UriMetadata:
    """Represetns a lot of metadata about a uri.
		v-ObjectName
		-MimeType
        v-FileName
		v-FileExt
		v-FilePath
		-getMoreKeywords
		-resetKeywordPointer
		-Title
		v-FileSize
		v-FileCreationDate
		v-FileModificationDate
		-Author
		-Copyright
		-Genre
		-Tags
		-Description
		-thumbnail
		-wordcount
		-pauseIndexing
"""
    def __init__(self, protocol, globalIdentifier):
        """Creates a new instance.
           -`protocol`: The protocol used to get the `globalIdentifier`,
                        e.g. http, file etc.
           -`globalIdentifier`: Identifies the represented object uniquely
                        in the World, when combined with the `protocol`.
                        This can e.g. be a file path or web url.
        """
        self.protocol = protocol
        self.globalIdentifier = globalIdentifier

        self.filePath = None
        self.fileName = None
        self.fileExtension = None
        self.fileSizeBytes = None
        self.fileCreateDate = None
        self.fileModificationDate = None

    def __str__(self):
        return self.protocol + "://" + self.globalIdentifier

    def setFileInfo(self, path, name, ext, sizeBytes, createDate, modDate):
        """Sets information you usually gets from a file. It is OK to set info
           to `None` if it does not exist.
           -`path`: The path to the file, excluding protocol and file name. Trailing slash is optional.
           -`name`: The file name including extension.
           -`ext`:  The file extension excluding the leading dot. If a file name contains
                    more than one dot, like .tar.gz, it is up to the implementor to determine
                    if the multiple extensions should be part of the extension or not.
           -`sizeBytes`: The file size in bytes - and bytes only.
           -`createDate`: The creation date of the file in Unix time (seconds since 1.1. 1970).
           -`modDate`:  The files modification date in Unix time.
        """
        self.filePath = path
        self.fileName = name
        self.fileExtension = ext
        self.fileSizeBytes = sizeBytes
        self.fileCreateDate = createDate
        self.fileModificationDate = modDate
    
    def getProtocol(self):
        return self.protocol

    def getGlobalIdentifier(self):
        return self.globalIdentifier

    def getFilePath(self):
        return self.filePath

    def getFileName(self):
        return self.fileName

    def getFileExtension(self):
        return self.fileExtension

    def getsizeBytes(self):
        return self.fileSizeBytes

    def getFileCreateDate(self):
        return self.fileCreateDate

    def getFileModificationDate(self):
        return self.fileModificationDate

