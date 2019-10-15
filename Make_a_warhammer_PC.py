#!/usr/bin/env python3

# Joe Howie, Updated Oct 12th, 2019
# War Hammer fantasy 4ed Character Sheet Generator
# ./Make_a_warhammer_PC.py --race='Wood Elf' --career='Witch Hunter' --pdf=myNewCharacter.pdf > myNewCharacter.txt

import pdfrw                           
import sys
import numpy as np
import pandas as pd
from Dice import DiceSet
from pickle import load
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import white, black 

def main():
        try:
                args = sys.argv
                Race = args[1][7:]
                #print(Race)
                abScore = ''
                myJob = args[2][9:]
                #print(myJob)
                filename = args[3][6:]
                myClass = ''
                thres = 3
                if len(filename) < thres:
                        filename = 'out.pdf'
                if len(Race) < thres and len(myJob) < thres:
                        #print('no race or career')
                        Race = GetRace()
                        myJob, myClass = GetAJob(Race)
                elif len(myJob)<thres and len(Race)>thres:
                        #print('race but no job')
                        myJob, myClass = GetAJob(Race)
                elif len(Race)<thres and len(myJob)>thres:
                        #print('job but no race')
                        Race = GetRace() 
                        myClass = GetMyClass(myJob)

                myClass = GetMyClass(myJob)
                abScore, ABS = GetAbScore(Race)
                race_skills = GetRaceSkills(Race)
                race_talents = GetRaceTalents(Race)
                age, height, eye, hair = PhysicalFeatures(Race)
                traps = GetClassTrappings(myClass)
                
                #### Print results ####
                
                for args in (("RACE:", Race), ("CLASS:", myClass), ("CAREER:", myJob)):
                        print("{0:<10} {1:<10}".format(*args))
                        
                print(pd.DataFrame.from_dict(abScore, orient = 'index'))
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

                
                
                ### Create pdf ## needs to come last
                create_simple_form(filename, Race, myClass, myJob, age, int(height), eye, hair, ABS, race_talents, traps)
                return 0


        except KeyError:
                print("Incorrect input, must be in the form:\n./Make_a_warhammer_PC.py --race='Dwarf' --career='Miner'")
                print("If you want random race and/or career leave it blank:\n./Make_a_warhammer_PC.py --race= --career=")
                exit()

                
                

