class File:
    def __init__(self, parent, name, hashName, hash):
        self.parent = parent
        self.name = name
        self.hashName = hashName
        self.hash = hash
        self.files = []
        self.accents = []

    def addFile(self, file):
        if isinstance(file, File):
            self.files.append(file)
        else:
            raise AssertionError("should be file")

    def removeFile(self, file):
        if isinstance(file, File):
            self.files.remove(file)
        else:
            raise AssertionError("should be file")

    def addAccent(self, accent):
        self.accents.append(accent)

    def removeAccent(self, accent):
        self.accents.remove(accent)
