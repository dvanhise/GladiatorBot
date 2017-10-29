from army import Army
from simulation import Simulation
from settings import POP_SIZE, BOT_DATA


def main():
    armies = []
    for bot in BOT_DATA:
        armies.append(Army(bot))

    # Fill out rest of population with completely random bots
    for x in range(POP_SIZE - len(armies)):
        armies.append(Army())

    sim = Simulation()

    # gen = 1
    # while True:
    #     sim.setEntrants(armies)
    #     results = sim.runSim()
    #
    #     # Use results to generate army fitness roulette
    #     # Save new army genes to file
    #     nextGenArmies = [army.makeChild(armies[5]) for army in armies]
    #     armies = nextGenArmies
    #     for army in armies:
    #         army.save()
    #     gen += 1

    sim.setEntrants(armies)
    results = sim.runSim()


if __name__ == "__main__":
    main()
