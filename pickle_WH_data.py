#!/usr/bin/env python

import pickle
import pandas as pd

def tickle_my_pickle(dic, pickle_file):
    pickle_out = open(pickle_file, "wb")
    pickle.dump(dic, pickle_out)
    pickle_out.close()
    

def convert2Int(strNum):
    '''This function takes an arrray of strings with elements in the form 
    '55' or '6-9'. The function turns the array into a list of lists in the form 
    [[6, 7, 8, 9], ..., [55]]'''

    new_list = []    
    for num in strNum:
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
        
    
def make_career_table():
    # need 5 tables of careers, one for each race 
    # there are Careers which are grouped in sets called Classes 
    # each races has a dictionary
    # in that dic the career is the KEY and
    # the VALUE is a list of numbers corresponding   
    # to the Career ex: human_careers = {..., 'Nun': [4, 5], ...}
    # Then you can look up the Class in the Class dic
    # ex: human_classes = {'Academic': [..., 'Nun',...], ...}

    TCT = pd.read_csv('PDF_piece/CareerTable.csv', dtype = str)

    # print(TCT)
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

    return (master_map, career_class)


def make_rand_talent_table():
    randTal = pd.read_csv('PDF_piece/RandomTalents.csv', dtype = str)
    tab = pd.concat([pd.DataFrame(randTal['Roll']), pd.DataFrame(randTal['Description'])], axis =1)
    tabB = pd.concat([pd.DataFrame(randTal['Roll.1']), pd.DataFrame(randTal['Description.1'])], axis=1)
    tabB = tabB.rename(columns= {"Roll.1": "Roll", "Description.1": "Description"})
    res = tab.append(tabB)
    res = res.dropna()
    res = res.reset_index(drop=True)
    rolls = convert2Int(res["Roll"])
    dick_tab = Make_a_Dick(res["Description"], rolls)
    return dick_tab

def make_PT_table(filepath):
    eye_tab = pd.read_csv(filepath)
    eye_tab = eye_tab.drop(["Unnamed: 6"], axis = 1)

    rollers = convert2Int(eye_tab["2d10"].values)
    human = eye_tab["Human"].values
    halfling = eye_tab["Halfling"].values
    dwarf = eye_tab["Dwarf"].values
    high_elf = eye_tab["High Elf"].values
    wood_elf = eye_tab["Wood Elf"].values
    
    master_map = {}
    master_map['Human'] =Make_a_Dick(human, rollers)
    master_map['Halfling'] = Make_a_Dick(halfling, rollers)
    master_map['Dwarf'] = Make_a_Dick(dwarf, rollers)
    master_map['High Elf'] = Make_a_Dick(high_elf, rollers)
    master_map['Wood Elf'] = Make_a_Dick(wood_elf, rollers)
    master_map['Wood Elf']['Chestnut'] = [8, 9, 10, 11, 12, 13, 14]
    return master_map


def Make_a_Dick(keys, values):
    new_dic = {}
    nn = len(keys)
    for i in range(0, nn):
        new_dic[keys[i]] = values[i]
    return new_dic


if __name__=="__main__":

    dic_mm, dic_cc  = make_career_table()
    tickle_my_pickle(dic_mm, "career_table.pickle")
    tickle_my_pickle(dic_cc, "classes_table.pickle")

    eye_table = make_PT_table("PDF_piece/just_eyes.csv")
    hair_table = make_PT_table("PDF_piece/just_hair.csv")
    tickle_my_pickle(eye_table, "eye_table.pickle")
    tickle_my_pickle(hair_table, "hair_table.pickle")

    randTab = make_rand_talent_table()
    print(randTab)
    tickle_my_pickle(randTab, "RandTalent_table.pickle")
