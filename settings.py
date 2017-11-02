import yaml

# Genetic algorithm variables
POP_SIZE = 20
MUT_RATE = .01
CROSSOVER_RATE = .8
MUT_AMOUNT = .2

# Strongest army challenge variables
WOOD = 1500
FOOD = 1500
GOLD = 2000

SAVE_DIR = './save'

UNIT_DATA_PATH = './units.yaml'
BOT_DATA_PATH = './bots.yaml'

AOE2_PATH = 'E:/jdownloads/historytourpics/historytourpics/Microsoft Games/Age of Empires II/Age2_x1/age2_x2.exe'
# INPUT_SCENARIO

# Load data files and keep them available
with open(UNIT_DATA_PATH, 'r') as f:
    UNIT_DATA = yaml.load(f)
with open(BOT_DATA_PATH, 'r') as f:
    BOT_DATA = [bot for bot in yaml.load_all(f)]