def create_simple_form(pdf, race, Class, job, age, height, eye, hair, ABS, talent, traps):
        c = canvas.Canvas(pdf)
        curry = 820
        c.setFont("Courier", 20)
        c.drawCentredString(300, curry, 'War Hammer Character Sheet')
        c.setFont("Courier", 14)
        form = c.acroForm
        ### Top of page 1
        # character name
        curry -= 30
        c.drawString(10, curry, 'Name:')
        curry -= 5
        next_insert(form, 50, curry, 200, 20, "")
        # species
        curry += 5
        c.drawString(250, curry, 'Species:')
        curry -= 5
        next_insert(form, 320, curry, 100, 20, race)
        # class
        curry += 5
        c.drawString(420, curry, 'Class:') 
        curry -= 5
        next_insert(form, 470, curry, 100, 20, Class) 

        #career
        curry -=30
        c.drawString(10, curry, 'Career:')   
        curry -= 5
        next_insert(form, 70, curry, 180, 20, job)
        # career level
        curry += 5
        c.drawString(260, curry, 'Career Level:')   
        curry -= 5
        next_insert(form, 370, curry, 200, 20, '')

        # career path
        curry -=30
        c.drawString(10, curry, 'Career Path:')   
        curry -= 5
        next_insert(form, 110, curry, 280, 20, '')
        # status
        curry += 5
        c.drawString(410, curry, 'Status:')   
        curry -= 5
        next_insert(form, 470, curry, 100, 20, '')

        # Age
        curry -=30
        c.drawString(10, curry, 'Age:')   
        curry -= 5
        next_insert(form, 50, curry, 60, 20, str(age))
        # height
        curry += 5
        c.drawString(115, curry, 'Height:')   
        curry -= 5
        next_insert(form, 180, curry, 100, 20, str(height)+" cm")
        # Hair
        curry += 5
        c.drawString(285, curry, 'Hair:')   
        curry -= 5
        next_insert(form, 330, curry, 100, 20, hair)
        # eyes
        curry += 5
        c.drawString(440, curry, 'Eye:')   
        curry -= 5
        next_insert(form, 475, curry, 95, 20, eye)

        ## Characterisitcs
        curry -= 20
        c.drawString(60, curry, 'Characterisitcs')   
        c.drawString(290, curry, 'Fate')
        c.drawString(360, curry, 'Resilience')
        c.drawString(485, curry, 'Experience')   
        ## abs
        c.setFont("Courier", 12)
        curry -= 20
        ab = ('WS', 'BS', 'S', 'T', 'I', 'AG', 'Dex', 'Int', 'WP', 'Fel')
        spacing = (13, 39, 67, 92, 117, 139, 160, 186, 215, 235)
        for i in range(0, len(ab)):
                c.drawString(spacing[i], curry, ab[i])   
        
        curry -= 22
        i = 10
        j=0
        while i < 240:
                next_insert(form, i, curry, 22, 20, str(int(ABS[ab[j]])))
                i +=25
                j +=1
        
        curry -= 20
        i = 10
        while i < 240:
                next_insert(form, i, curry, 22, 20,'')
                i +=25
        
        curry -= 20
        i = 10
        j = 0
        while i < 240:
                next_insert(form, i, curry, 22, 20, str(int(ABS[ab[j]])))
                i +=25
                j += 1
        
        # Fate
        curry += 60
        c.drawString(270, curry, 'Fate:')
        curry -= 5
        next_insert(form, 330, curry, 15, 20, str(int(ABS['Fate'])))
        curry -= 15
        c.drawString(270, curry, 'Fortune:')
        curry -= 5
        next_insert(form, 330, curry, 15, 20, str(int(ABS['Fate'])))
        # Resilience
        curry += 25
        c.drawString(355, curry, 'Resilience:')
        curry -= 5
        next_insert(form, 440, curry, 15, 20, str(int(ABS['Resilience'])))
        curry -= 15
        c.drawString(355, curry, 'Resolve:')
        curry -= 5
        next_insert(form, 440, curry, 15, 20, str(int(ABS['Resilience'])))
        # Experience
        curry += 25
        c.drawString(465, curry, 'Current:')
        curry -= 5
        next_insert(form, 530, curry, 50, 20, '')
        curry -= 15
        c.drawString(465, curry, 'Total:')
        curry -= 5
        next_insert(form, 510, curry, 70, 20, '')
        # Movement
        curry -= 10
        c.drawString(360, curry, 'Movement:')
        curry -= 20
        c.drawString(270, curry, 'Movement:')
        curry -=5
        next_insert(form, 350, curry, 22, 20, str(int(ABS['Movement'])))
        curry += 5
        c.drawString(385, curry, 'Walk:')
        curry -=5
        next_insert(form, 435, curry, 22, 20, str(2*int(ABS['Movement'])))
        curry += 5
        c.drawString(470, curry, 'Run:')
        curry -=5
        next_insert(form, 510, curry, 22, 20, str(4*int(ABS['Movement'])))
        curry -=30
        # Basic Skills & Advanced Skills
        tbs = 15
        c.setFont("Courier", 14)
        c.drawString(80, curry, 'Basic Skills')
        c.drawString(320, curry, 'Grouped & Advanced Skills')
        curry -= tbs
        c.setFont("Courier", 12)
        c.drawString(10, curry, 'Name             | Charac. | Adv')
        c.drawString(310, curry, 'Name             | Charac. | Adv')
        #
        sl = [('Art              | Dex     |', 'Dex'),
              ('Athletics        | Ag      |', 'AG'),
              ('Bribery          | Fel     |', 'Fel'),
              ('Charm            | Fel     |', 'Fel'),
              ('Charm Animal     | WP      |', 'WP'),
              ('Climb            | S       |', 'S'),
              ('Cool             | WP      |', 'WP'),
              ('Consume Alcohol  | T       |', 'T'),
              ('Dodge            | Ag      |', 'AG'),
              ('Drive            | Ag      |', 'AG'),
              ('Endurance        | T       |', 'T'),
              ('Entertain        | Fel     |', 'Fel'),
              ('Gamble           | Int     |', 'Int'),
              ('Gossip           | Fel     |', 'Fel'),
              ('Haggle           | Fel     |', 'Fel'),
              ('Intimidate       | S       |', 'S'),
              ('Intuition        | I       |', 'I'),
              ('Leadership       | Fel     |', 'Fel'),
              ('Melee (Basic)    | WS      |', 'WS'),
              ('Melee            | WS      |', 'WS'),
              ('Navigation       | I       |', 'I'),
              ('Outdoor Survival | Int     |', 'Int'),
              ('Perception       | I       |', 'I'),
              ('Ride             | Ag      |', 'AG'),
              ('Row              | S       |', 'S'),
              ('Stealth          | Ag      |', 'AG')]
        blank= '                 |         |'
        curry -=5 
        for sk, ab in sl:
                curry -= tbs
                c.drawString(10, curry, sk)
                c.drawString(310, curry, blank)
                curry -=5
                next_insert(form, 180, curry, 22, 20, str(int(ABS[ab])))
                next_insert(form, 217, curry, 22, 20, '')
                # advanced
                next_insert(form, 310, curry, 120, 20, '')
                next_insert(form, 442, curry, 35, 20, '')
                next_insert(form, 482, curry, 22, 20, '')
                next_insert(form, 517, curry, 22, 20, '')
        

        c.showPage()

        ## Page 2

        ## Talents
        c.setFont("Courier", 14)
        curry = 820
        c.drawString(150, curry, 'Talents')
        c.drawString(420, curry, 'Trappings')
        curry -= tbs
        c.setFont("Courier", 12)
        c.drawString(10, curry, 'Talent Name         | T. | Description')
        c.drawString(380, curry, 'Name                  | Enc')
        
        count = 0
        for ta in talent:
                #print(ta)
                curry -= tbs*2
                next_insert(form, 10, curry, 150, 20, ta)
                next_insert(form, 165, curry, 22, 20, '')
                next_insert(form, 200, curry, 175, 20, '')
                count+=1
        curry +=tbs*2*count
        count2 = 0
        for itm in traps:
                #print(itm)
                curry -= tbs*2
                next_insert(form, 380, curry, 160, 20, itm)
                next_insert(form, 550, curry, 22, 20, '')
                count2 +=1

                
        pad = abs(count - count2)
        e = 0
        #print(count, count2, pad)
        curry +=tbs*2*pad
        if count > count2:
                curry -=2*tbs
                while e < pad:
                        curry -=2*tbs
                        next_insert(form, 380, curry, 160, 20, '')
                        next_insert(form, 550, curry, 22, 20, '')
                        e+=1
        elif count < count2:
                while e < pad:
                        curry -=2*tbs
                        next_insert(form, 10, curry, 150, 20, '')
                        next_insert(form, 165, curry, 22, 20, '')
                        next_insert(form, 200, curry, 175, 20, '')                
                        e +=1
        e=max(count,count2)
        while e < 11:
                curry -=2*tbs
                next_insert(form, 10, curry, 150, 20, '')
                next_insert(form, 165, curry, 22, 20, '')
                next_insert(form, 200, curry, 175, 20, '')                
                next_insert(form, 380, curry, 160, 20, '')
                next_insert(form, 550, curry, 22, 20, '')
                e +=1
        
        
        # Ambitions
        c.setFont("Courier", 14)
        curry -= 15
        c.drawString(100, curry, 'Personal Ambitions')
        c.drawString(380, curry, 'Party Ambitions')
        curry -= 20
        L =['ST:', 'LT:']
        for g in L:
                c.drawString(10, curry, g)
                c.drawString(300, curry, g)
                curry -= 5
                next_insert(form, 40, curry, 250, 20, '')
                next_insert(form, 325, curry, 250, 20, '')
                curry -= 15
        
        # Armour
        c.drawString(250, curry, 'Armour')
        curry -= 20
        c.setFont('Courier', 12)
        c.drawString(10, curry, 'Name                 | Location | Enc | AP | Qualities')
        for i in range(0, 6):
                curry -= 25
                next_insert(form, 10, curry, 150, 20, '')
                next_insert(form, 177, curry, 55, 20, '')
                next_insert(form, 252, curry, 25, 20, '')
                next_insert(form, 290, curry, 30, 20, '')
                next_insert(form, 330, curry, 250, 20, '')
                

        ## body
        curry -=25
        c.drawString(10, curry, "Head: ")
        curry -=5
        next_insert(form, 44, curry, 22, 20, '')
        curry +=5
        c.drawString(68, curry, "| Left Arm: ")
        curry -=5
        next_insert(form, 147, curry, 22, 20, '')
        curry +=5
        c.drawString(171, curry, "| Right Arm: ")
        curry -=5
        next_insert(form, 258, curry, 22, 20, '')
        curry +=5
        c.drawString(285, curry, "| Body: ")
        curry -=5
        next_insert(form, 337, curry, 22, 20, '')
        curry +=5
        c.drawString(363, curry, "| Left Leg: ")
        curry -=5
        next_insert(form, 443, curry, 22, 20, '')
        curry +=5
        c.drawString(470, curry, "| Right Leg: ")
        curry -=5
        next_insert(form, 558, curry, 22, 20, '')
        curry -= 20
        curry +=5
        c.drawString(470, curry, "| Shield: ")
        curry -=5
        next_insert(form, 558, curry, 22, 20, '')

        c.drawString(250, curry, 'Weapons')
        curry -= 20
        c.setFont('Courier', 12)
        c.drawString(10, curry, 'Name                 | Group | Enc | R/R | Danage | Qualities')
        for i in range(0, 6):
                curry -= 25
                next_insert(form, 10, curry, 150, 20, '')
                next_insert(form, 169, curry, 50, 20, '')
                next_insert(form, 233, curry, 25, 20, '')
                next_insert(form, 267, curry, 40, 20, '')
                next_insert(form, 313, curry, 60, 20, '')
                next_insert(form, 377, curry, 213, 20, '')
        
        c.showPage()
        
        ## Page 3
        cash = ('| D:', '| SS:', '| GC:')
        space = ((70, 100), (130, 170), (200, 240))
        curry = 820
        c.setFont('Courier', 14)
        c.drawString(10, curry, 'Wealth:')
        c.setFont('Courier', 12)
        i = 0
        for a, b in space:
                c.drawString(a, curry, cash[i])
                curry -=5
                next_insert(form, b, curry, 25, 20, '')
                curry +=5
                i +=1

        c.setFont('Courier', 14)
        c.drawString(275, curry, '| Encumbrance: | Max:    | Total:')
        curry -=5
        next_insert(form, 455, curry, 25, 20, str(int(ABS['Enc'])))
        next_insert(form, 555, curry, 25, 20, '')
        curry -= 25

        # Wounds
        c.drawString(10, curry, 'Wounds:')
        c.setFont('Courier', 12)
        c.drawString(70, curry, '| Total:     | Current:     | Critical: ')
        curry -= 5
        next_insert(form, 132, curry, 25, 20, str(int(ABS['Wounds'])))
        next_insert(form, 242, curry, 25, 20, str(int(ABS['Wounds'])))
        next_insert(form, 355, curry, 25, 20, '0')
        curry -= 25
        c.setFont('Courier', 14)
        c.drawString(10, curry, 'Conditions:')
        curry -= 5
        next_insert(form, 110, curry, 470, 20, '')
        curry -= 25
        # Curruptions and Mutations
        c.drawString(10, curry, 'Insanities:     | Corruptions:     | Mutations: ')
        curry -= 5
        next_insert(form, 115, curry, 25, 20, '0')
        next_insert(form, 275, curry, 25, 20, '0')
        next_insert(form, 415, curry, 25, 20, '0')
        curry -= 15
        # Notes
        c.drawString(250, curry, 'NOTES')
        i = 0
        curry -=5
        while i < 35:
                curry -= 20
                next_insert(form, 10, curry, 570, 20, '')
                i +=1
        
        c.save()
        
        
