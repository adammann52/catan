import random
class Board:

    def __init__(self, standard = True):
        self.rollDic = {}
        self.spots = {}
        self.vertices = []
        self.availableVertices = []
        self.setBoard(standard)
        self.setVertices()
        self.edges = {}
        self.setEdges()
        self.availableEdges = set(self.edges.keys())



    def setBoard(self, standard):

        self.spots = {i: Tile() for i in range(1,20)}


        #assigning vertices to tiles
        ranges = [[2,9],[1,10],[0,11],[1,10],[2,9]]


        orderLayout = [1,2,3,12,13,14,4,11,18,19,15,5,10,17,16,6,9,8,7]
        count = 0
        for i in range(len(ranges)):

            current = ranges[i][1]-3
            end = ranges[i][0]

            while current >= end:
                vertices = [[i,q] for q in range(current,current+3)]+[[i+1,q] for q in range(current,current+3)]
                self.spots[orderLayout[count]].vertices = vertices
                count+=1
                current-=2



        #assigning resources to tiles
        options = ['Desert'] + ['Sheep']*4 +['Wheat']*4 + ['Ore']*3 + ['Wood']*4 + ['Brick']*3
        random.shuffle(options)
        for spot,r  in zip(range(1,20),options):
            self.spots[spot].resource = r

        #assinging rolls to tiles
        self.rollDic = {}
        rolls = [5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11][::-1]
        if not standard:
            random.shuffle(rolls)

        for i in range(1,20):
            if self.spots[i].resource != 'Desert':
                self.rollDic[i] = rolls.pop()


    def setVertices(self):
        self.vertices = []
        for i in range(6):
            row = []
            availableRow = []
            for q in range(11):
                #make sure it's not a corner
                if (i,q) in [(0,0),(0,1),(1,0),(5,0),(4,0),(5,1),
                             (0,10),(1,10),(0,9),(5,10),(4,10),(5,9)]:
                    row.append(None)
                    availableRow.append(None)
                else:
                    row.append(Vertex())
                    availableRow.append(True)

            self.vertices.append(row)
            self.availableVertices.append(availableRow)


        #assigning ports
        threeOnes = [[0,2],[0,3],[1,8],[1,9],[2,10],[3,10],[5,2],[5,3]]
        for spot in threeOnes:
            self.vertices[spot[0]][spot[1]].port = '3:1'

        for spot in [[1,1],[2,1]]:
            self.vertices[spot[0]][spot[1]].port = 'ore'

        for spot in [[3,1],[4,1]]:
            self.vertices[spot[0]][spot[1]].port = 'wheat'

        for spot in [[5,5],[5,6]]:
            self.vertices[spot[0]][spot[1]].port = 'wood'

        for spot in [[4,9],[4,8]]:
            self.vertices[spot[0]][spot[1]].port = 'brick'

        for spot in [[0,5],[0,6]]:
            self.vertices[spot[0]][spot[1]].port = 'sheep'


    def setEdges(self):

        #write to left
        for i in range(6):
            for q in range(10):
                if self.vertices[i][q] and self.vertices[i][q+1]:
                    self.edges[((i,q),(i,q+1))] = Edge()

        #write up and down
        for q in range(1,10):
            if q % 2 == 1:
                self.edges[((1,q),(2,q))] = Edge()
            else:
                self.edges[((0,q),(1,q))] = Edge()

        for q in range(0,11):
            if q % 2 == 0:
                self.edges[((2,q),(3,q))] = Edge()
            else:
                self.edges[((3,q),(4,q))] = Edge()

        for q in range(2,9):
            if q % 2 == 0:
                self.edges[((4,q),(5,q))] = Edge()

    def propogateVertexPurchase(self, t):
        for el in self.edges:
            if t in el:
                if t == el[0]:
                    self.availableVertices[el[1][0]][el[1][1]] = False
                else:
                    self.availableVertices[el[0][0]][el[0][1]] = False


class Vertex:

    def __init__(self):
        self.owner  = None
        self.port = None
        self.city = None
        self.val = 0

class Tile:

    def __init__(self):
        self.resource = None
        self.vertices = []
        self.blocked = False

class Edge:

    def __init__(self):
        owner = None
