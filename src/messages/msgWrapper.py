
class MsgWrapper:
    def __init__(self, body, dest, performative):
        self.body = body
        self.dest = dest
        self.performative = performative

    def getBody(self):
        return self.body
    
    def getDest(self):
        return self.dest
    
    def getPerformative(self):
        return self.performative
    
    def setBody(self, body):
        self.body = body

    def setDest(self, dest):
        self.dest = dest

    def setPerformative(self, performative):
        self.performative = performative