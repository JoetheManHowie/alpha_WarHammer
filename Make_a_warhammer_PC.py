#!/home/joe/anaconda3/bin/python

from Dice import DiceSet
import numpy as np
import pandas as pd


def GetRace():
    d = DiceSet()
    race_roll = d.d100
    print('race roll = ' +str(race_roll))
    if race_roll < 91:
        return 'Human'
    elif race_roll > 90 and race_roll < 95:
        return 'Halfling'
    elif race_roll > 94 and race_roll < 99:
        return 'Dwarf'
    elif race_roll == 99:
        return 'High Elf'
    else:
        return 'Wood Elf'



def GetAJob(race):
    # need 5 tables of careers, one for each race
    # there are Careers which are grouped in sets called Classes
    # each races has a dictionary
    # in that dic the career is the KEY and
    # the VALUE is a list of numbers corresponding
    # to the Career ex: human_careers = {..., 'Nun': [4, 5], ...}
    # Then you can look up the Class in the Class dic
    # ex: human_classes = {'Academic': [..., 'Nun',...], ...}
    TCT = pd.read_csv('CareerTable.csv')
    print(TCT.info())
    # this should convert the dtype...FML
    TCT["Career/Species"] = TCT['Career/Species'].astype('str') 
    print(TCT["Career/Species"].dtype)
    # print(TCT.head())
           #Class Career/Species  Human  Dwarf Halfling High Elf Wood Elf
# 0  ACADEMICS     Apothecary     01     01       01    01–02        –
# 1        NaN       Engineer     02  02–04       02        –        –
# 2        NaN         Lawyer     03  05–06    03–04    03–06        –
# 3        NaN            Nun  04-05      –        –        –        –
# 4        NaN      Physician     06     07    05–06    07–08        –

   # print(TCT.loc[:, ["Career/Species", "Human"]])
   # print(TCT.loc[:, ["Career/Species", "Wood Elf"]])
   # print(TCT.loc[:, ["Career/Species", "High Elf"]])
   # print(TCT.loc[:, ["Career/Species", "Halfling"]])
   # print(TCT.loc[:, ["Career/Species", "Dwarf"]])
    
    

def GetAbScore(race):
    # need 5 tables for the ability scores, one for each race option
    # make a dictionary with races as keys.
    # the dictionary stores the ab score rudrics that races rolls
    # the arrays in the are the modifiers to the 2d10 roll
    # which are in order of [WS, BS, S, T, I, AG, Dex, Int, WP, Fel, Fate, Resiliance, Extra Points, Movement]

    AB = ['WS', 'BS', 'S', 'T', 'I', 'AG', 'Dex', 'Int', 'WP', 'Fel']
    if race.endswith("Elf"): race = 'Elf'
    AFW = ['Fate', 'Resiliance', 'Extra Points', 'Movement']
    options = { "Human":    np.ones(10)*20,
                "Halfling": np.array([10, 30, 10, 20, 20, 20, 30, 20, 30, 30]),
                "Dwarf":    np.array([30, 20, 20, 30, 20, 10, 30, 20, 40, 10]),
                "Elf":      np.array([30, 30, 20, 20, 40, 30, 30, 30, 30, 20])
                }
    afterWounds = { "Human":    np.array([2, 1, 3, 4]),
                    "Halfling": np.array([0, 2, 3, 3]),
                    "Dwarf":    np.array([0, 2, 2, 3]),
		    "Elf":      np.array([0, 0, 2, 5])
		}

    
    your_abScore = {}
    count = 0
    for mod in options[race]:
        d = DiceSet()
        your_abScore[AB[count]] = 2*d.d10 +mod
        count += 1

    your_abScore['Wounds'] = "SB + (2 x TB) + WPB"
    
    count = 0
    for lif in afterWounds[race]:
        your_abScore[AFW[count]] = lif
        count += 1

    return your_abScore

        
if __name__ == '__main__':
    Race = GetRace()
    print(Race)
    abScore = GetAbScore(Race)
    print(abScore)
    GetAJob(Race)
    
    
