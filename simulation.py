from itertools import combinations
from settings import UNIT_DATA
import yaml
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
        # Create yaml files for the php scenario generator to use
        with open('./php_scx/home.yaml', 'w') as outfile:
            comp = self.convertToPhpScxName(home.getUnitComp())
            yaml.dump(comp, outfile, default_flow_style=False)
        with open('./php_scx/away.yaml', 'w') as outfile:
            comp = self.convertToPhpScxName(away.getUnitComp())
            yaml.dump(comp, outfile, default_flow_style=False)

        # Generate scenario, needs to be called twice
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)
        subprocess.call('php .\\php_scx\\Compiler.php', shell=True)

        # Run scenario in AoE2
        return 100

    def convertToPhpScxName(self, comp):
        newComp = {}
        for unit, count in comp.items():
            newComp[('T_' if 'tech' in UNIT_DATA[unit]['type'] else 'U_') + unit.upper().replace('-', '_')] = count
        return newComp
