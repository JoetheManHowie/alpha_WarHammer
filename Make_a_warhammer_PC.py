#!/usr/bin/env python3

## ex: ./Make_a_warhammer_PC.py --race= --career='Witch Hunter' > myNewCharacter.txt

import sys
from Dice import DiceSet
import numpy as np
import pandas as pd
from pickle import load


def main():
        try:
                args = sys.argv
                Race = args[1][7:]
                abScore = ''
                myJob = args[2][9:]
                myClass = ''
                if Race=='' and myJob=='':
                        Race = GetRace()
                        abScore = GetAbScore(Race)
                        myJob, myClass = GetAJob(Race)
                elif myJob=='' and Race!='':
                        abScore = GetAbScore(Race)
                        myJob, myClass = GetAJob(Race)
                elif Race=='' and myJob!='':
                        Race = GetRace() 
                        abScore = GetAbScore(Race)
                        myClass = GetMyClass(myJob)
                else:
                        Race = GetRace() 
                        abScore = GetAbScore(Race)
                        myJob, myClass = GetAJob(Race)
        except KeyError:
                print("Incorrect input, must be in the form:\n./Make_a_warhammer_PC.py --race='Dwarf' --career='Miner'")
                print("If you want random race and/or career leave it blank:\n./Make_a_warhammer_PC.py --race= --career=")
                exit()
        race_skills = GetRaceSkills(Race)
        race_talents = GetRaceTalents(Race)
        age, height, eye, hair = PhysicalFeatures(Race)
        traps = GetClassTrappings(myClass)
        
        #### Print results ####

        for args in (("RACE:", Race), ("CLASS:", myClass), ("CAREER:", myJob)):
                print("{0:<10} {1:<10}".format(*args))
                
        print(abScore)
        print("\nSKILLS:\t(Pick three with 3 pts Advance, and three with 5 pts Advance):")
        [print("\t%s" %sk) for sk in race_skills ]
        print("Go to your Career Path and Spend 40 pts Advance on your starting skills \n\
(Max 10pts per skill with these points) Note there is enough Advance \n\
to put 5 pts in each skill in your starting class (which is required to level up)!\n")
        print("TALENTS: (Humans & Halfling, Random Talents are rolled for you):")
        [print("\t%s" %ta) for ta in race_talents ]
        print("Note: if any doubles occurred, you may re-roll.\n\
Go to your Career Path Take ONE talent from your starting career path.\n")
                
                
        print("Physical Features:")
        for args in (("Age:", age), ("Height:", str(int(height))+" cm"), ("Eye Color:", eye), ("Hair Color:", hair)):
                print("\t{0:<15} {1:<15}".format(*args))
        
        print("\nTrappings: (You also get the trappings from your career)")
        [print('\t%s' %itm) for itm in traps]
        
        return 0


def GetRace():
        d = DiceSet()
        race_roll = d.d100
        # print('race roll = ' +str(race_roll))
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
        return 0
        

def GetMyClass(job):
        cc = touch_my_pickle("classes_table.pickle")
        return cc[job]

        
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
        # print("career roll = " +str(roll))
        my_possible_careers = master_map[race]
        for career, nums in my_possible_careers.items():
                if roll in nums:
                        return career, career_class[career]
                
        
        return 0
        
        
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
        your_abScore['Wounds'] = "SB + 2*TB + WPB = %d + %d + %d = %2d" %(SB, (2*TB), WPB, absNums['Wounds'])
        
        count = 0
        for lif in afterWounds[race]:
                your_abScore[AFW[count]] = str(lif)
                count += 1
        
        
        return pd.DataFrame.from_dict(your_abScore, orient = 'index')


def GetClassTrappings(Class):
        trap = {'ACADEMICS': ['Clothing', 'Dagger', 'Pouch',
                              'Sling Bag containing Writing Kit and 1d10 sheets of Parchment'],
                'BURGHERS':  ['Cloak', 'Clothing', 'Dagger',
                              'Hat', 'Pouch', 'Sling Bag containing Lunch'],
                'COURTIERS': ['Dagger', 'Fine Clothing',
                              'Pouch containing Tweezers, Ear Pick, and a Comb'],
                'PEASANTS':  ['Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Sling Bag containing Rations (1 day)'],
                'RANGERS':   ['Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Backpack containing Tinderbox, Blanket, Rations (1 day)'],
                'RIVERFOLK': ['Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Sling Bag containing a Flask of Spirits'],
                'ROGUES':    ['Clothing', 'Dagger', 'Pouch',
                              'Sling Bag containing 2 Candles, 1d10 Matches, a Hood or Mask'],
                'WARRIORS':  ['Clothing', 'Hand Weapon', 'Dagger', 'Pouch'] }
        return trap[Class]


def GetRaceTalents(race):
        race_talent = {"Human":    ['Doomed', 'Savvy or Suave', '3 Random Talents'],
                       "Dwarf":    ['Magic Resistance', 'Night Vision', 'Read/Write or Relentless',
                                    'Resolute or Strong-minded', 'Sturdy'],
                       "Halfling": ['Acute Sense (Taste)', 'Night Vision', 'Resistance (Chaos)',
                                    'Small', '2 Random Talents'],
                       "High Elf": ['Acute Sense (Sight)', 'Coolheaded or Savvy', 'Night Vision',
                                    'Second Sight or Sixth Sense', 'Read/Write'],
                       "Wood Elf": ['Acute Sense (Sight)', 'Hardy or Second Sight', 'Night Vision',
                                    'Read/Write or Very Resilient', 'Rover'] }
        these_tal = race_talent[race]
        isRand = these_tal[-1].split()
        if len(isRand)>1:
                these_tal = these_tal[:-1]
                numRT = int(isRand[0])
                randTab = touch_my_pickle("RandTalent_table.pickle")
                i=0
                while i < numRT:
                        d = DiceSet()
                        my_roll = d.d100
                        for tal, nums in randTab.items():
                                if my_roll in nums:
                                        these_tal.append(tal)
                                        
                        i+=1
                
        return these_tal

        
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


def PhysicalFeatures(race):
        eye_table = touch_my_pickle("eye_table.pickle")
        eye_roll = DiceSet().d10 + DiceSet().d10
        eye_color = ''
        for color, nums in eye_table[race].items():
                if eye_roll in nums:
                        eye_color = color
                
        
        hair_table = touch_my_pickle("hair_table.pickle")
        hair_roll = DiceSet().d10 + DiceSet().d10
        hair_color = ''
        for color, nums in hair_table[race].items():
                if hair_roll in nums:
                        hair_color = color
                
        
        age = 0;
        height = 0;
        if race == 'Human':
                age = 15 + DiceSet().d10
                height = 2.54*(4*12 + 9 + sum([DiceSet().d10 for i in range(0, 2)])) 
        elif race == "Dwarf":
                age = 15 + sum([DiceSet().d10 for i in range(0, 10)])
                height = 2.54*(4*12 + 3 + DiceSet().d10) 
        elif race == "Halfling":
                age = 15 + sum([DiceSet().d10 for i in range(0, 5)])
                height = 2.54*(5*12+11+ DiceSet().d10) 
        else:
                age = 30 + sum([DiceSet().d10 for i in range(0, 10)])
                height = 2.54*(3*12 +1 + DiceSet().d10) 
                
        return (age, height, eye_color, hair_color)


if __name__ == '__main__':
        main()
