import random

class DevelopmentCards:

    def __init__(self):

        self.cards = ['Knight']*14 + ['Year of Plenty']*2 + ['Monoploy']*2 + ['Road Builder']*2 + ['Point Card']*5

        random.shuffle(self.cards)
