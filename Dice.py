#!/usr/bin/python

import random

class DiceSet():
    def __init__(self):
        self.d4 = random.randint(1, 4)
        self.d6 = random.randint(1, 6)
        self.d8 = random.randint(1, 8)
        self.d10 = random.randint(1, 10)
        self.d12 = random.randint(1, 12)
        self.d20 = random.randint(1, 20)
        self.d100 = random.randint(1, 100)


