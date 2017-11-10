from itertools import combinations
from random import shuffle


class Scoreboard(object):

    def __init__(self, entrants, saveData=None):
        if type(entrants[0]) is str:
            ents = entrants
        else:
            ents = [e.name for e in entrants]

        if saveData:
            self.board = saveData['board']
            self.matches = saveData['matches']
        else:
            self.board = {e.name: (0, 0) for e in ents}
            self.matches = list(combinations(ents, 2))
            shuffle(self.matches)

    def getNextMatch(self):
        while len(self.matches):
            yield self.matches.pop()
        return

    # Adding a new player mid-gen
    def addEntrant(self, entrant):
        self.board[entrant.name] = (0, 0)
        for e in self.board.items():
            self.matches.append((e, entrant))
        shuffle(self.matches)

    def result(self, winner, loser):
        self.board[winner.name][0] += 1
        self.board[loser.name][1] += 1

    def getRecord(self, army):
        return self.board[army.name]

    def getBest(self):
        return sorted(self.board.items(), key=lambda x: x[1][0]-x[1][1], reverse=True)[0]

    def getScoreStrings(self):
        output = []
        for army, score in sorted(self.board.items(), key=lambda x: x[1][0]-x[1][1], reverse=True):
            output.append('%s  %d-%d' % (army, score[0], score[1]))
        return output

    def getSaveData(self):
        return {
            'board': self.board,
            'matches': self.matches
        }
