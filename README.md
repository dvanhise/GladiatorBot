## GladiatorBot
Genetic algorithm to select an ideal army composition in an Age of Empires 2 scenario.  Testing the armies is automated via generating and running scenarios in the game.

## Setup
# Warning - The way this project was put together is not very conducive to a clean setup.  The following list is almost certainly incomplete with regards to getting it working in your computer.
* Install Python and PHP
* Install python libraries: pip install -r requirements.txt
* Change SCX::$scenarios_path in Compiler.php
* Add Immobile Units AI (http://aok.heavengames.com/blacksmith/showfile.php?fileid=4122) to AoE2 AI folder
* Start AoE2HD and run a generated arena scenario with both players set to "Immobile AI" and all other settings as desired and let it finish and leave it in the finished state
* Run gladiatorBot: python main.py

# Special thanks to:
* AzZzRu
* Vehemos
* Leif Ericson
* Sparks