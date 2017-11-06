from random import random, randint, betavariate
from copy import deepcopy
import os.path
import yaml

from genome import Genome
from resources import Resources

from settings import MUT_RATE, CROSSOVER_RATE, SAVE_DIR, WOOD, FOOD, GOLD, UNIT_DATA


class Army(object):

    def __init__(self, botData=None, genome=None):
        self.wins = 0
        self.losses = 0
        if botData:
            self.name = botData.get('name', 'bot' + str(randint(0, 10**6)))
            self.display = botData.get('display', self.name)
        else:
            self.name = self.display = 'bot' + str(randint(0, 10**6))

        if genome:
            self.genome = genome
        else:
            try:
                with open(self.getSavePath(), 'r') as data:
                    self.genome = Genome(yaml.load(data))
            except FileNotFoundError:
                # If no file is found, assume first run and randomize genome
                self.genome = Genome()
                for unitName, unitData in UNIT_DATA.items():
                    # Use a beta distribution weighted by bot's likes and dislikes
                    # Magic numbers are magic   (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
                    alpha = beta = 1
                    for like in (botData.get('like', []) if botData else []):
                        if like in unitData['type']:
                            alpha += .5
                    for dislike in (botData.get('dislike', []) if botData else []):
                        if dislike in unitData['type']:
                            beta += .5

                    self.genome[unitName] = betavariate(alpha=alpha, beta=beta)

    # Save state to file
    def save(self):
        with open(self.getSavePath(), 'w') as outfile:
            yaml.dump(self.genome, outfile, default_flow_style=False)

    def getSavePath(self):
        return os.path.join(SAVE_DIR, self.name + '.yaml')

    def makeChild(self, army):
        print('%s mates with %s' % (self.display, army.display))
        tempGenome = deepcopy(self.genome)
        if random() <= CROSSOVER_RATE:
            tempGenome.crossover(army.getGenome())
        for gene in tempGenome.keys():
            if random() <= MUT_RATE:
                tempGenome.mutate(gene)
        return Army({'name': self.name, 'display': self.display}, genome=tempGenome)

    # Returns dictionary of unit->count from army genome
    def getUnitComp(self):
        normGenome = self.genome.power(2)
        resources = Resources(WOOD, FOOD, GOLD)
        armyComp = {}

        valueTotal = sum(normGenome.values())
        totalResources = WOOD + FOOD + GOLD

        testResources = Resources(0, 0, 0)
        # Iterate through units to find relative demand for each resource
        for key, value in normGenome.items():
            unit = UNIT_DATA[key]
            totalUnitCost = unit['wood'] + unit['food'] + unit['gold']
            fairRatio = value/valueTotal

            # How many of unit should I buy if all resources were combined and identical?
            fairUnitBuy = fairRatio * totalResources/totalUnitCost

            testResources.unpurchase(unit, fairUnitBuy)

        woodDemand = testResources.wood/WOOD
        foodDemand = testResources.food/FOOD
        goldDemand = testResources.gold/GOLD

        remainderTab = {}
        # Based off relative resource demand and fair ratio, purchase units
        for key, value in normGenome.items():
            fairRatio = value/valueTotal
            unit = UNIT_DATA[key]
            mod = 1.5  # This helps but might cause invalid unit purchases
            allowance = []
            if unit['wood']:
                woodAllowance = WOOD * fairRatio * mod/(woodDemand * unit['wood'])
                allowance.append(woodAllowance)
            if unit['food']:
                foodAllowance = FOOD * fairRatio * mod/(foodDemand * unit['food'])
                allowance.append(foodAllowance)
            if unit['gold']:
                goldAllowance = GOLD * fairRatio * mod/(goldDemand * unit['gold'])
                allowance.append(goldAllowance)

            count = min(allowance)
            avg = sum(allowance)/len(allowance)

            # Only one of a technology can be had
            if 'tech' in unit['type']:
                count = min(1, count)

            resources.purchase(unit, int(count))
            armyComp[key] = int(count)
            remainderTab[key] = avg - int(count)

        # Go through remainderTab sorted by highest value and build one of each unit if it can be afforded.
        #   This is to fairly use up remaining resources
        sortedRemainder = sorted(remainderTab.items(), key=lambda x: x[1], reverse=True)
        for key, value in sortedRemainder:
            unit = UNIT_DATA[key]
            if resources.canAfford(unit, 1) and not ('tech' in unit['type'] and armyComp[key] >= 1):
                resources.purchase(unit, 1)
                armyComp[key] += 1

        print(self.display + ' resources remaining: ' + str(resources))
        return armyComp

    def getGenome(self):
        return self.genome
