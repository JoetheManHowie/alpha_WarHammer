#!/usr/bin/env python3

# Joe Howie, Updated Oct 12th, 2019
# War Hammer fantasy 4ed Character Sheet Generator
#######  Example  ############
# ./Make_a_warhammer_PC.py --race= --career= --filename=
# pdf & txt default name: out.pdf & out.txt

# ./Make_a_warhammer_PC.py --race=Human --career='Witch Hunter' --filename=myNewCharacter
# pdf & txt named: myNewCharacter.pdf & myNewCharacter.txt
#####################################

import numpy as np
import pdfrw                           
import sys
import os
import numpy as np
import pandas as pd
import random
from pickle import load
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import white, black 

## class
class path():
        def __init__(self, name, status, skills, talents, trappings, page):
                self.name = name
                self.status = status
                self.skills = skills
                self.talents = talents
                self.trappings = trappings
                self.page = page


        def __str__(self):
                return "On page "+ str(self.page)+"\n"+self.name+"--"+self.status 
                        

class armor():
        def __init__(self, loc, enc, ap, qual):
                self.loc = loc
                self.enc = enc
                self.qual = qual
        


def main():
        '''Main calls to create character
        and where the txt file is made'''
        try:
                args = sys.argv
                Race = args[1][7:]
                abScore = ''
                myJob = args[2][9:]
                filename = args[3][11:]
                textfile = args[3][11:]
                myClass = ''
                thres = 1
                if len(filename) < thres:
                        filename = 'out.pdf'
                        textfile = 'out.txt'
                else:
                        filename = filename+".pdf"
                        textfile = textfile+".txt"
                        os.system("touch {}".format(textfile))
                        
                if len(Race) < thres and len(myJob) < thres:
                        Race = GetRace()
                        myJob, myClass = GetAJob(Race)
                elif len(myJob)<thres and len(Race)>thres:
                        myJob, myClass = GetAJob(Race)
                elif len(Race)<thres and len(myJob)>thres:
                        Race = GetRace() 
                        myClass = GetMyClass(myJob)
                        
                ## The meat ##
                myClass = GetMyClass(myJob)
                abScore, ABS = GetAbScore(Race)
                race_skills = GetRaceSkills(Race)
                race_talents = GetRaceTalents(Race)
                age, height, eye, hair = GetPhysicalFeatures(Race)
                traps = GetClassTrappings(myClass)
                cp =  GetCareerData(myClass, myJob)
                cash = GetMoney(cp.status)
                #### Print results to textfile ####
                txt = open(textfile,'w')
                
                for args in (("RACE:", Race), ("CLASS:", myClass), ("CAREER:", myJob)):
                        txt.write("{0:<10} {1:<10}\n".format(*args))
                        
                txt.write("See page "+str(cp.page)+ " for more details\n")
                txt.write(str(pd.DataFrame.from_dict(abScore, orient = 'index')))
                
                txt.write("\n\nSKILLS:\t(Pick three with 3 pts Advance, and three with 5 pts Advance):\n")
                [txt.write("\t%s\n" %sk) for sk in race_skills ]
                txt.write("FROM CAREER: (you get 40 advances between the eight, with a max of 10 in any one skill)\n")
                #[txt.write("\t%s\n" %sk) for sk in cp.skills ]
                '''txt.write("Go to your Career Path and Spend 40 pts Advance on your starting skills \n\
        (Max 10pts per skill with these points) Note there is enough Advance \n\
        to put 5 pts in each skill in your starting class (which is required to level up)!\n")'''

                txt.write("TALENTS: (Humans & Halfling, Random Talents are rolled for you):\n")
                [txt.write("\t%s\n" %ta) for ta in race_talents ]
                txt.write("FROM CAREER: (pick ONE)\n")
                [txt.write("\t%s\n" %ta) for ta in cp.talents ]
                txt.write("Note: if any doubles occurred, you may re-roll.\n\
        Go to your Career Path Take ONE talent from your starting career path.\n")
                
                
                txt.write("Physical Features:\n")
                for args in (("Age:", age), ("Height:", str(int(height))+" cm"), ("Eye Color:", eye), ("Hair Color:", hair)):
                        txt.write("\t{0:<15} {1:<15}\n".format(*args))
                        
                txt.write("\nTrappings: (You also get the trappings from your career)\n")
                [txt.write('\t%s\n' %itm) for itm in traps]
                
                [txt.write('\t%s\n' %itm) for itm in cp.trappings]
                g, s, c = cash
                txt.write('You have: %d gold, %d silver, and %d copper\n' %(g, s, c))
                
                txt.close()
                
                ### Create pdf ## needs to come last
                getCharacterSheet(filename, Race, myClass, myJob, age, int(height), eye, hair, ABS, race_talents, traps, cp, cash)
                return 0


        except KeyError:
                print("Incorrect input, must be in the form:\n./Make_a_warhammer_PC.py --race='Dwarf' --career='Miner'")
                print("If you want random race and/or career leave it blank:\n./Make_a_warhammer_PC.py --race= --career=")
                exit()

                

def D(n):
        return random.randint(1, n)

                
def binary_search(itm_list, itm):
        first = 0
        last = len(itm_list)-1
        found = False
        while (first <= last and found == False):
                mid = (first + last)//2                
                if (itm_list[mid] == itm):
                        found = True
                else:
                        if itm < itm_list[mid]:
                                last = mid - 1
                        else:
                                first = mid + 1
                        
                
        
        return found


def GetMoney(status):
        ''' returns a tuple with (gold, silver, copper)'''
        cl, cn = status.split(' ')
        cn = int(cn)
        if (cl =="Brass"):
                return (sum([D(10) for i in range(0, 2*cn)]), 0, 0)
        elif (cl == 'Silver'):
                return (0, sum([D(10) for i in range(0, cn)]), 0)
        else:
                return (0, 0, cn)
        