def next_insert(form, xpos, ypos, wbox, hbox, val):                     
        form.textfield(value =val, x=xpos, y=ypos, borderStyle='inset',                 
                       borderColor=white, fillColor=white,                  
                       width=wbox, height = hbox, textColor=black) 
        
        
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
        # which are in order of [WS, BS, S, T, I, AG, Dex, Int, WP, Fel, Fate, Resilience, Extra Points, Movement]
        
        AB = ['WS', 'BS', 'S', 'T', 'I', 'AG', 'Dex', 'Int', 'WP', 'Fel']
        if race.endswith("Elf"): race = 'Elf'
        AFW = ['Fate', 'Resilience', 'Extra Points', 'Movement']
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
        
        # Calc wounds & encumb
        SB = int(absNums['S']/10)
        TB = int(absNums['T']/10)
        WPB = int(absNums['WP']/10)
        absNums['Wounds'] = SB+2*TB+WPB
        absNums['Enc'] = SB+TB
        your_abScore['Wounds'] = "SB + 2*TB + WPB = %d + %d + %d = %2d" %(SB, (2*TB), WPB, absNums['Wounds'])
        your_abScore['Enc'] = "SB + TB = %d + %d = %2d" %(SB, (TB), absNums['Enc'])
        
        count = 0
        for lif in afterWounds[race]:
                your_abScore[AFW[count]] = str(lif)
                absNums[AFW[count]] = str(lif)
                count += 1
        
        
        return (your_abScore, absNums)


