from army import Army
from simulation import Simulation
from settings import POP_SIZE, BOT_DATA, SAVE_DIR
import os
import random


def main():
    armies = []
    for bot in BOT_DATA[:POP_SIZE]:
        armies.append(Army(bot))

    # Fill out rest of population with completely random bots
    for x in range(POP_SIZE - len(armies)):
        armies.append(Army())

    sim = Simulation()

    try:
        with open(os.path.join(SAVE_DIR, 'gen.txt'), 'r') as genFile:
            gen = int(genFile.read())
    except FileNotFoundError:
        gen = 1

    while True:
        print("Starting generation %d" % gen)
        sim.setEntrants(armies)
        sim.runSim()

        # Use results to generate army fitness roulette
        rouletteWheel = []
        for army in armies:
            rouletteWheel += [army] * army.wins

        # Save new army genes to file
        nextGenArmies = [army.makeChild(random.choice(rouletteWheel)) for army in armies]
        armies = nextGenArmies
        for army in armies:
            army.save()

        gen += 1
        with open(os.path.join(SAVE_DIR, 'gen.txt'), 'w') as genFile:
            genFile.write(str(gen))


if __name__ == "__main__":
    main()