def getCharacterSheet(pdf, race, Class, job, age, height, eye, hair, ABS, talent, traps, cp, cash):
        c = canvas.Canvas(pdf)
        curry = 820
        c.setFont("Courier", 20)
        c.drawCentredString(300, curry, 'Warhammer Character Sheet')
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
        next_insert(form, 370, curry, 200, 20, "See page "+str(cp.page))

        # career path
        curry -=30
        c.drawString(10, curry, 'Career Path:')   
        curry -= 5
        next_insert(form, 110, curry, 280, 20, cp.name)
        # status
        curry += 5
        c.drawString(410, curry, 'Status:')   
        curry -= 5
        next_insert(form, 470, curry, 100, 20, cp.status)

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
        c.setFont('Courier', 14)
        c.drawString(360, curry, 'Movement:')
        c.setFont('Courier', 12)
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

        curry -=15
        c.drawString(190, curry, 'Extra Points:')
        curry -=5
        next_insert(form, 290, curry, 15, 20, str(int(ABS['Extra Points'])))
        curry += 5
        curry -=15
        #curry -=30

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
        sl = (('Art              | Dex     |', 'Dex'),
              ('Athletics        | Ag      |', 'AG'),
              ('Bribery          | Fel     |', 'Fel'),
              ('Charm            | Fel     |', 'Fel'),
              ('Charm Animal     | WP      |', 'WP'),
              ('Climb            | S       |', 'S'),
              ('Consume Alcohol  | T       |', 'T'),
              ('Cool             | WP      |', 'WP'),
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
              ('Stealth          | Ag      |', 'AG'))
        blank= '                 |         |'
        curry -=5 
        # race skills
        bas = []
        ass = []
        bs = 0
        all_sk = [s.split("|")[0].rstrip() for s,_ in sl]
        #print (all_sk)
        for skill in cp.skills:
                in_list = binary_search(all_sk, skill)
                if (in_list):
                        bas.append(skill)
                else:
                        ass.append(skill)
        
        #print(bas, ass)
        for i in range(0, len(all_sk)):
                sk, ab = sl[i]
                curry -= tbs
                c.drawString(10, curry, sk)
                c.drawString(310, curry, blank)
                curry -=5
                in_list = binary_search(bas, all_sk[i])
                if (in_list):
                        next_insert(form, 180, curry, 22, 20, str(int(ABS[ab])))
                        next_insert(form, 217, curry, 22, 20, '5')
                else:
                        next_insert(form, 180, curry, 22, 20, str(int(ABS[ab])))
                        next_insert(form, 217, curry, 22, 20, '')
                # advanced
                if len(ass) >0:
                        next_insert(form, 310, curry, 120, 20, ass[0])
                        next_insert(form, 442, curry, 35, 20, '')
                        next_insert(form, 482, curry, 22, 20, '')
                        next_insert(form, 517, curry, 22, 20, '5')
                        ass = ass[1:]
                else:
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
        # career talents
        rtal = str(cp.talents)
        talent.append(rtal)
        for ta in talent:
                #print(ta)
                curry -= tbs*2
                next_insert(form, 10, curry, 150, 20, ta)
                next_insert(form, 165, curry, 22, 20, '')
                next_insert(form, 200, curry, 175, 20, '')
                count+=1
        curry +=tbs*2*count

        # pull out these item for later
        armour = ['Leather Breastplate',
                  'Leather Jack',
                  'Leather Jerkin',
                  'Leather Leggings',
                  'Mail Shirt']
        # location enc ap qualities
        a_stat = {'Leather Breastplate': ('Body', '2', '2', 'Weakpoints'),
                  'Leather Jack': ('Arms, Body', '1', '1', ''),
                  'Leather Jerkin': ('Body', '1', '1', ''),
                  'Leather Leggings': ('Legs', '1', '1', ''),
                  'Mail Shirt': ('Body', '2', '2', 'Flexible')}
        # group enc r/r damage qualities
        weapons = ['Axe',
                   'Dagger',
                   'Flail',
                   'Knuckledusters',
                   'Hand Weapon',
                   'Hand Weapon (Boat Hook)',
                   'Rapier',
                   'Hand Weapon (Sword)',
                   'Shield',
                   'Weapon (Any Melee)' ]
        w_stat =  {'Axe': ['Basic', '1', 'Average', 'SL+SB+4', ''],
                   'Dagger': ['Basic', '0', 'Varies', 'SL+SB+2', ''],
                   'Flail': ['Flail', '1', 'Average', 'SL+SB+5', 'Distract, Wrap'],
                   'Knuckledusters': ['Brawling', '0', 'Personal', 'SL+SB+2', ''],
                   'Hand Weapon': ['Basic', '1', 'Average', 'SL+SB+4', ''],
                   'Hand Weapon (Boat Hook)': ['Basic', '1', 'Average', 'SL+SB+4', ''],
                   'Rapier': ['Fencing', '1', 'Long', 'SL+SB+4', 'Fast, Impale'],
                   'Hand Weapon (Sword)': ['Basic', '1', 'Average', 'SL+SB+4', ''],
                   'Shield': ['Basic', '1', 'Very Short', 'SL+SB+2', 'Shield 2, Defensive, Undamaging'],
                   'Weapon (Any Melee)':['', '', '', '', ''] }

        # career trappings
        count2 = 0
        traps = list(traps)
        traps.extend(list(cp.trappings))
        traps.sort()
        any_a = []
        any_w = []
        while len(weapons) > 0:
                itm = weapons[0]
                in_weapons = binary_search(traps, itm)
                if in_weapons:
                        traps.remove(itm)
                        any_w.append(itm)

                weapons = weapons[1:]   

        while len(armour) > 0:
                itm = armour[0]
                in_armor = binary_search(traps, itm)
                if in_armor:
                        traps.remove(itm)
                        any_a.append(itm)
                armour = armour[1:]

        
        for itm in traps:
                curry -= tbs*2
                next_insert(form, 380, curry, 160, 20, itm)
                next_insert(form, 550, curry, 22, 20, '')
                count2 +=1

                
        pad = abs(count - count2)
        e = 0
        # special cases
        if (curry == 715 and pad*2*tbs): curry +=tbs*2
        else:                            curry +=tbs*2*pad
        
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
        left = len(any_a)
        while len(any_a) != 0:
                curry -= 25
                key = any_a[0]
                values = a_stat[key]
                next_insert(form, 10, curry, 150, 20, key)
                next_insert(form, 177, curry, 55, 20, values[0])
                next_insert(form, 252, curry, 25, 20, values[1])
                next_insert(form, 290, curry, 30, 20, values[2])
                next_insert(form, 330, curry, 250, 20, values[3])
                any_a = any_a[1:]
        
        for i in range(left, 6):
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
        #print(any_w)
        left = len(any_w)
        while len(any_w) != 0:
                curry -= 25
                key = any_w[0]
                values = w_stat[key]
                next_insert(form, 10, curry, 150, 20, key)
                next_insert(form, 169, curry, 50, 20, values[0])
                next_insert(form, 233, curry, 25, 20, values[1])
                next_insert(form, 267, curry, 40, 20, values[2])
                next_insert(form, 313, curry, 60, 20, values[3])
                next_insert(form, 377, curry, 213, 20, values[4])
                any_w = any_w[1:]
                
        for i in range(left, 6):
                curry -= 25
                next_insert(form, 10, curry, 150, 20, '')
                next_insert(form, 169, curry, 50, 20, '')
                next_insert(form, 233, curry, 25, 20, '')
                next_insert(form, 267, curry, 40, 20, '')
                next_insert(form, 313, curry, 60, 20, '')
                next_insert(form, 377, curry, 213, 20, '')
        
        c.showPage()
        
        ## Page 3
        cash_d = ('| D:', '| SS:', '| GC:')
        space = ((70, 100), (130, 170), (200, 240))
        curry = 820
        c.setFont('Courier', 14)
        c.drawString(10, curry, 'Wealth:')
        c.setFont('Courier', 12)
        i = 0
        for a, b in space:
                c.drawString(a, curry, cash_d[i])
                curry -=5
                next_insert(form, b, curry, 25, 20, str(cash[i]))
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
        race_roll = D(100)
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
        cc = touch_my_pickle("Pickles/classes_table.pickle")
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
        
        master_map = touch_my_pickle("Pickles/career_table.pickle")
        career_class = touch_my_pickle("Pickles/classes_table.pickle")
        # TIME TO ROLL
        roll = D(100)
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
                r1 = D(10)
                r2 = D(10)
                absNums[AB[count]] = r1+r2+mod
                your_abScore[AB[count]] = "2d10 + mod = %2d + %2d + %2d = %2d" %(r1, r2, mod, absNums[AB[count]])
                
                count += 1
        
        # Calc wounds & encumb
        SB = int(absNums['S']/10)
        TB = int(absNums['T']/10)
        WPB = int(absNums['WP']/10)
        if race == 'Halfling': absNums['Wounds'] = 2*TB+WPB
        else:                  absNums['Wounds'] = SB+2*TB+WPB
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
        trap = {'ACADEMICS': ('Clothing', 'Dagger', 'Pouch',
                              'Sling Bag', 'Writing Kit', str(D(10)) +' sheets of Parchment'),                'BURGHERS':  ('Cloak', 'Clothing', 'Dagger',
                              'Hat', 'Pouch', 'Sling Bag', 'Lunch'),
                'COURTIERS': ('Dagger', 'Fine Clothing',
                              'Pouch', 'Tweezers', 'Ear Pick', 'Comb'),
                'PEASANTS':  ('Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Sling Bag', 'Rations (1 day)'),
                'RANGERS':   ('Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Backpack', 'Tinderbox', 'Blanket', 'Rations (1 day)'),
                'RIVERFOLK': ('Cloak', 'Clothing', 'Dagger',
                              'Pouch', 'Sling Bag', 'Flask of Spirits'),
                'ROGUES':    ('Clothing', 'Dagger', 'Pouch',
                              'Sling Bag', '2 Candles', str(D(10))+' Matches', 'Hood or Mask'),
                'WARRIORS':  ('Clothing', 'Hand Weapon', 'Dagger', 'Pouch') }
        return trap[Class]


