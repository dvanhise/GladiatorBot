from itertools import combinations
from settings import UNIT_DATA

import subprocess


class Simulation(object):

    def __init__(self):
        # Open AoE2
        # Open OBS with local config file and start stream
        self.entrants = []
        self.results = []

    def runSim(self):
        # TODO: This is full round robin, need a way to have fewer matches
        self.runBattle(self.entrants[0], self.entrants[1])
        # for home, away in combinations(self.entrants, 2):
        #     results = self.runBattle(home, away)
        #     # accumulate results

        return {}

    def setEntrants(self, armies):
        self.entrants = armies
        self.results = []

    # Run battle with existing script file and return results.
    #   results are hitpoints remaining on all winning side units, number is negative if away team won
    def runBattle(self, home, away):
        homeCoords = [25, 25]
        awayCoords = [40, 40]

        data = """<?php function Scenario(){
            SetPlayersCount(2);
            SetMapSize(50);
            """
        data += self.unitCreationString(home.getUnitComp(), 1, homeCoords)
        data += self.unitCreationString(away.getUnitComp(), 2, awayCoords)
        data += '\n\nTrig("Attack each other",1,0);'
        data += '\nCond_Timer(1);'
        data += self.armyPatrolString(1, homeCoords, awayCoords)
        data += self.armyPatrolString(2, awayCoords, homeCoords)
        data += '} ?>'

        with open('./php_scx/Scenario.php', 'w') as outfile:
            outfile.write(data)

        # Generate scenario, needs to be called twice
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)

        # Run scenario in AoE2
        return 100

    def unitCreationString(self, comp, playerNum, coords):
        str = ''
        for unit, count in comp.items():
            unitData = UNIT_DATA[unit]

            if 'tech' in unitData['type']:
                str += '\nEfft_Research(%d, %d);' % (playerNum, unitData['id'])
            else:
                for i in range(count):
                    str += '\nNewObject(%d, %d, [%d, %d], 0);' % (playerNum, unitData['id'], coords[0], coords[1])

        return str

    def armyPatrolString(self, playerNum, coords, enemyCoords):
        return '\nEfft_PatrolO(%d, [[%d, %d],[%d, %d]], [%d, %d]);' % (
            playerNum,
            coords[0]+5,
            coords[1]+5,
            coords[0]-5,
            coords[1]-5,
            enemyCoords[0],
            enemyCoords[1]
        )
