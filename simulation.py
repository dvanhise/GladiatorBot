from settings import UNIT_DATA, HOME_SPAWN, AWAY_SPAWN
from obscomm import Obscomm
from scoreboard import Scoreboard

import pyautogui
import subprocess
import time
import psutil
from string import Template


class Simulation(object):

    def __init__(self, entrants, scoreboardData=None):
        self.entrants = {entrant.name: entrant for entrant in entrants}
        self.obs = Obscomm()
        self.scoreboard = Scoreboard(list(self.entrants.keys()), saveData=scoreboardData)

        pyautogui.PAUSE = .2
        self.assertAoe2Running()

    def runSim(self):
        self.obs.split('scoreboard', self.scoreboard.getScoreStrings(self.entrants), size=9)

        for homeName, awayName in self.scoreboard.getNextMatch():
            home, away = self.entrants[homeName], self.entrants[awayName]
            self.generateScenario(home, away)
            self.obs.set('victory', '')
            result = self.runBattle()
            while result == 0:
                print('Inconclusive match, regenerating scenario file')
                self.obs.set('victory', 'Battle Inconclusive')
                self.generateScenario(home, away)
                self.obs.set('victory', '')
                result = self.runBattle()

            if result == -1:
                print('%s defeats %s' % (away.display, home.display))
                self.obs.set('victory', '%s defeats %s' % (away.display, home.display))
                self.scoreboard.result(away.name, home.name)
            elif result == 1:
                print('%s defeats %s' % (home.display, away.display))
                self.obs.set('victory', '%s defeats %s' % (home.display, away.display))
                self.scoreboard.result(away.name, home.name)

            self.obs.split('scoreboard', self.scoreboard.getScoreStrings(self.entrants), size=9)
            yield

        print('End of generation results:')
        for score in self.scoreboard.getScoreStrings(self.entrants):
            print(score)
        self.obs.set('victory', 'Winner: %s' % self.scoreboard.getBest())
        time.sleep(10)  # Take a moment to pause on the winner screen
        return None

    # Run battle with existing script file and return:
    #  1 for home team win
    #  0 for inconclusive result
    #  -1 for away team win
    def runBattle(self):
        # (Hopefully) click within the AoE window
        pyautogui.click(1000, 1000, button='left')

        # Open menu and select 'Restart' and 'Yes'
        pyautogui.press('f10')
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
        initialActions = self.armyPatrolString(1, HOME_SPAWN, AWAY_SPAWN) + \
            self.armyPatrolString(2, AWAY_SPAWN, HOME_SPAWN) + \
            '\nEfft_ChangeView(1, [%d,%d]);' % (int((HOME_SPAWN[0] + AWAY_SPAWN[0])/2)-1, int((HOME_SPAWN[1] + AWAY_SPAWN[1])/2))

        subDict = {
            'SetPlayerNames': '\nSetPlayerName(1, "%s");' % home.display + '\nSetPlayerName(2, "%s");' % away.display,
            'AddUnitsTechs': self.unitCreationString(home.comp, 1, HOME_SPAWN) + self.unitCreationString(away.comp, 2, AWAY_SPAWN),
            'InitialActions': initialActions
        }

        with open('./php_scx/ScenarioTemplate.php', 'r') as templateFile:
            result = Template(templateFile.read()).substitute(subDict)
            with open('./php_scx/Scenario.php', 'w') as outfile:
                outfile.write(result)

        # Generate scenario, needs to be called twice
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)
        time.sleep(6)   # If we don't wait it breaks, maybe AoE2 is reading scenario before it's done compiling

        self.obs.set('home-comp', home.getArmyCompStrings())
        self.obs.set('away-comp', away.getArmyCompStrings())
        homeRecord = self.scoreboard.getRecord(home)
        awayRecord = self.scoreboard.getRecord(away)
        self.obs.set('home-display', '%s  %d-%d' % (home.display, homeRecord[0], homeRecord[1]))
        self.obs.set('away-display', '%d-%d  %s' % (awayRecord[0], awayRecord[1], away.display))

    def imageIsLine(self, im):
        pixels = [im.getpixel((x, 0)) for x in range(im.width)]
        for p in pixels:
            if p != pixels[0]:
                return False
        return True

    def unitCreationString(self, comp, playerNum, coords):
        output = ''
        for unit, count in comp.items():
            unitData = UNIT_DATA[unit]

            if 'tech' in unitData['type']:
                output += '\nEfft_Research(%d, %d);' % (playerNum, unitData['id'])
            else:
                for i in range(count):
                    output += '\nNewObject(%d, %d, [%d, %d], 0);' % (
                        playerNum,
                        unitData['id'],
                        coords[0],
                        coords[1]
                    )
        return output

    def armyPatrolString(self, playerNum, coords, enemyCoords):
        return '\nEfft_PatrolO(%d, Area(%d, %d, %d, %d), %s);' % (
            playerNum,
            coords[0]-4,
            coords[1]-4,
            coords[0]+4,
            coords[1]+4,
            enemyCoords
        )

    def assertAoe2Running(self):
        found = False
        for pid in psutil.pids():
            try:
                if psutil.Process(pid).name() == "AoK HD.exe":
                    found = True
            except psutil.NoSuchProcess:
                pass
        if not found:
            raise RuntimeError("AoE2 HD must be running with the arena scenario.")
