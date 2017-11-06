from settings import UNIT_DATA
from obscomm import Obscomm

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
        self.obs = Obscomm()
        pyautogui.PAUSE = .25

        self.assertAoe2Running()
        # (Hopefully) click within the AoE2 window
        pyautogui.click(1000, 1000, button='left')

    def runSim(self):
        self.obs.split('scoreboard', self.getScoreStrings(), size=9)
        # Create and shuffle full round robin
        matches = list(combinations(self.entrants, 2))
        shuffle(matches)
        for home, away in matches:
            self.generateScenario(home, away)
            self.obs.set('victory', '')
            result = self.runBattle()
            while result == 0:
                print('Inconclusive match, regenerating scenario file')
                self.obs.set('victory', 'Battle Inconclusive')
                self.generateScenario(home, away)
                result = self.runBattle()
            if result == -1:
                print('%s defeats %s' % (away.display, home.display))
                self.obs.set('victory', '%s defeats %s' % (away.display, home.display))
                home.losses += 1
                away.wins += 1
            elif result == 1:
                print('%s defeats %s' % (home.display, away.display))
                self.obs.set('victory', '%s defeats %s' % (home.display, away.display))
                away.losses += 1
                home.wins += 1
            self.obs.split('scoreboard', self.getScoreStrings(), size=9)

        print('End of generation results:')
        for st in self.getScoreStrings():
            print(st)

    def setEntrants(self, armies):
        self.entrants = armies

    # Run battle with existing script file and return:
    #  1 for home team win
    #  0 for inconclusive result
    #  -1 for away team win
    def runBattle(self):
        pyautogui.press('f10')   # Open menu and select 'Restart'
        pyautogui.press('up')
        pyautogui.press('up')
        pyautogui.press('enter')
        pyautogui.press('enter')
        self.assertAoe2Running()

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

    def generateScenario(self, home, away):
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
            '\nEfft_ChangeView(1, [%d,%d]);' % (int((homeCoords[0] + awayCoords[0])/2)-1, int((homeCoords[1] + awayCoords[1])/2))

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
        time.sleep(5)   # If we don't wait it breaks, maybe AoE2 is reading scenario before it's done compiling

        self.obs.set('home-comp', self.getArmyCompStrings(homeComp))
        self.obs.set('away-comp', self.getArmyCompStrings(awayComp))
        self.obs.set('home-display', '%s  %d-%d' % (home.display, home.wins, home.losses))
        self.obs.set('away-display', '%d-%d  %s' % (away.wins, away.losses, away.display))

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

    def getScoreStrings(self):
        output = []
        for army in sorted(self.entrants, key=lambda x: x.wins, reverse=True):
            output.append('%s  %d-%d' % (army.display, army.wins, army.losses))
        return output

    def getArmyCompStrings(self, comp):
        output = []
        for unit, num in sorted(comp.items(), key=lambda x: x[1], reverse=True):
            output.append('%d %s' % (num, UNIT_DATA[unit]['display']))
        return output

    def assertAoe2Running(self):
        found = False
        for pid in psutil.pids():
            try:
                if psutil.Process(pid).name() == "AoK HD.exe":
                    found = True
            except ProcessLookupError:
                pass
        if not found:
            raise RuntimeError("AoE2 HD must be running with the arena scenario.")
