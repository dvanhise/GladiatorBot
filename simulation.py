from settings import UNIT_DATA

import pyautogui
import subprocess
import time
import psutil
from random import shuffle
from string import Template
from itertools import combinations
from more_itertools import chunked


class Simulation(object):

    def __init__(self):
        self.entrants = []
        self.wins = self.losses = []
        pyautogui.PAUSE = .5

        # Confirm AoE2 is running, it's the best check I can do
        if not [1 for pid in psutil.pids() if psutil.Process(pid).name() == "AoK HD.exe"]:
            raise RuntimeError("AoE2 HD must be running with the arena scenario in a completed state.")
        # (Hopefully) click within the AoE2 window
        pyautogui.click(1000, 1000, button='left')

    def runSim(self):
        # Create and shuffle full round robin
        matches = list(combinations(self.entrants, 2))
        shuffle(matches)
        for home, away in matches:
            result = self.runBattle(home, away)
            if result == -1:
                print('\n%s defeats %s' % (away.display, home.display))
                self.losses[home.name] += 1
                self.wins[away.name] += 1
            elif result == 1:
                print('\n%s defeats %s' % (home.display, away.display))
                self.losses[away.name] += 1
                self.wins[home.name] += 1
            else:
                raise ValueError('Match ended inconclusive, exiting.')

        return self.wins

    def setEntrants(self, armies):
        self.entrants = armies
        self.wins = {army.name: 0 for army in self.entrants}
        self.losses = {army.name: 0 for army in self.entrants}

    # Run battle with existing script file and return:
    #  1 for home team win
    #  0 for inconclusive result
    #  -1 for away team win
    def runBattle(self, home, away):
        # Coordinates for arenabase
        homeCoords = [10, 10]
        awayCoords = [24, 24]
        # Coordinates for arenabase2
        # homeCoords = [20, 7]
        # awayCoords = [20, 35]

        homeComp = home.getUnitComp()
        awayComp = away.getUnitComp()

        initialActions = self.armyPatrolString(1, homeCoords, awayCoords) + \
            self.armyPatrolString(2, awayCoords, homeCoords) + \
            '\nEfft_ChangeView(1, [%d,%d]);' % (int((homeCoords[0] + awayCoords[0])/2)-1, int((homeCoords[1] + awayCoords[1])/2)) + \
            self.armyCompChat(1, homeComp) + \
            self.armyCompChat(2, awayComp)

        subDict = {
            'SetPlayerNames': '\nSetPlayerName(1, "%s");' % home.display + '\nSetPlayerName(2, "%s");' % away.display,
            'AddUnitsTechs': self.unitCreationString(homeComp, 1, homeCoords) + self.unitCreationString(awayComp, 2, awayCoords),
            'InitialActions': initialActions
        }

        with open('./php_scx/ScenarioTemplate.php', 'r') as templateFile:
            result = Template(templateFile.read()).substitute(subDict)
            with open('./php_scx/Scenario.php', 'w') as outfile:
                outfile.write(result)

        # Generate scenario, needs to be called twice
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)

        # If we don't wait, AoE2 might read scenario before it's done compiling
        time.sleep(4)

        pyautogui.typewrite(['f10', 'up', 'up', 'enter', 'enter'])  # Open menu and select 'Restart'

        n = 0
        while n < 40:
            # Take a screenshot and crop to where the line appears through a player's score when they're eliminated.
            # Yes, seriously, that's how we're detecting who won and when the match is over.  If the home team is
            # given artificial point inflation, it will always be on top
            image = pyautogui.screenshot()

            awayLine = image.crop((1750, 890, 1910, 891)).convert('L')
            homeLine = image.crop((1750, 870, 1910, 871)).convert('L')
            if self.imageIsLine(homeLine):
                return -1
            elif self.imageIsLine(awayLine):
                return 1

            time.sleep(3)
            n += 1
        return 0

    def imageIsLine(self, im):
        pixels = [im.getpixel((x, 0)) for x in range(im.width)]
        for p in pixels:
            if p != pixels[0]:
                return False
        return True

    def unitCreationString(self, comp, playerNum, coords):
        strn = ''
        for unit, count in comp.items():
            unitData = UNIT_DATA[unit]

            if 'tech' in unitData['type']:
                strn += '\nEfft_Research(%d, %d);' % (playerNum, unitData['id'])
            else:
                for i in range(count):
                    strn += '\nNewObject(%d, %d, [%d, %d], 0);' % (
                        playerNum,
                        unitData['id'],
                        coords[0],
                        coords[1]
                    )

        return strn

    def armyPatrolString(self, playerNum, coords, enemyCoords):
        return '\nEfft_PatrolO(%d, Area(%d, %d, %d, %d), %s);' % (
            playerNum,
            coords[0]-4,
            coords[1]-4,
            coords[0]+4,
            coords[1]+4,
            enemyCoords
        )

    def armyCompChat(self, playerNum, comp):
        data = ''
        countList = []
        for unit, num in sorted(comp.items(), key=lambda x: x[1], reverse=True):
            if num > 0:
                countList.append('%d %s' % (num, UNIT_DATA[unit]['display']))
        for line in list(chunked(countList, 4)):
            data += '\nEfft_Chat(%d, "%s");' % (playerNum, ' - '.join(line))
        return data