def GetCareerData(Class, career):
        Ca_path = {"ACADEMICS": {'Apothecary': path('Apothecary’s Apprentice',
                                                    'Brass 3',
                                                    ('Consume Alcohol',
                                                     'Heal',
                                                     'Language (Classical)',
                                                     'Lore (Chemistry)',
                                                     'Lore (Medicine)',
                                                     'Lore (Plants)',
                                                     'Trade (Apothecary)',
                                                     'Trade (Poisoner)'),
                                                    ('Concoct',
                                                     'Craftsman (Apothecary)',
                                                     'Etiquette (Scholar)',
                                                     'Read/Write)'),
                                                    ('Book (Blank)',
                                                     'Healing Draught',
                                                     'Leather Jerkin',
                                                     'Pestle and Mortar'), 53),
                                 'Engineer': path('Student Engineer',
                                                  'Brass 4',
                                                  ('Consume Alcohol',
                                                   'Cool',
                                                   'Endurance',
                                                   'Language (Classical)',
                                                   'Lore (Engineer)',
                                                   'Perception',
                                                   'Ranged (Blackpowder)',
                                                   'Trade (Engineer)'),
                                                  ('Artistic', 
                                                   'Gunner',
                                                   'Read/Write',
                                                   'Tinker'),
                                                  ('Book (Engineer)',
                                                   'Hammer and Spikes'), 54),
                                 'Lawyer': path('Student Lawyer',
                                                'Brass 4',
                                                ('Consume Alcohol',
                                                 'Endurance',
                                                 'Haggle',
                                                 'Language (Classical)',
                                                 'Lore (Law)',
                                                 'Lore (Theology)',
                                                 'Perception',
                                                 'Research'),
                                                ('Blather',
                                                 'Etiquette (Scholar)',
                                                 'Read/Write',
                                                 'Speedreader'),
                                                ('Book (Law)',
                                                 'Magnifying Glass'), 55),
                                 'Nun': path('Novitiate',
                                             'Brass 1',
                                             ('Art (Calligraphy)',
                                              'Cool',
                                              'Endurance',
                                              'Entertain (Storyteller)',
                                              'Gossip',
                                              'Heal',
                                              'Lore (Theology)',
                                              'Pray'),
                                             ('Bless (Any)',
                                              'Stone Soup',
                                              'Panhandle',
                                              'Read/Write'),
                                             ('Religious Symbol',
                                              'Robes'), 56),
                                 'Physician': path('Physician`s Apprentice',
                                                   'Brass 4',
                                                   ('Bribery',
                                                    'Cool',
                                                    'Drive',
                                                    'Endurance',
                                                    'Gossip',
                                                    'Heal',
                                                    'Perception',
                                                    'Sleight of Hand'),
                                                   ('Bookish',
                                                    'Field Dressing',
                                                    'Read/Write',
                                                    'Strike to Stun'),
                                                   ('Bandages',
                                                    'Healing Draught'), 57),
                                 'Priest': path('Initiate',
                                                'Brass 2',
                                                ('Athletics',
                                                 'Cool',
                                                 'Endurance',
                                                 'Intuition',
                                                 'Lore (Theology)',
                                                 'Perception',
                                                 'Pray',
                                                 'Research'),
                                                ('Bless (Any)',
                                                 'Holy Visions',
                                                 'Read/Write',
                                                 'Suave'),
                                                ('Religious Symbol',
                                                 'Robes'), 58),
                                 'Scholar': path('Student',
                                                 'Brass 3',
                                                 ('Consume Alcohol',
                                                  'Entertain (Storytelling)',
                                                  'Gamble',
                                                  'Gossip',
                                                  'Haggle',
                                                  'Language (Classical)',
                                                  'Lore (Any)',
                                                  'Research'),
                                                  ('Carouser',
                                                   'Read/Write',
                                                   'Savvy',
                                                   'Super Numerate'),
                                                 ('Alcohol',
                                                  'Book',
                                                  'Opinions',
                                                  'Writing Kit'), 59),
                                 'Wizard': path('Wizard`s Apprentice',
                                                'Brass 3',
                                                ('Channelling (Any Colour)',
                                                 'Dodge',
                                                 'Intuition',
                                                 'Language (Magick)',
                                                 'Lore (Magic)',
                                                 'Melee (Basic)',
                                                 'Melee (Polearm)',
                                                 'Perception'),
                                                ('Aethyric Attunement',
                                                 'Petty Magic',
                                                 'Read/Write',
                                                 'Second Sight'),
                                                ('Grimoire',
                                                 'Quarterstaff'), 60) },
                   "BURGHERS":  {'Agitator': path('Pamphleteer',
                                                  'Brass 1',
                                                  ('Art (Writing)',
                                                   'Bribery',
                                                   'Charm',
                                                   'Consume Alcohol',
                                                   'Gossip',
                                                   'Haggle',
                                                   'Lore (Politics)',
                                                   'Trade (Printing)'),
                                                  ('Blather',
                                                   'Gregarious',
                                                   'Panhandle',
                                                   'Read/Write'),
                                                  ('Writing Kit',
                                                   'Hammer and Nails',
                                                   'Pile of Leaflets'), 61),
                                 'Artisan': path('Apprentice Artisan',
                                                 'Brass 2',
                                                 ('Athletics',
                                                  'Cool',
                                                  'Consume Alcohol',
                                                  'Dodge',
                                                  'Endurance',
                                                  'Evaluate',
                                                  'Stealth (Urban)',
                                                  'Trade (Any)'),
                                                 ('Artistic',
                                                  'Craftsman (any)',
                                                  'Strong Back',
                                                  'Very Strong'),
                                                 ('Chalk',
                                                  'Leather Jerkin',
                                                  str(D(10))+' rags'), 62),
                                 'Beggar': path('Pauper',
                                                'Brass 0',
                                                ('Athletics',
                                                 'Charm',
                                                 'Consume Alcohol',
                                                 'Cool',
                                                 'Dodge',
                                                 'Endurance',
                                                 'Intuition',
                                                 'Stealth (Urban)'),
                                                ('Panhandle',
                                                 'Resistance (Disease)',
                                                 'Stone Soup',
                                                 'Very Resilient'),
                                                ('Poor Quality Blanket',
                                                 'Cup'), 63),
                                 'Investigator': path('Sleuth',
                                                      'Silver 1',
                                                      ('Charm',
                                                       'Climb',
                                                       'Cool',
                                                       'Gossip',
                                                       'Intuition',
                                                       'Perception',
                                                       'Stealth (Urban)',
                                                       'Track'),
                                                      ('Alley Cat',
                                                       'Beneath Notice',
                                                       'Read/Write',
                                                       'Sharp'),
                                                      ('Lantern',
                                                       'Lamp Oil',
                                                       'Journal',
                                                       'Quill and Ink'), 64),
                                 'Merchant': path('Trader',
                                                  'Silver 2',
                                                  ('Animal Care',
                                                   'Bribery',
                                                   'Charm',
                                                   'Consume Alcohol',
                                                   'Drive',
                                                   'Gamble',
                                                   'Gossip',
                                                   'Haggle'),
                                                  ('Blather',
                                                   'Dealmaker',
                                                   'Read/Write',
                                                   'Suave'),
                                                  ('Abacus',
                                                   'Mule and Cart',
                                                   'Canvas Tarpaulin',
                                                   str(sum([D(10) for i in range(0, 3)]))+' Silver Shillings'), 65),
                                 'Rat Catcher': path('Rat Hunter',
                                                     'Brass 3',
                                                     ('Athletics',
                                                      'Animal Training (Dog)',
                                                      'Charm Animal',
                                                      'Consume Alcohol',
                                                      'Endurance',
                                                      'Melee (Basic)',
                                                      'Ranged (Sling)',
                                                      'Stealth (Underground or Urban)'),
                                                     ('Night Vision',
                                                      'Resistance (Disease)',
                                                      'Strike Mighty Blow',
                                                      'Strike to Stun'),
                                                     ('Sling with Ammunition',
                                                      'Sack',
                                                      'Small but Vicious Dog'), 66),
                                 'Townsman': path('Clerk',
                                                  'Silver 1',
                                                  ('Charm',
                                                   'Climb',
                                                   'Consume Alcohol',
                                                   'Drive',
                                                   'Dodge',
                                                   'Gamble',
                                                   'Gossip',
                                                   'Haggle'),
                                                   ('Alley Cat',
                                                    'Beneath Notice',
                                                    'Etiquette (Servants)',
                                                    'Sturdy'),
                                                  ('Lodgings',
                                                   'Sturdy Boots'), 67),
                                 'Watchman': path('Watch Recruit',
                                                  'Brass 3',
                                                  ('Athletics',
                                                   'Climb',
                                                   'Consume Alcohol',
                                                   'Dodge',
                                                   'Endurance',
                                                   'Gamble',
                                                   'Melee (Any)',
                                                   'Perception'),
                                                  ('Drilled',
                                                   'Hardy',
                                                   'Strike to Stun',
                                                   'Tenacious'),
                                                  ('Hand Weapon',
                                                   'Leather Jack',
                                                   'Uniform'), 68)},
                   "COURTIERS": {'Advisor': path('Aide',
                                                 'Silver 2',
                                                 ('Bribery',
                                                  'Consume Alcohol',
                                                  'Endurance',
                                                  'Gossip',
                                                  'Haggle',
                                                  'Language (Classical)',
                                                  'Lore (Politics)',
                                                  'Perception'),
                                                 ('Beneath Notice', 
                                                  'Etiquette (Any)',
                                                  'Gregarious',
                                                  'Read/Write'),
                                                 ('Writing Kit',), 69),
                                 'Artist': path('Apprentice Artist',
                                                'Silver 1',
                                                ('Art (Any)',
                                                 'Cool',
                                                 'Consume Alcohol',
                                                 'Evaluate',
                                                 'Endurance',
                                                 'Gossip',
                                                 'Perception',
                                                 'Stealth (Urban)'),
                                                ('Artistic',
                                                 'Sharp',
                                                 'Strong Back',
                                                 'Tenacious'),
                                                ('Brush or Chisel or Quill Pen',), 70),
                                 'Duellist': path('Fencer',
                                                  'Silver 3',
                                                  ('Athletics',
                                                   'Dodge',
                                                   'Endurance',
                                                   'Heal',
                                                   'Intuition',
                                                   'Language (Classical)',
                                                   'Melee (Any)',
                                                   'Perception'),
                                                  ('Beat Blade',
                                                   'Distract',
                                                   'Feint',
                                                   'Step Aside'),
                                                  ('Rapier',
                                                   'Sling Bag containing Clothing', 
                                                   str(D(10))+' Bandages'), 71),
                                 'Envoy': path('Herald',
                                               'Silver 2',
                                               ('Athletics',
                                                'Charm',
                                                'Drive',
                                                'Dodge',
                                                'Endurance',
                                                'Intuition',
                                                'Ride (Horse)',
                                                'Row'),
                                               ('Blather',
                                                'Etiquette (Nobles)',
                                                'Read/Write',
                                                'Suave'),
                                               ('Leather Jack',
                                                'Livery',
                                                'Scroll Case'), 72),
                                 'Noble': path('Scion',
                                               'Gold 1',
                                               ('Bribery',
                                                'Consume Alcohol',
                                                'Gamble',
                                                'Intimidate',
                                                'Leadership',
                                                'Lore (Heraldry)',
                                                'Melee (Fencing)',
                                                'Play (Any)'),
                                               ('Etiquette (Nobles)',
                                                'Luck',
                                                'Noble Blood',
                                                'Read/Write'),
                                               ('Courtly Garb',
                                                'Foil or Hand Mirror',
                                                'Jewellery worth '+ str(sum([D(10) for i in range(0, 3)])) +' gc',
                                                'Personal Servant'), 73 ),
                                 'Servant': path('Menial',
                                                 'Silver 1',
                                                 ('Athletics',
                                                  'Climb',
                                                  'Drive',
                                                  'Dodge',
                                                  'Endurance',
                                                  'Intuition',
                                                  'Perception',
                                                  'Stealth (Any)'),
                                                 ('Beneath Notice',
                                                  'Strong Back',
                                                  'Strong-minded',
                                                  'Sturdy'),
                                                 ('Floor Brush', ), 74),
                                 'Spy': path('Informer',
                                             'Brass 3',
                                             ('Bribery',
                                              'Charm',
                                              'Cool',
                                              'Gamble',
                                              'Gossip',
                                              'Haggle',
                                              'Perception',
                                              'Stealth (Any)'),
                                             ('Blather',
                                              'Carouser',
                                              'Gregarious',
                                              'Shadow'),
                                             ('Charcoal stick',
                                              'Sling Bag containing 2 different sets of clothing',
                                              'Hooded Cloak'), 75),
                                 'Warden': path('Custodian',
                                                'Silver 1',
                                                ('Athletics',
                                                 'Charm Animal',
                                                 'Consume Alcohol',
                                                 'Cool',
                                                 'Endurance',
                                                 'Intuition',
                                                 'Lore (Local)',
                                                 'Perception'),
                                                ('Menacing',
                                                 'Night Vision',
                                                 'Sharp',
                                                 'Strike to Stun'),
                                                ('Keys',
                                                 'Lantern',
                                                 'Lamp Oil',
                                                 'Livery'), 76)},
                   "PEASANTS":  {'Bailiff': path('Tax Collector',
                                                 'Silver 1',
                                                 ('Cool',
                                                  'Dodge',
                                                  'Endurance',
                                                  'Gossip',
                                                  'Haggle',
                                                  'Intimidate',
                                                  'Melee (Basic)',
                                                  'Perception'),
                                                 ('Embezzle',
                                                  'Numismatics',
                                                  'Strong Back',
                                                  'Tenacious'),
                                                 ('Hand Weapon',
                                                  'small lock box'), 77),
                                 'Hedge Witch': path('Hedge Apprentice',
                                                     'Brass 1',
                                                     ('Channelling',
                                                      'Endurance',
                                                      'Intuition',
                                                      'Language (Magick)',
                                                      'Lore (Folklore)',
                                                      'Lore (Herbs)',
                                                      'Outdoor Survival',
                                                      'Perception'),
                                                     ('Fast Hands',
                                                      'Petty Magic',
                                                      'Rover',
                                                      'Strider (Woodlands)'),
                                                     (str(D(10))+' Lucky Charms',
                                                      'Quarterstaff',
                                                      'Backpack'), 78),
                                 'Herbalist': path('Herb Gatherer',
                                                   'Brass 2',
                                                   ('Charm Animal',
                                                    'Climb',
                                                    'Endurance',
                                                    'Lore (Herbs)',
                                                    'Outdoor Survival',
                                                    'Perception',
                                                    'Swim',
                                                    'Trade (Herbalist)'),
                                                   ('Acute Sense (Taste)',
                                                    'Orientation',
                                                    'Rover',
                                                    'Strider (any)'),
                                                   ('Boots',
                                                    'Cloak',
                                                    'Sling Bag containing Assortment of Herbs'), 79),
                                 'Hunter': path('Trapper',
                                                'Brass 2',
                                                ('Charm Animal',
                                                 'Climb',
                                                 'Endurance',
                                                 'Lore (Beasts)',
                                                 'Outdoor Survival',
                                                 'Perception',
                                                 'Ranged (Sling)',
                                                 'Set Trap'),
                                                ('Hardy',
                                                 'Rover',
                                                 'Strider (any)',
                                                 'Trapper'),
                                                ('Selection of Animal Traps',
                                                 'Hand Weapon',
                                                 'Sling with 10 Stone Bullets',
                                                 'Sturdy Boots and Cloak'), 80),
                                 'Miner': path('Prospector',
                                               'Brass 2',
                                               ('Cool',
                                                'Endurance',
                                                'Intuition',
                                                'Lore (Local)',
                                                'Melee (Two-handed)',
                                                'Outdoor Survival',
                                                'Perception',
                                                'Swim'),
                                               ('Rover',
                                                'Strider (Rocky)',
                                                'Sturdy',
                                                'Tenacious'),
                                               ('Charcoal Stick',
                                                'Crude Map',
                                                'Pan',
                                                'Spade'), 81),
                                 'Mystic': path('Fortune Teller',
                                                'Brass 1',
                                                ('Charm',
                                                 'Entertain (Fortune Telling)',
                                                 'Dodge',
                                                 'Gossip',
                                                 'Haggle',
                                                 'Intuition',
                                                 'Perception',
                                                 'Sleight of Hand'),
                                                ('Attractive',
                                                 'Luck',
                                                 'Second Sight',
                                                 'Suave'),
                                                ('Deck of Cards or Dice',
                                                 'Cheap Jewellery'), 82),
                                 'Scout': path('Guide',
                                               'Brass 3',
                                               ('Charm Animal',
                                                'Climb',
                                                'Endurance',
                                                'Gossip',
                                                'Lore (Local)',
                                                'Melee (Basic)',
                                                'Outdoor Survival',
                                                'Perception'),
                                               ('Orientation',
                                                'Rover',
                                                'Sharp',
                                                'Strider (any)'),
                                               ('Hand Weapon',
                                                'Leather Jack',
                                                'Sturdy Boots and Cloak',
                                                'Rope'), 83),
                                 'Villager': path('Peasant',
                                                  'Brass 2',
                                                  ('Animal Care',
                                                   'Athletics',
                                                   'Consume Alcohol',
                                                   'Endurance',
                                                   'Gossip',
                                                   'Melee (Brawling)',
                                                   'Lore (Local)',
                                                   'Outdoor Survival'),
                                                  ('Rover',
                                                   'Strong Back',
                                                   'Strong-minded',
                                                   'Stone Soup'),
                                                  (), 84)},
                   "RANGERS":   {'Bounty Hunter': path('Thief-taker',
                                                       'Silver 1',
                                                       ('Bribery',
                                                        'Charm',
                                                        'Gossip',
                                                        'Haggle',
                                                        'Intuition',
                                                        'Melee (Basic)',
                                                        'Outdoor Survival',
                                                        'Perception'),
                                                       ('Break and Enter',
                                                        'Shadow',
                                                        'Strike to Stun',
                                                        'Suave'),
                                                       ('Hand Weapon',
                                                        'Leather Jerkin',
                                                        'Rope'), 85),
                                 'Coachman': path('Postilion',
                                                  'Silver 1',
                                                  ('Animal Care',
                                                   'Charm Animal',
                                                   'Climb',
                                                   'Drive',
                                                   'Endurance',
                                                   'Perception',
                                                   'Ranged (Entangling)',
                                                   'Ride (Horse)'),
                                                  ('Animal Affinity',
                                                   'Seasoned Traveller',
                                                   'Trick-Riding',
                                                   'Tenacious'),
                                                  ('Warm Coat and Gloves',
                                                   'Whip'), 86),
                                 'Entertainer': path('Busker',
                                                     'Brass 3',
                                                     ('Athletics',
                                                      'Charm',
                                                      'Entertain (Any)',
                                                      'Gossip',
                                                      'Haggle',
                                                      'Perform (Any)',
                                                      'Play (any)',
                                                      'Sleight of Hand'),
                                                     ('Attractive',
                                                      'Mimic',
                                                      'Public-Speaking',
                                                      'Suave'),
                                                     ('Bowl',
                                                      'Instrument'), 87),
                                 'Flagellant': path('Zealot',
                                                    'Brass 0',
                                                    ('Dodge',
                                                     'Endurance',
                                                     'Heal',
                                                     'Intimidate',
                                                     'Intuition',
                                                     'Lore (Sigmar)',
                                                     'Melee (Flail)',
                                                     'Outdoor Survival'),
                                                    ('Berserk Charge',
                                                     'Frenzy',
                                                     'Read/Write',
                                                     'Stone Soup'),
                                                    ('Flail',
                                                     'Tattered Robes'), 88),
                                 'Messenger': path('Runner',
                                                   'Brass 3',
                                                   ('Athletics',
                                                    'Climb',
                                                    'Dodge',
                                                    'Endurance',
                                                    'Gossip',
                                                    'Navigation',
                                                    'Perception',
                                                    'Melee (Brawling)'),
                                                   ('Flee!',
                                                    'Fleet Footed',
                                                    'Sprinter',
                                                    'Step Aside'),
                                                   ('Scroll Case',), 89),
                                 'Pedlar': path('Vagabond',
                                                'Brass 1',
                                                ('Charm',
                                                 'Endurance',
                                                 'Entertain (Storytelling)',
                                                 'Gossip',
                                                 'Haggle',
                                                 'Intuition',
                                                 'Outdoor Survival',
                                                 'Stealth (Rural or Urban)'),
                                                ('Fisherman',
                                                 'Flee!',
                                                 'Rover',
                                                 'Tinker'),
                                                ('Backpack',
                                                 'Bedroll',
                                                 'Goods worth '+str(sum([D(10) for i in range(0, 3)]))+' Brass',
                                                 'Tent'), 90),
                                 'Road Warden': path('Toll Keeper',
                                                     'Brass 5',
                                                     ('Bribery',
                                                      'Consume Alcohol',
                                                      'Gamble',
                                                      'Gossip',
                                                      'Haggle',
                                                      'Melee (Basic)',
                                                      'Perception',
                                                      'Ranged (Crossbow)'),
                                                     ('Coolheaded',
                                                      'Embezzle',
                                                      'Marksman',
                                                      'Numismatics'),
                                                     ('Crossbow with 10 Bolts',
                                                      'Leather Jack'), 91),
                                 'Witch Hunter': path('Interrogator',
                                                      'Silver 1',
                                                      ('Charm',
                                                       'Consume Alcohol',
                                                       'Heal',
                                                       'Intimidate',
                                                       'Intuition',
                                                       'Lore (Torture)',
                                                       'Melee (Brawling)',
                                                       'Perception'),
                                                      ('Coolheaded',
                                                       'Menacing',
                                                       'Read/Write',
                                                       'Resolute'),
                                                      ('Hand Weapon',
                                                       'Instruments of Torture'), 92)},
                   "RIVERFOLK": {'Boatman': path('Boat-hand',
                                                 'Silver 1',
                                                 ('Consume Alcohol',
                                                  'Dodge',
                                                  'Endurance',
                                                  'Gossip',
                                                  'Melee (Brawling)',
                                                  'Row',
                                                  'Sail',
                                                  'Swim'),
                                                 ('Dirty Fighting',
                                                  'Fisherman',
                                                  'Strong Back',
                                                  'Strong',
                                                  'Swimmer'),
                                                 ('Hand Weapon (Boat Hook)',
                                                  'Leather Jack',
                                                  'Pole'), 93),
                                 'Huffer': path('Riverguide',
                                                'Brass 4',
                                                ('Consume Alcohol',
                                                 'Gossip',
                                                 'Intuition',
                                                 'Lore (Local)',
                                                 'Lore (Riverways)',
                                                 'Perception',
                                                 'Row',
                                                 'Swim'),
                                                ('Fisherman',
                                                 'Night Vision', 
                                                 'Orientation',
                                                 'Waterman'),
                                                ('Hand Weapon (Boat Hook)',
                                                 'Storm Lantern and Oil)'), 94),
                                 'Riverwarden': path('River Recruit',
                                                     'Silver 1',
                                                     ('Athletics',
                                                      'Dodge',
                                                      'Endurance',
                                                      'Melee (Basic)',
                                                      'Perception',
                                                      'Row',
                                                      'Sail',
                                                      'Swim'),
                                                     ('Strong Swimmer',
                                                      'Strong Back',
                                                      'Very Strong',
                                                      'Waterman'),
                                                     ('Hand Weapon (Sword)',
                                                      'Leather Jack',
                                                      'Uniform'), 95), 
                                 'Riverwoman': path('Greenfish',
                                                    'Brass 2',
                                                    ('Athletics',
                                                     'Consume Alcohol',
                                                     'Dodge',
                                                     'Endurance',
                                                     'Gossip',
                                                     'Outdoor Survival',
                                                     'Row',
                                                     'Swim'),
                                                    ('Fisherman',
                                                     'Gregarious',
                                                     'Strider (Marshes)',
                                                     'Strong Swimmer'),
                                                    ('Bucket',
                                                     'Fishing Rod and Bait',
                                                     'Leather Leggings'), 96),
                                 'Seaman': path('Landsman',
                                                'Silver 1',
                                                ('Climb',
                                                 'Consume Alcohol',
                                                 'Gamble',
                                                 'Gossip',
                                                 'Row',
                                                 'Melee (Brawling)',
                                                 'Sail',
                                                 'Swim'),
                                                ('Fisherman',
                                                 'Strider (Coastal)',
                                                 'Strong Back',
                                                 'Strong Swimmer'),
                                                ('Bucket',
                                                 'Brush',
                                                 'Mop'), 97),
                                 'Smuggler': path('River Runner',
                                                  'Brass 2',
                                                  ('Athletics',
                                                   'Bribery',
                                                   'Cool',
                                                   'Consume Alcohol',
                                                   'Row',
                                                   'Sail',
                                                   'Stealth (Rural or Urban)',
                                                   'Swim'),
                                                  ('Criminal',
                                                   'Fisherman',
                                                   'Strider (Marshes)',
                                                   'Strong Back'),
                                                   ('Large Sack',
                                                    'Mask or Scarves',
                                                    'Tinderbox',
                                                    'Storm Lantern and Oil'), 98),
                                 'Stevedore': path('Dockhand',
                                                   'Brass 3',
                                                   ('Athletics',
                                                    'Climb',
                                                    'Consume Alcohol',
                                                    'Dodge',
                                                    'Endurance',
                                                    'Gossip',
                                                    'Melee (Basic)',
                                                    'Swim'),
                                                   ('Dirty Fighting',
                                                    'Strong Back',
                                                    'Sturdy',
                                                    'Very Strong'),
                                                   ('Hand Weapon (Boat Hook)',
                                                    'Leather Gloves'), 99),
                                 'Wrecker': path('Cargo Scavenger',
                                                 'Brass 2',
                                                 ('Climb',
                                                  'Consume Alcohol',
                                                  'Dodge',
                                                  'Endurance',
                                                  'Row',
                                                  'Melee (Basic)',
                                                  'Outdoor Survival',
                                                  'Swim'),
                                                 ('Break and Enter',
                                                  'Criminal',
                                                  'Fisherman',
                                                  'Strong Back'),
                                                 ('Crowbar',
                                                  'Large Sack',
                                                  'Leather Gloves'), 100)},
                   "ROGUES":    {'Bawd': path('Hustler',
                                              'Brass 1',
                                              ('Bribery',
                                               'Charm',
                                               'Consume Alcohol',
                                               'Entertain (Any)',
                                               'Gamble',
                                               'Gossip',
                                               'Haggle',
                                               'Intimidate'),
                                              ('Attractive',
                                               'Alley Cat',
                                               'Blather',
                                               'Gregarious'),
                                              ('Flask of Spirits', ), 101), 
                                 'Charlatan': path('Swindler',
                                                   'Brass 3',
                                                   ('Bribery',
                                                    'Consume Alcohol',
                                                    'Charm',
                                                    'Entertain (Storytelling)',
                                                    'Gamble',
                                                    'Gossip',
                                                    'Haggle',
                                                    'Sleight of Hand'),
                                                    ('Cardsharp',
                                                     'Diceman',
                                                     'Etiquette (Any)',
                                                     'Luck'),
                                                    ('Backpack',
                                                     '2 Sets of Clothing',
                                                     'Deck of Cards',
                                                     'Dice'), 102),
                                 'Fence': path('Broker',
                                               'Silver 1',
                                               ('Charm',
                                                'Consume Alcohol',
                                                'Dodge',
                                                'Evaluate',
                                                'Gamble',
                                                'Gossip',
                                                'Haggle',
                                                'Melee (Basic)'),
                                               ('Alley Cat',
                                                'Cardsharp',
                                                'Dealmaker',
                                                'Gregarious'),
                                               ('Hand Weapon',
                                                'Stolen Goods worth '+str(sum([D(10) for i in range(0, 3)]))+' Shillings'), 103),
                                 'Grave Robber': path('Body Snatcher',
                                                      'Brass 2',
                                                      ('Climb',
                                                       'Cool',
                                                       'Dodge',
                                                       'Endurance',
                                                       'Gossip',
                                                       'Intuition',
                                                       'Perception',
                                                       'Stealth (Any)'),
                                                      ('Alley Cat',
                                                       'Criminal',
                                                       'Flee!',
                                                       'Strong Back'),
                                                      ('Crowbar',
                                                       'Handcart',
                                                       'Hooded Cloak',
                                                       'Tarpaulin'), 104),
                                 'Outlaw': path('Brigand',
                                                'Brass 1',
                                                ('Athletics',
                                                 'Consume Alcohol',
                                                 'Cool',
                                                 'Endurance',
                                                 'Gamble',
                                                 'Intimidate',
                                                 'Melee (Basic)',
                                                 'Outdoor Survival'),
                                                ('Combat Aware',
                                                 'Criminal',
                                                 'Rover',
                                                 'Flee!'),
                                                ('Bedroll',
                                                 'Hand Weapon',
                                                 'Leather Jerkin',
                                                 'Tinderbox'), 105),
                                 'Racketeer': path('Thug',
                                                   'Brass 3',
                                                   ('Consume Alcohol',
                                                    'Cool',
                                                    'Dodge',
                                                    'Endurance',
                                                    'Intimidate',
                                                    'Lore (Local)',
                                                    'Melee (Brawling)',
                                                    'Stealth (Urban)'),
                                                   ('Criminal',
                                                    'Etiquette (Criminals)',
                                                    'Menacing',
                                                    'Strike Mighty Blow'),
                                                   ('Knuckledusters',
                                                    'Leather Jack'), 106),
                                 'Thief': path('Prowler',
                                               'Brass 1',
                                               ('Athletics',
                                                'Climb',
                                                'Cool',
                                                'Dodge',
                                                'Endurance',
                                                'Intuition',
                                                'Perception',
                                                'Stealth (Urban)'),
                                               ('Alley Cat',
                                                'Criminal',
                                                'Flee!',
                                                'Strike to Stun'),
                                               ('Crowbar',
                                                'Leather Jerkin',
                                                'Sack'), 107),
                                'Witch': path('Hexer',
                                              'Brass 1',
                                              ('Channelling',
                                               'Cool',
                                               'Endurance',
                                               'Gossip',
                                               'Intimidate',
                                               'Language (Magick)',
                                               'Sleight of Hand',
                                               'Stealth (Rural)'),
                                              ('Criminal',
                                               'Instinctive Diction',
                                               'Menacing',
                                               'Petty Magic'),
                                              ('Candles',
                                               'Chalk',
                                               'Doll',
                                               'Pins'), 108)},
                "WARRIORS":    {'Cavalryman': path('Horseman',
                                                   'Silver 2',
                                                   ('Animal Care',
                                                    'Charm Animal',
                                                    'Endurance',
                                                    'Language (Battle)',
                                                    'Melee (Basic)',
                                                    'Outdoor Survival',
                                                    'Perception',
                                                    'Ride (Horse)'),
                                                   ('Combat Aware',
                                                    'Crack the Whip',
                                                    'Lightning Reflexes',
                                                    'Roughrider'),
                                                   ('Leather Jack',
                                                    'Riding Horse with Saddle and Tack'), 109),
                                'Guard': path('Sentry',
                                              'Silver 1',
                                              ('Consume Alcohol',
                                               'Endurance',
                                               'Entertain (Storytelling)',
                                               'Gamble',
                                               'Gossip',
                                               'Intuition',
                                               'Melee (Basic)',
                                               'Perception'),
                                              ('Diceman',
                                               'Etiquette (Servants)',
                                               'Strike to Stun',
                                               'Tenacious'),
                                              ('Buckler',
                                               'Leather Jerkin',
                                               'Storm Lantern with Oil'), 110),
                                'Knight': path('Squire',
                                               'Silver 3',
                                               ('Athletics',
                                                'Animal Care',
                                                'Charm Animal',
                                                'Heal',
                                                'Lore (Heraldry)',
                                                'Melee (Cavalry)',
                                                'Ride (Horse)',
                                                'Trade (Farrier)'),
                                               ('Etiquette (any)',
                                                'Roughrider',
                                                'Sturdy',
                                                'Warrior Born'),
                                               ('Leather Jack',
                                                'Mail Shirt',
                                                'Riding Horse with Saddle and Tack',
                                                'Shield',
                                                'Trade Tools (Farrier)'), 111),
                                'Pit Fighter': path('Pugilist',
                                                    'Brass 4',
                                                    ('Athletics',
                                                     'Cool',
                                                     'Dodge',
                                                     'Endurance',
                                                     'Gamble',
                                                     'Intimidate',
                                                     'Melee (Any)',
                                                     'Melee (Brawling)'),
                                                     ('Dirty Fighting',
                                                      'In-fighter',
                                                      'Iron Jaw',
                                                      'Reversal'),
                                                    ('Bandages',
                                                     'Knuckledusters',
                                                     'Leather Jack'), 112),
                                'Protagonist': path('Braggart',
                                                    'Brass 2',
                                                    ('Athletics',
                                                     'Dodge',
                                                     'Endurance',
                                                     'Entertain (Taunt)',
                                                     'Gossip',
                                                     'Haggle',
                                                     'Intimidate',
                                                     'Melee (Any)'),
                                                    ('In-fighter',
                                                     'Dirty Fighting',
                                                     'Menacing',
                                                     'Warrior Born'),
                                                    ('Hood or Mask',
                                                     'Knuckledusters',
                                                     'Leather Jack'), 113),
                                'Slayer': path('Troll Slayer',
                                                'Brass 2',
                                                ('Consume Alcohol',
                                                 'Cool',
                                                 'Dodge,'
                                                 'Endurance',
                                                 'Gamble',
                                                 'Heal',
                                                 'Lore (Trolls)',
                                                 'Melee (Basic)'),
                                                ('Dual Wielder',
                                                 'Fearless (Everything)',
                                                 'Frenzy',
                                                 'Slayer'),
                                                ('Axe',
                                                 'Flask of Spirits',
                                                 'Shame',
                                                 'Tattoos'), 114),
                                'Soldier': path('Recruit',
                                                'Silver 1',
                                                ('Athletics',
                                                 'Climb',
                                                 'Cool',
                                                 'Dodge',
                                                 'Endurance',
                                                 'Language (Battle)',
                                                 'Melee (Basic)',
                                                 'Play (Drum or Fife)'),
                                                ('Diceman',
                                                 'Marksman',
                                                 'Strong Back',
                                                 'Warrior Born'),
                                                ('Dagger',
                                                 'Leather Breastplate',
                                                 'Uniform'), 115),
                                'Warrior Priest': path('Novitiate',
                                                       'Brass 2',
                                                       ('Cool',
                                                        'Dodge',
                                                        'Endurance',
                                                        'Heal',
                                                        'Leadership',
                                                        'Lore (Theology)',
                                                        'Melee (Any)',
                                                        'Pray'),
                                                       ('Bless (Any)',
                                                        'Etiquette (Cultists)',
                                                        'Read/Write',
                                                        'Strong-minded'),
                                                       ('Book (Religion)',
                                                        'Leather Jerkin',
                                                        'Religious Symbol',
                                                        'Robes',
                                                        'Weapon (Any Melee)'), 116)}}
                
        
        
        return Ca_path[Class][career]


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
                randTab = touch_my_pickle("Pickles/RandTalent_table.pickle")
                i=0
                while i < numRT:
                        my_roll = D(100)
                        #print(my_roll, i)
                        this_t = ''
                        for tal, nums in randTab.items():
                                if my_roll in nums:
                                        this_t = tal
                                
                        #print(this_t)
                        if this_t in these_tal: continue
                        these_tal.append(this_t)
                        i+=1
                
        
        return these_tal

        