def GetClassTrappings(Class):
        trap = {'ACADEMICS': ['Clothing', 'Dagger', 'Pouch',
                              'Sling Bag', 'Writing Kit', '1d10 sheets of Parchment'],
                'BURGHERS':  ['Cloak', 'Clothing', 'Dagger',
                              'Hat', 'Pouch', 'Sling Bag', 'Lunch'],
                'COURTIERS': ['Dagger', 'Fine Clothing',
                              'Pouch', 'Tweezers', 'Ear Pick', 'Comb'],
                'PEASANTS':  ['Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Sling Bag', 'Rations (1 day)'],
                'RANGERS':   ['Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Backpack', 'Tinderbox', 'Blanket', 'Rations (1 day)'],
                'RIVERFOLK': ['Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Sling Bag', 'Flask of Spirits'],
                'ROGUES':    ['Clothing', 'Dagger', 'Pouch',
                              'Sling Bag', '2 Candles', '1d10 Matches', 'Hood or Mask'],
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
        if isRand[0] in ('2', '3'):
                these_tal = these_tal[:-1]
                numRT = int(isRand[0])
                randTab = touch_my_pickle("RandTalent_table.pickle")
                i=0
                while i < numRT:
                        d = DiceSet()
                        my_roll = d.d100
                        #print(my_roll)
                        for tal, nums in randTab.items():
                                
                                if my_roll in nums:
                                        #print(tal)
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
                height = 2.54*(3*12 +1 + DiceSet().d10) 
        else:
                age = 30 + sum([DiceSet().d10 for i in range(0, 10)])
                height = 2.54*(5*12+11+ DiceSet().d10) 
                
        return (age, height, eye_color, hair_color)


if __name__ == '__main__':
        main()

        '''
        y = (-30, -5, 5, -5, 5, -5, -30, -5)
        x = (10, 50, 250, 310, 370, 400, 10, 70)
        w = (200, 100, 120, 180)
        fn = ('Name:', 'Species:', 'Class:', 'Career:')
        va = ('', race, Class, job)
        j = 0
        for i in range(0, len(w)):
                curry +=y[j]
                c.drawString(x[j], curry, fn[i])
                j += 1
                curry +=y[j]
                next_insert(form, x[j], curry, w[i], 20, va[i])

        
        '''
