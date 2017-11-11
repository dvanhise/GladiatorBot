from random import random, randint, betavariate
from copy import deepcopy

from genome import Genome
from resources import Resources

from settings import MUT_RATE, CROSSOVER_RATE, WOOD, FOOD, GOLD, UNIT_DATA


class ArmyManager(list):
    def getByName(self, name):
        for army in self:
            if army.name == name:
                return army


class Army(object):

    def __init__(self, botData=None, genome=None):

        if botData:
            self.name = botData.get('name', 'bot' + str(randint(0, 10**6)))
            self.display = botData.get('display', self.name)
        else:
            self.name = self.display = 'bot' + str(randint(0, 10**6))

        if genome:
            self.genome = genome
        else:
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
        self.comp = self.getUnitComp()

    def __str__(self):
        return self.name

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
    # def getUnitComp(self):
    #     normGenome = self.genome.power(3)   # Higher number here boosts higher valued units even more
    #     resources = Resources(WOOD, FOOD, GOLD)
    #     armyComp = {}
    #
    #     valueTotal = sum(normGenome.values())
    #     totalResources = WOOD + FOOD + GOLD
    #
    #     testResources = Resources(0, 0, 0)
    #     # Iterate through units to find relative demand for each resource
    #     for key, value in normGenome.items():
    #         unit = UNIT_DATA[key]
    #         totalUnitCost = unit['wood'] + unit['food'] + unit['gold']
    #         fairRatio = value/valueTotal
    #
    #         # How many of unit should I buy if all resources were combined and identical?
    #         fairUnitBuy = fairRatio * totalResources/totalUnitCost
    #
    #         testResources.unpurchase(unit, fairUnitBuy)
    #
    #     woodDemand = testResources.wood/WOOD
    #     foodDemand = testResources.food/FOOD
    #     goldDemand = testResources.gold/GOLD
    #
    #     remainderTab = {}
    #     # Based off relative resource demand and fair ratio, purchase units
    #     for key, value in normGenome.items():
    #         fairRatio = value/valueTotal
    #         unit = UNIT_DATA[key]
    #         totalRelativeUnitCost = unit['wood']*woodDemand + unit['food']*foodDemand + unit['gold']*goldDemand
    #         allowance = []
    #         if unit['wood']:
    #             woodAllowance = WOOD * fairRatio/(woodDemand * unit['wood'])
    #             allowance.append(woodAllowance)
    #         if unit['food']:
    #             foodAllowance = FOOD * fairRatio/(foodDemand * unit['food'])
    #             allowance.append(foodAllowance)
    #         if unit['gold']:
    #             goldAllowance = GOLD * fairRatio/(goldDemand * unit['gold'])
    #             allowance.append(goldAllowance)
    #
    #         count = min(allowance)
    #
    #         # Only one of a technology can be had
    #         if 'tech' in unit['type']:
    #             count = min(1, count)
    #
    #         resources.purchase(unit, int(count))
    #         armyComp[key] = int(count)
    #         #
    #         remainderTab[key] = value - int(count)*totalRelativeUnitCost*valueTotal/totalResources
    #
    #     # Go through remainderTab sorted by highest value and build one of each unit if it can be afforded.
    #     #   This is to fairly use up remaining resources
    #     sortedRemainder = sorted(remainderTab.items(), key=lambda x: x[1], reverse=True)
    #     for key, value in sortedRemainder:
    #         unit = UNIT_DATA[key]
    #         if resources.canAfford(unit, 1) and not ('tech' in unit['type'] and armyComp[key] >= 1):
    #             resources.purchase(unit, 1)
    #             armyComp[key] += 1
    #
    #     print(self.display + ' resources remaining: ' + str(resources))
    #     return armyComp

    # Returns dictionary of unit->count based on genome and resource limits
    def getUnitComp(self):
        normGenome = self.genome.power(3)   # Higher number here boosts higher valued units even more
        resources = Resources(WOOD, FOOD, GOLD)
        armyComp = {key: 0 for key in UNIT_DATA.keys()}

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

        purchase = True
        while purchase:
            purchase = False
            # Iterate through units starting from highest value
            for key, value in sorted(normGenome.items(), key=lambda x: x[1], reverse=True):
                unit = UNIT_DATA[key]
                # If unit can be afforded and isn't an already purchased tech
                if resources.canAfford(unit, 1) and not ('tech' in unit['type'] and armyComp[key] >= 1):
                    resources.purchase(unit, 1)
                    armyComp[key] += 1
                    totalRelativeUnitCost = unit['wood']*woodDemand + unit['food']*foodDemand + unit['gold']*goldDemand
                    normGenome[key] -= totalRelativeUnitCost*valueTotal/totalResources
                    purchase = True
                    # Re-sort gene values and start again once a unit had been purchased
                    break

        print(self.display + ' resources remaining: ' + str(resources))
        return armyComp

    def getArmyCompStrings(self):
        output = []
        # Sort tech first, then by count
        for unit, num in sorted(self.comp.items(), key=lambda x: x[1] + 20*UNIT_DATA[x[0]]['type'].count('tech'), reverse=True):
            if num > 0:
                if 'tech' in UNIT_DATA[unit]['type']:
                    output.append(UNIT_DATA[unit]['display'])
                else:
                    output.append('%d %s' % (num, UNIT_DATA[unit]['display']))
        return output

    def getGenome(self):
        return self.genome
