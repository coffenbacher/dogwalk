import json

class MSLogEntry(object):
    def __init__(self, pwalker, pdog, s, score):
        self.pwalker = pwalker
        self.pdog = pdog
        self.s = s
        self.score = score

    def __str__(self):
        return '%s\t%s\t%s\t%s\t%s\t%s\nSCORE:%s\n' % (self.pwalker.time, self.pwalker.walker.name, self.pdog.dog.name, self.pwalker.node, self.pdog.node, self.s, json.dumps(self.score))
