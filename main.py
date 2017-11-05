from army import Army
from simulation import Simulation
from settings import POP_SIZE, BOT_DATA, SAVE_DIR
import os
import random


def getArmyByName(armies, name):
    for army in armies:
        if army.name == name:
            return army
    raise ValueError


def main():
    armies = []
    for bot in BOT_DATA:
        armies.append(Army(bot))

    # Fill out rest of population with completely random bots
    for x in range(POP_SIZE - len(armies)):
        armies.append(Army())

    sim = Simulation()

    try:
        with open(os.path.join(SAVE_DIR, 'gen.txt'), 'r') as genFile:
            gen = genFile.read()
    except FileNotFoundError:
        gen = 1

    while True:
        sim.setEntrants(armies)
        results = sim.runSim()

        # Use results to generate army fitness roulette
        rouletteWheel = []
        for army, wins in results.items():
            rouletteWheel += [getArmyByName(armies, army)] * wins

        # Save new army genes to file
        nextGenArmies = [army.makeChild(random.choice(rouletteWheel)) for army in armies]
        armies = nextGenArmies
        for army in armies:
            army.save()

        gen += 1
        with open(os.path.join(SAVE_DIR, 'gen.txt'), 'w') as genFile:
            genFile.write(gen)


if __name__ == "__main__":
    main()
