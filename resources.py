
class Resources:

    def __init__(self, wood, food, gold):
        self.wood = wood
        self.food = food
        self.gold = gold

    def canAfford(self, unit, count):
        return unit['wood']*count <= self.wood and \
               unit['food']*count <= self.food and \
               unit['gold']*count <= self.gold

    def purchase(self, unit, count=1):
        self.wood -= count * unit['wood']
        self.food -= count * unit['food']
        self.gold -= count * unit['gold']
        self.verify()

    def unpurchase(self, unit, count=1):
        self.wood += count * unit['wood']
        self.food += count * unit['food']
        self.gold += count * unit['gold']

    def verify(self):
        if min(self.wood, self.food, self.gold) < 0:
            raise ValueError

    def __str__(self):
        return 'wood: {}, food: {}, gold: {}'.format(self.wood, self.food, self.gold)
