#!/usr/bin/env python

from Dice import DiceSet
import numpy as np
import pandas as pd
import pickle


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

    master_map = touch_my_pickle("career_table.pickle")
    career_class = touch_my_pickle("classes_table.pickle")
    # TIME TO ROLL
    d = DiceSet()
    roll = d.d100
    print("career roll = " +str(roll))
    my_possible_careers = master_map[race]
    for career, nums in my_possible_careers.items():
        if roll in nums:
            return career, career_class[career]

        
def touch_my_pickle(pickle_file):
    pickle_in = open(pickle_file, "rb")
    my_dic = pickle.load(pickle_in)
    return my_dic

    
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

    # Calc wounds
    SB = int(your_abScore['S']/10)
    TB = int(your_abScore['T']/10)
    WPB = int(your_abScore['WP']/10)
    your_abScore['Wounds'] = int(SB + (2*TB) + WPB)
    
    count = 0
    for lif in afterWounds[race]:
        your_abScore[AFW[count]] = lif
        count += 1

    yeeBoo = pd.DataFrame.from_dict(your_abScore, orient = 'index')
    return yeeBoo

        
if __name__ == '__main__':
    Race = GetRace()
    abScore = GetAbScore(Race)
    myJob, myClass = GetAJob(Race)
    print(r'You are a %s %s, working as a %s' %(Race, myClass, myJob))
    print(abScore)
    print()

