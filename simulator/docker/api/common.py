#!/usr/bin/python -B


# Common response handler for WRITEFUNCTION callback
class HTTPResponseCollector():
    def __init__(self):
        self.responsebody = None
        self.responsebodylist = []
        self.lastline = None
        self._iteration = 0  

    def write(self, data):
        if self.responsebody == None:
            self.responsebody = data
        else:
            self.responsebody = self.responsebody + data
        
        self.lastline = data
        self._iteration += 1

    def writelist(self, data):
        self.responsebodylist.append(data)

        self.lastline = data
        self._iteration += 1