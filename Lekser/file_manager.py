import os

class FileManager:
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        self.file = open(self.path, "r")

    def close(self):
        self.file.close()
        self.file = None

    def get_chars(self, n=1):
        if n < 0:
            raise ValueError("cant get negative number of chars")

        chars = self.file.read(n)
        
        return chars

    def peek_chars(self, n=1):
        if n < 0:
            raise ValueError("cant get negative number of chars")

        position = self.file.tell()
        chars = self.file.read(n)
        self.file.seek(position, os.SEEK_SET)

        return chars
