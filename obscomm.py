from more_itertools import chunked


class Obscomm(object):

    def __init__(self):
        self.names = [
            'home-display',
            'away-display',
            'home-comp',
            'away-comp',
            'gen',
            'scoreboard',
            'victory'
        ]

    def set(self, name, text):
        with open('./obs-' + name + '.txt', 'w') as obsfile:
            if type(text) is list:
                obsfile.write('\n'.join(text))
            else:
                obsfile.write(text)

    def split(self, name, text, size=3):
        for i, chunk in enumerate(list(chunked(text, size))):
            self.set(name + str(i+1), chunk)
