#!/usr/bin/env python3

from Dice import DiceSet
import numpy as np
import pandas as pd
from pickle import load


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
    my_dic = load(pickle_in)
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
                "Elf":      np.array([30, 30, 20, 20, 40, 30, 30, 30, 30, 20]) }
    
    afterWounds = { "Human":    np.array([2, 1, 3, 4]),
                    "Halfling": np.array([0, 2, 3, 3]),
                    "Dwarf":    np.array([0, 2, 2, 3]),
		    "Elf":      np.array([0, 0, 2, 5]) }

    
    your_abScore = {}
    absNums = {}
    count = 0
    for mod in options[race]:
        d = DiceSet()
        e = DiceSet()
        r1 = e.d10; r2 = d.d10
        absNums[AB[count]] = r1+r2+mod
        your_abScore[AB[count]] = "2d10 + mod = %2d + %2d + %2d = %2d" %(r1, r2, mod, absNums[AB[count]])

        count += 1

    # Calc wounds
    SB = int(absNums['S']/10)
    TB = int(absNums['T']/10)
    WPB = int(absNums['WP']/10)
    absNums['Wounds'] = SB+2*TB+WPB
    your_abScore['Wounds'] = "SB +2*TB + WPB = %d + %d + %d = %2d" %(SB, (2*TB), WPB, absNums['Wounds'])
    
    count = 0
    for lif in afterWounds[race]:
        your_abScore[AFW[count]] = str(lif)
        count += 1


    return pd.DataFrame.from_dict(your_abScore, orient = 'index')


def GetRaceTalents(race):
    race_talent = {"Human":   ['Doomed', 'Savvy or Suave', '3 Random Talents'],
                   "Dwarf":    ['Magic Resistance', 'Night Vision', 'Read/Write or Relentless',
                                'Resolute or Strong-minded', 'Sturdy'],
                   "Halfling": ['Acute Sense (Taste)', 'Night Vision', 'Resistance (Chaos)',
                                'Small', '2 Random Talents'],
                   "High Elf": ['Acute Sense (Sight)', 'Coolheaded or Savvy', 'Night Vision',
                                'Second Sight or Sixth Sense', 'Read/Write'],
                   "Wood Elf": ['Acute Sense (Sight)', 'Hardy or Second Sight', 'Night Vision',
                                'Read/Write or Very Resilient', 'Rover'] }
    return race_talent[race]
    

def GetRaceSkills(race):
    race_skill = {"Human":    ['Animal Care', 'Charm, Cool', 'Evaluate', 'Gossip', 'Haggle',
                               'Language (Bretonnian)', 'Language (Wastelander)', 'Leadership',
                               'Lore (Reikland)', 'Melee (Basic)', 'Ranged (Bow)'],
                  "Dwarf":    ['Consume Alcohol', 'Cool', 'Endurance', 'Entertain (Storytelling)',
                               'Evaluate', 'Intimidate', 'Language (Khazalid)', 'Lore (Dwarfs)',
                               'Lore (Geology)', 'Lore (Metallurgy)', 'Melee (Basic)', 'Trade (any one)'], 

                  "Halfling": ['Charm', 'Consume Alcohol', 'Dodge', 'Gamble', 'Haggle',
                               'Intuition', 'Language (Mootish)', 'Lore (Reikland)', 'Perception',
                               'Sleight of Hand', 'Stealth (Any)', 'Trade (Cook)' ],

                  "High Elf": ['Cool', 'Entertain (Sing)', 'Evaluate', 'Language (Eltharin)',
                               'Leadership', 'Melee (Basic)', 'Navigation', 'Perception',
                               'Play (anyone)', 'Ranged (Bow)', 'Sail', 'Swim'],
                  "Wood Elf": ['Athletics', 'Climb', 'Endurance', 'Entertain (Sing)',
                               'Intimidate', 'Language (Eltharin)', 'Melee (Basic)', 'Outdoor'
                               'Survival', 'Perception', 'Ranged (Bow)', 'Stealth (Rural)', 'Track'] }
    return race_skill[race]


if __name__ == '__main__':
    Race = GetRace()
    abScore = GetAbScore(Race)
    myJob, myClass = GetAJob(Race)
    race_skills = GetRaceSkills(Race)
    race_talents = GetRaceTalents(Race)
    
    #### Print results ####
    print('RACE: %s, CLASS: %s, CAREER: %s' %(Race, myClass, myJob))
    print(abScore)
    print("\nSKILLS:\t(Pick three with 3 pts Advantage, and three with 5 pts Advantage):")
    [print("\t%s" %sk) for sk in race_skills ]
    print("Go to your Career Path and Spend 40 pts Advantage on your starting skills \n\
(Max 10pts per skill with these points) Note there is enough Advantage \n\
to put 5 pts in each skill in your starting class (which is required to level up)!\n")
    print("TALENTS: (Go to page 37 of the handbook for the Random Talent Table):")
    [print("\t%s" %ta) for ta in race_talents ]
    print("Go to your Career Path Take ONE talent from your starting career path.\n")
