from army import Army
from simulation import Simulation
from obscomm import Obscomm
from genome import Genome
from settings import POP_SIZE, BOT_DATA, SAVE_FILE, SAVE_DIR
import os
import random
import yaml


def main():
    armies = []
    scoreboardData = None

    try:
        with open(SAVE_FILE, 'r') as saveFile:
            data = yaml.load(saveFile)
            if not data:
                raise FileNotFoundError
        gen = data['gen']
        for bot in BOT_DATA[:POP_SIZE]:
            armies.append(Army(bot, Genome(data['armies'][bot['name']])))
        scoreboardData = data

    except FileNotFoundError:
        gen = 1

        # Initial bots from bots.yaml
        for bot in BOT_DATA[:POP_SIZE]:
            armies.append(Army(bot))

        # Fill out rest of population with completely random bots
        for x in range(POP_SIZE - len(armies)):
            armies.append(Army())

    sim = Simulation(armies, scoreboardData)
    while True:
        print('Starting generation %d' % gen)
        Obscomm().set('gen', 'Generation %d' % gen)

        for a in sim.runSim():
            with open(SAVE_FILE, 'w') as saveFile:
                saveData = {
                    'gen': gen,
                    'armies': {army.name: dict(army.getGenome()) for army in armies},
                    **sim.scoreboard.getSaveData()
                }
                yaml.dump(saveData, saveFile, default_flow_style=False)

        # Use results to generate army fitness roulette
        rouletteWheel = []
        best = findIn(armies, sim.scoreboard.getBest())
        for army in armies:
            rouletteWheel += [army] * sim.scoreboard.getRecord(army.name)[0]
        record = sim.scoreboard.getRecord(best.name)
        # Save data on winning bot for analysis
        with open(os.path.join(SAVE_DIR, 'gen%d-winner.txt' % gen), 'w') as winFile:
            winFile.write('%s (%s)' % (best.display, best.name))
            winFile.write('Record: %d-%d' % (record[0], record[1]))
            winFile.write('Army Composition:')
            winFile.write('\n'.join(best.getArmyCompStrings()))

        # Save new army genes to file
        nextGenArmies = [army.makeChild(random.choice(rouletteWheel)) for army in armies]
        armies = nextGenArmies
        for army in armies:
            army.save()

        gen += 1
        sim = Simulation(armies)


def findIn(armies, name):
    for army in armies:
        if army.name == name:
            return army

if __name__ == "__main__":
    main()
