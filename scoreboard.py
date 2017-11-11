from itertools import combinations
from random import shuffle


def strOrObj(func):
    def wrapper(*args, **kwargs):
        return func(args[0], *[x if type(x) is str else str(x) for x in args[1:]])
    return wrapper


class Scoreboard:

    def __init__(self, entrants, saveData=None):
        if type(entrants[0]) is str:
            ents = entrants
        else:
            ents = [str(e) for e in entrants]

        if saveData:
            self.board = saveData['board']
            self.matches = saveData['matches']
        else:
            self.board = {e: [0, 0] for e in ents}
            self.matches = list(combinations(ents, 2))
            shuffle(self.matches)

    def getNextMatch(self):
        while len(self.matches):
            yield self.matches.pop()
        return

    # Adding a new player mid-gen
    @strOrObj
    def addEntrant(self, entrant):
        self.board[entrant] = [0, 0]
        for e in self.board.items():
            self.matches.append((e, entrant))
        shuffle(self.matches)

    @strOrObj
    def result(self, winner, loser):
        self.board[winner][0] += 1
        self.board[loser][1] += 1

    @strOrObj
    def getRecord(self, entrant):
        return self.board[entrant]

    def getBest(self):
        return max(self.board.items(), key=lambda x: x[1][0]-x[1][1])[0]

    def getScoreStrings(self, e):
        output = []
        for name, score in sorted(self.board.items(), key=lambda x: x[1][0]-x[1][1], reverse=True):
            output.append('%s  %d-%d' % (e[name].display, score[0], score[1]))
        return output

    def getSaveData(self):
        return {
            'board': self.board,
            'matches': self.matches
        }
