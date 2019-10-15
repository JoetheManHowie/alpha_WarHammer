# WarHammer

## What we have

This repository holds the code necessary to run a python script that out puts a random warhammer character with few steps left to compelte manually.

The other piece of code needed for this to work is the class Dice.py
And the five pickles.

## Installation

We will need python 3 installed for these programs to run.
If you don't have python I recommend installing Anaconda, because it's the bomb digity!
You need to install the following as well:

- `conda install numpy`
- `conda install pandas`
- `pip install reportlab`

## How to use this code

- First download: Make_a_warhammer_PC.py, Dice.py, career_table.pickle, hair_table.pickle, classes_table.pickle , eye_table.pickle, RandTalent_table.pickle
- Second: run the following command to generate a character `./Make_a_warhammer_PC.py --race='Wood Elf' --career='Witch Hunter' --pdf=myNewCharacter.pdf > myNewCharacter.txt`

- the three arguments can be changed or left blank.
- the last part of thr line saves the output to a txt file

The code will also output a fillable pdf of your character sheet that can be modified.
The only parts left that you must do maually are explained in the txt file output.