def GetRaceSkills(race):
        race_skill = {"Human":    ('Animal Care', 'Charm', 'Cool', 'Evaluate', 'Gossip', 'Haggle',
                                   'Language (Bretonnian)', 'Language (Wastelander)', 'Leadership',
                                   'Lore (Reikland)', 'Melee (Basic)', 'Ranged (Bow)'),
                      "Dwarf":    ('Consume Alcohol', 'Cool', 'Endurance', 'Entertain (Storytelling)',
                                   'Evaluate', 'Intimidate', 'Language (Khazalid)', 'Lore (Dwarfs)',
                                   'Lore (Geology)', 'Lore (Metallurgy)', 'Melee (Basic)', 'Trade (any one)'), 
                      "Halfling": ('Charm', 'Consume Alcohol', 'Dodge', 'Gamble', 'Haggle',
                                   'Intuition', 'Language (Mootish)', 'Lore (Reikland)', 'Perception',
                                   'Sleight of Hand', 'Stealth (Any)', 'Trade (Cook)' ),
                      "High Elf": ('Cool', 'Entertain (Sing)', 'Evaluate', 'Language (Eltharin)',
                                   'Leadership', 'Melee (Basic)', 'Navigation', 'Perception',
                                   'Play (anyone)', 'Ranged (Bow)', 'Sail', 'Swim'),
                      "Wood Elf": ('Athletics', 'Climb', 'Endurance', 'Entertain (Sing)',
                                   'Intimidate', 'Language (Eltharin)', 'Melee (Basic)', 'Outdoor'
                                   'Survival', 'Perception', 'Ranged (Bow)', 'Stealth (Rural)', 'Track') }
        return race_skill[race]


def GetPhysicalFeatures(race):
        eye_table = touch_my_pickle("Pickles/eye_table.pickle")
        eye_roll = D(10) + D(10)
        eye_color = ''
        for color, nums in eye_table[race].items():
                if eye_roll in nums:
                        eye_color = color
                
        
        hair_table = touch_my_pickle("Pickles/hair_table.pickle")
        hair_roll = D(10) + D(10)
        hair_color = ''
        for color, nums in hair_table[race].items():
                if hair_roll in nums:
                        hair_color = color
                
        
        age = 0
        height = 0
        if race == 'Human':
                age = 15 + D(10)
                height = 2.54*(4*12 + 9 + sum([D(10) for i in range(0, 2)])) 
        elif race == "Dwarf":
                age = 15 + sum([D(10) for i in range(0, 10)])
                height = 2.54*(4*12 + 3 + D(10)) 
        elif race == "Halfling":
                age = 15 + sum([D(10) for i in range(0, 5)])
                height = 2.54*(3*12 +1 + D(10)) 
        else:
                age = 30 + sum([D(10) for i in range(0, 10)])
                height = 2.54*(5*12+11+ D(10)) 
                
        return (age, height, eye_color, hair_color)


if __name__ == '__main__':
        main()
