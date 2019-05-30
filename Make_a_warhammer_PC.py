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


def convert2Int(species):
    '''This function takes an arrray of strings with elements in the form
    '55' or '6-9'. The function turns the array into a list of lists in the form
    [[6, 7, 8, 9], ..., [55]]'''
    
    new_list = []
    for num in species:
        # \u2013 is the unicode for the en dash character
        if (u'\u2013' in num ):
            # skips the no number entries
            if(num == u'\u2013'):
                # we need the array length to stay the same
                # so that it is still one to one with
                # the careers array
                new_list.append([])
                continue
            # splits the string and fills in the missing numbers
            rang = num.split(u'\u2013')
            minNum = int(rang[0])
            maxNum = int(rang[1])
            this_entry = []
            for i in range(minNum, maxNum +1):
                this_entry.append(i)

            new_list.append(this_entry)
        # checks for regular dash otherwise same as above
        elif('-' in num):
             # skips the no number entries
            if(num == '-'):
                new_list.append([])
                continue
            # splits the string and fills in the missing numbers
            rang = num.split('-')
            minNum = int(rang[0])
            maxNum = int(rang[1])
            this_entry = []
            for i in range(minNum, maxNum +1):
                this_entry.append(i)

            new_list.append(this_entry)
        # just a number string
        else:
            new_list.append([int(num)])
    
    return new_list
           

def Make_a_Dick(careers, values):
    new_dic = {}
    nn = len(careers)
    for i in range(0, nn):
        new_dic[careers[i]] = values[i]
    return new_dic


def GetAJob(race):
    # need 5 tables of careers, one for each race
    # there are Careers which are grouped in sets called Classes
    # each races has a dictionary
    # in that dic the career is the KEY and
    # the VALUE is a list of numbers corresponding
    # to the Career ex: human_careers = {..., 'Nun': [4, 5], ...}
    # Then you can look up the Class in the Class dic
    # ex: human_classes = {'Academic': [..., 'Nun',...], ...}
    
        
    TCT = pd.read_csv('CareerTable.csv', dtype = str)

    #print(TCT)
    # convert to arrays of strings, which are the
    # converted to arrays of lists of int's
    classes = TCT["Class"].values
    careers = TCT["Career/Species"].values
    humans = convert2Int(TCT["Human"].values)
    halflings = convert2Int(TCT["Halfling"].values)
    dwarves = convert2Int(TCT["Dwarf"].values)
    highElves = convert2Int(TCT["High Elf"].values)
    woodElves = convert2Int(TCT["Wood Elf"].values)

    # makes a map of classes to careers
    Classes_for_careers = {}
    this_occu = 'butts'
    for i in range(0, len(classes)):
        this_class = str(classes[i])
        if(this_class != 'nan'):
            this_occu = this_class
        elif(this_class == 'nan'):
            classes[i] = this_occu

    career_class = Make_a_Dick(careers, classes)
        
    
    # makes a map of the maps for each race
    master_map = {}
    master_map['Human'] =Make_a_Dick(careers, humans)
    master_map['Halfling'] = Make_a_Dick(careers, halflings)
    master_map['Dwarf'] = Make_a_Dick(careers, dwarves)
    master_map['High Elf'] = Make_a_Dick(careers, highElves)
    master_map['Wood Elf'] = Make_a_Dick(careers, woodElves)

    # TIME TO ROLL
    d = DiceSet()
    roll = d.d100
    print("career roll = " +str(roll))
    my_possible_careers = master_map[race]
    for career, nums in my_possible_careers.items():
        if roll in nums:
            return career, career_class[career]


    
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

