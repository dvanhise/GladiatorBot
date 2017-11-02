from settings import UNIT_DATA, AOE2_PATH
import pyautogui

import subprocess
import time
from random import randint
from itertools import combinations


class Simulation(object):

    def __init__(self):
        # Open OBS with local config file and start stream
        self.entrants = []
        self.results = []
        pyautogui.PAUSE = .5

        # Open AoE2
        # subprocess.call(AOE2_PATH + ' nostartup nomusic', shell=True)
        subprocess.call(AOE2_PATH, shell=True)

    def runSim(self):
        # TODO: This is full round robin, need a way to have fewer matches, each player plays ~10
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
        homeCoords = [11, 11]
        awayCoords = [23, 23]

        # TODO: Set players as blank AI, no fog of war
        # Create scenario with 2 AI players controlling the home and away armies respectively
        data = """<?php function Scenario(){

            Trig('init');
            SetPlayersCount(2);
            SetMapSize(34);
            SetAllTech(True);

            SetPlayerCiv(1, 'Chinese');
            SetPlayerCiv(2, 'Chinese');
            SetPlayerStartAge(1, 'Castle');
            SetPlayerStartAge(2, 'Castle');
            """
        data += '\nSetPlayerName(1, "%s");' % home.display
        data += '\nSetPlayerName(2, "%s");' % away.display
        data += self.unitCreationString(home.getUnitComp(), 1, homeCoords)
        data += self.unitCreationString(away.getUnitComp(), 2, awayCoords)
        data += '\n\nTrig("start");'
        data += '\nCond_Timer(1);'
        data += '\nEfft_Chat(1,"Hello1");'
        data += '\nEfft_Chat(2,"Hello2");'
        data += self.armyPatrolString(1, homeCoords, awayCoords)
        data += self.armyPatrolString(2, awayCoords, homeCoords)
        data += '\nEfft_ChangeView(1, [17,17]);'
        data += '\nEfft_ChangeView(2, [17,17]);'
        data += '} ?>'

        with open('./php_scx/Scenario.php', 'w') as outfile:
            outfile.write(data)

        # Generate scenario, needs to be called twice
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)

        # Run scenario in AoE2
        time.sleep(5)
        print('Starting automated clicking')
        pyautogui.click(884, 189, button='left')  # Click 'Single Player'
        pyautogui.click(1477, 302, button='left')  # Click 'Standard Game'
        pyautogui.click(1852, 117, button='left')  # Click dropdown arrow on game type
        pyautogui.click(1605, 326, button='left')  # Click "Scenario..."
        pyautogui.doubleClick(371, 165, button='left')  # Double click first scenario on list
        # set AI?
        # Start game
        while True:
            im = pyautogui.screenshot()
            # test it for end of game screen  and player points
            time.sleep(1)
        # Click finish
        # Click to main menu

        return 100

    def unitCreationString(self, comp, playerNum, coords):
        strn = ''
        for unit, count in comp.items():
            unitData = UNIT_DATA[unit]

            if 'tech' in unitData['type']:
                strn += '\nEfft_Research(%d, %d);' % (playerNum, unitData['id'])
            else:
                for i in range(count):
                    strn += '\nNewObject(%d, %d, [%d, %d], 0, %d);' % (
                        playerNum,
                        unitData['id'],
                        coords[0]+randint(-2, 2),
                        coords[1]+randint(-2, 2),
                        playerNum+5000
                    )

        return strn

    def armyPatrolString(self, playerNum, coords, enemyCoords):
        return '\nEfft_PatrolG(%d, %d, [[%d, %d],[%d, %d]], [%d, %d]);' % (
            playerNum,
            5000+playerNum,
            coords[0]+4,
            coords[1]+4,
            coords[0]-4,
            coords[1]-4,
            enemyCoords[0],
            enemyCoords[1]
        )
