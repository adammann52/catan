

class Player:
    default_colors = ['blue','red','white','orange']
    colors = []
    names = []

    def  __init__(self,name,color):

        if name in self.names:
            self.name = name+'_1'

        else:
            self.name = name

        while color in self.colors:
            color = self.default_colors.pop()

        self.color = color

        self.hand = {'ore':0,
                     'wheat':0,
                     'sheep':0,
                     'wood':0,
                     'brick':0}

        self.knight = 0
        self.monopoly = 0
        self.road_builder = 0
        self.year_of_plenty = 0
        self.settlements = []
        self.cities = []
        self.roads = []
        self.points = 0
        self.played_knights = 0
        self.longest_road = False
        self.largest_army = False
        self.point_cards = 0
        self.ports ={'3:1':False,
                     'brick':False,
                     'ore':False,
                     'sheep':False,
                     'wheat':False,
                     'wood':False}

    def updateScore(self):

        self.points = len(self.settlements) + len(self.cities) + self.point_cards +\
            2*self.longest_road + 2*self.largest_army




