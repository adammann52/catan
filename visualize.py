from tkinter import *
import math
from game import Game
from seven import Seven
import board
import player
import random
from seven import Seven


class Visualize:

    def __init__(self):
        self.game = None
        self.freeze = False
        self.robber_move = False
        self.rolled = False
        self.setUp() #initializes game
        self.playGame()
        self.hand = None
        self.devs = None
        self.c = None
        self.point_counter = 0
        self.current_robber = None


    """Creates a small window to obtain user input
    of the names of players and their desired colors"""

    def setUp(self):
        root = Tk()
        root.title('Settlers of Catan')

        n_players = 0
        players = []
        colors = []

        def addInput():
            players.append(e1.get())
            colors.append(e2.get())
            e1.delete(0,END)
            e2.delete(0,END)

        Label(root,
                 text="Name").grid(row=0)
        Label(root,
                 text="Color").grid(row=1)

        e1 = Entry(root)
        e2 = Entry(root)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        Button(root,text='Enter',command=addInput)\
            .grid(row=2,column=0,sticky=W)
        Button(root,
                  text='Start Game',
                  command=root.destroy).grid(row=2,
                                            column=1,
                                            sticky=W)


        root.mainloop()
        if len(players) > 2:
            self.game = Game(players,colors)
        else:
            self.game = Game()

    def playGame(self):

        #creatig the board
        root = Tk()
        root.title('Settlers of Catan')


        #creating the tiles
        w = 70 #tile sizes
        spots = [self.game.board.spots[i].resource for i in range(1,20)]
        colors = {'Ore':'grey','Wheat':'yellow','Brick':'red',
                  'Wood':'#228B22','Desert':'tan','Sheep':'#90EE90'}

        c = Canvas(root,width=w*15, height=w*15, background ='#ADD8E6')
        self.c = c
        c.pack()
        center = [w*7.5,w*6] #center of board


        #positioning of tiles in spiral order
        tiles = [[2,-2*math.sqrt(3)],[0,-2*math.sqrt(3)],[-2,-2*math.sqrt(3)],
                 [-3,-math.sqrt(3)],[-4,0],[-3,math.sqrt(3)],
                 [-2,2*math.sqrt(3)],
                 [0,2*math.sqrt(3)],[2,2*math.sqrt(3)],[3,math.sqrt(3)],[4,0],
                 [3,-math.sqrt(3)],[1,-math.sqrt(3)],[-1,-math.sqrt(3)],[-2,0],
                 [-1,math.sqrt(3)],[1,math.sqrt(3)],[2,0],[0,0]]

        #padded width of each tile to create space in between for roads
        pw = math.sqrt(w**2 - (w/2)**2) + 4

        #creates the tan area around the board
        points = []
        for i in range(0,360,60):
            points.append(math.cos(i*(math.pi/180))*pw*6.5 + center[0])
            points.append(math.sin(i*(math.pi/180))*pw*6.5 + center[1])
            c.create_polygon(points,fill = '#ffdf80')

        #create the black underlay
        points = []
        for i in range(0,360,60):
            points.append(math.cos(i*(math.pi/180))*pw*4.62 + center[0])
            points.append(math.sin(i*(math.pi/180))*pw*4.62 + center[1])
            c.create_polygon(points,fill = 'black')

        tile_to_knight = {}
        #creates each tile as specified in the board class
        for tile,spot,q in zip(tiles,spots,range(1,20)):
            points = []
            shiftx = (center[0]+(tile[0]*pw))
            shifty = (center[1]+(tile[1]*pw))

            for i in range(30,390,60):
                points.append(math.cos(i*(math.pi/180))*w+shiftx)
                points.append(math.sin(i*(math.pi/180))*w+shifty)

            t = c.create_polygon(points, outline=colors[spot],
                                    fill=colors[spot])

            if spot != 'Desert':
                c.create_text(shiftx,shifty,fill='black',
                                     font="Times 25 bold",
                              text=str(self.game.board.rollDic[q]))

                #used to move the knight
            tmp = c.create_oval(shiftx+15,shifty+15,
                              shiftx-15,shifty-15,fill = '',outline='')

            tile_to_knight[t] = [tmp,self.game.board.spots[q]]

            if spot == 'Desert':
                self.current_robber = t
                c.itemconfigure(tile_to_knight[t][0],fill = 'black')


            c.tag_bind(t,"<Enter>", lambda event,
                       tag = t: enterTile(tag))
            c.tag_bind(t,"<Leave>", lambda event,
                       tag = t: leaveTile(tag))
            c.tag_bind(t,'<Button-1>',lambda event,
                       tag = t: clickTile(tag))


        def enterTile(tag):
            if self.freeze and self.robber_move:
                c.itemconfigure(tile_to_knight[tag][0],fill='black')

        def leaveTile(tag):
            if self.freeze and self.robber_move and \
                    tag != self.current_robber:
                c.itemconfigure(tile_to_knight[tag][0],fill = '')

        def clickTile(tag):
            if self.freeze and self.game.round > 1 and \
                    self.robber_move:

                c.itemconfigure(tile_to_knight[tag][0],fill='black')
                c.itemconfigure(tile_to_knight[self.current_robber][0],
                                fill = '')
                tile_to_knight[self.current_robber][1].blocked=False
                self.current_robber = tag
                tile_to_knight[self.current_robber][1].blocked=True

                self.robber_move = False
                self.freeze = False

                self.takeCard(tile_to_knight[self.current_robber][1])



        threeOnes = [[-2.8,-2.8*math.sqrt(3)],[-2.8,2.8*math.sqrt(3)],
                     [5.75,0],[4,-3]]

        for port in threeOnes:
            x = center[0] + port[0]*pw
            y = center[1] + port[1]*pw

            c.create_text(x,y,fill='black',font='Times 25 italic bold',
                          text='3:1')

        #positioning of ports
        ports = {'Sheep':[.7,-5],'Wood':[.7,5],'Ore':[-4.8,-1.7],
                 'Wheat':[-4.8,1.7],'Brick':[4,3]}

        for port in ports.keys():
            x = center[0] + ports[port][0]*pw
            y = center[1] + ports[port][1]*pw

            c.create_text(x,y,fill='black',font='Times 25 italic bold',
                          text=port)

        #Top left tells you which players turn
        turn_label = c.create_text(100,50,fill='black', font = 'Times 30',
                                text = self.game.current_player.name+"'s Turn")

        #Top right tell you the current players point tally
        point_counter = c.create_text(950,50,fill='black', font = 'Times 30',
                                    text = 'Points: '+ \
                                      str(self.game.current_player.points))
        self.point_counter = point_counter

        """Player's hand"""


        c.create_polygon([[140,1050],[910,1050],[910,800],[140,800]],
                         fill = 'white')

        self.hand = {}
        self.devs = {}

        #resource cards
        c.create_text(210,825,fill='black',font='Times 30 bold',
                      text='HAND')

        self.hand['brick'] = c.create_text(255,875,fill='black',
                        font='Times 25',text='Brick: '+ \
                        str(self.game.current_player.hand['brick']),
                        anchor='e')

        self.hand['ore'] = c.create_text(255,910,fill='black',
                        font='Times 25',text='Ore: '+ \
                        str(self.game.current_player.hand['ore']),
                                         anchor='e')

        self.hand['sheep'] = c.create_text(255,945,fill='black',
                        font='Times 25',text='Sheep: '+ \
                        str(self.game.current_player.hand['sheep']),
                                           anchor='e')

        self.hand['wheat'] = c.create_text(255,980,fill='black',
                        font='Times 25', text='Wheat: '+ \
                        str(self.game.current_player.hand['wheat']),
                                           anchor='e')

        self.hand['wood'] = c.create_text(255,1015,fill='black',
                        font='Times 25', text='Wood: '+ \
                        str(self.game.current_player.hand['wood']),
                                          anchor='e')


        #development cards
        c.create_text(900,82e5,fill='black',font='Times 30 bold',
                      text='DEV CARDS',anchor = 'e')

        self.devs['knight'] = c.create_text(900,875,fill='black',
                        font='Times 25',text='Knight x '+ \
                        str(self.game.current_player.knight),
                        anchor='e')

        def clickKnight(tag):
            if self.game.current_player.knight > 0 and not self.game.playedDev:
                self.game.current_player.knight -= 1
                self.game.playedDev = True
                self.updateDevs()
                self.robber_move = True
                self.freeze = True
                self.game.playedKnight()

        c.tag_bind(self.devs['knight'],'<Button-1>',lambda event,
                       tag = self.devs['knight']: clickKnight(tag))



        self.devs['monopoly'] = c.create_text(900,910,fill='black',
                        font='Times 25', text='Monopoly x '+ \
                        str(self.game.current_player.monopoly),
                        anchor='e')

        def clickMonopoly(tag):
            if self.game.current_player.monopoly > 0 and not self.game.playedDev:
                self.game.current_player.monopoly -= 1
                self.game.playedDev = True
                self.updateDevs()
                self.freeze = True

                self.monopolize()


        c.tag_bind(self.devs['monopoly'],'<Button-1>',lambda event,
                       tag = self.devs['monopoly']: clickMonopoly(tag))



        self.devs['road_builder'] = c.create_text(900,945,fill='black',
                        font='Times 25',text='Road Builder x '+ \
                        str(self.game.current_player.road_builder),
                        anchor='e')

        def clickRB(tag):
            if self.game.current_player.road_builder > 0 and not self.game.playedDev:
                self.game.current_player.road_builder -= 1
                self.game.playedDev = True
                self.updateDevs()
                self.game.building_roads = 2
                self.game.availableMoves()

        c.tag_bind(self.devs['road_builder'],'<Button-1>',lambda event,
                       tag = self.devs['road_builder']: clickRB(tag))


        self.devs['year_of_plenty'] = c.create_text(900,980,fill='black',
                        font='Times 25',text='Year of Plenty x '+ \
                        str(self.game.current_player.year_of_plenty),
                        anchor='e')

        def clickYP(tag):
            if self.game.current_player.year_of_plenty > 0 and\
                    not self.game.playedDev:
                self.game.current_player.year_of_plenty -= 1
                self.game.playedDev = True
                self.updateDevs()
                self.freeze = True
                self.plentiful(2)


        c.tag_bind(self.devs['year_of_plenty'],'<Button-1>',lambda event,
                       tag = self.devs['year_of_plenty']: clickYP(tag))




        self.devs['point_cards'] = c.create_text(900,1015,fill='black',
                        font='Times 25', text='Point Card x '+ \
                        str(self.game.current_player.point_cards),
                        anchor='e')




        #Keeps track of the current rolled number
        roll_label = c.create_text(525,825,fill='black',
                                   font = 'Times 30 bold',
                                   text = 'Roll: '+ str(self.game.dieRoll))

        def nextTurn():

            if self.game.round > 1:
                self.game.rollDice()
                c.itemconfigure(roll_label,
                                text = 'Roll: ' + str(self.game.dieRoll))
                self.rolled = True
            else:
                self.game.turn += 1
                self.game.round = self.game.turn//len(self.game.players)
                self.game.playerUpdate()
                self.updateDevs()
                c.itemconfigure(turn_label,
                            text = self.game.current_player.name+"'s Turn")
                self.game.availableMoves()
                self.updateHand()


            if self.game.dieRoll == 7:
                Seven.rolled(self,self.game.players)

            self.updateHand()
            self.game.availableMoves()


        def enterRoll(event,tag):
            if not self.freeze:
                c.itemconfigure(roll_box,fill = 'white')

        def leaveRoll(event,tag):
            if not self.freeze:
                c.itemconfigure(roll_box,fill = 'red')

        def clickRoll(event,tag):
            if not self.freeze and not self.rolled:
                if self.game.round > 1:
                    nextTurn()

        roll_box = c.create_rectangle(5,1020,135,970,fill = 'red')
        tmp = c.create_text(70,995,fill='black',font = 'Times 25 bold',
                            text = 'ROLL')
        c.tag_bind(tmp,"<Enter>", lambda event,
                   tag = tmp: enterRoll(event,tag))
        c.tag_bind(tmp,"<Leave>", lambda event,
                   tag = tmp: leaveRoll(event,tag))
        c.tag_bind(tmp,'<Button-1>',lambda event,
                   tag = tmp: clickRoll(event,tag))
        c.tag_bind(roll_box,'<Button-1>',lambda event,
                   tag = roll_box: clickRoll(event,tag))



        def enterEnd(event,tag):
            if not self.freeze:
                c.itemconfigure(end_box,fill = 'white')

        def leaveEnd(event,tag):
            if not self.freeze:
                c.itemconfigure(end_box,fill = '#808080')

        def clickEnd(event,tag):
            if not self.freeze and self.rolled:
                self.game.turn += 1
                self.game.round = self.game.turn//len(self.game.players)
                self.game.playerUpdate()
                self.updateDevs()
                c.itemconfigure(turn_label,
                            text = self.game.current_player.name+"'s Turn")
                self.game.availableMoves()
                self.updateHand()
                self.rolled = False


        end_box = c.create_rectangle(915,1020,1045,970,fill = '#808080')
        tmp = c.create_text(980,995,fill='black',font = 'Times 23 bold',
                            text = 'END TURN')
        c.tag_bind(tmp,"<Enter>", lambda event,
                   tag = tmp: enterEnd(event,tag))
        c.tag_bind(tmp,"<Leave>", lambda event,
                   tag = tmp: leaveEnd(event,tag))
        c.tag_bind(tmp,'<Button-1>',lambda event,
                   tag = tmp: clickEnd(event,tag))
        c.tag_bind(end_box,'<Button-1>',lambda event,
                   tag = end_box: clickEnd(event,tag))


        def enterBDev(event,tag):
            if not self.freeze:
                c.itemconfigure(dev_box,fill = 'white')

        def leaveBDev(event,tag):
            if not self.freeze:
                c.itemconfigure(dev_box,fill = '#A9A9A9')

        def clickBDev(event,tag):
            if not self.freeze and self.game.round > 1 and \
                    self.game.moves['dev_card']:
                self.game.buyDev()
                self.updateHand()
                self.updateDevs()
                self.game.availableMoves()

        dev_box = c.create_rectangle(915,965,1045,915,
                                     fill = '#A9A9A9')
        tmp = c.create_text(980,940,fill='black',font = 'Times 23 bold',
                            text = 'BUY DEV-C')
        c.tag_bind(tmp,"<Enter>", lambda event,
                   tag = tmp: enterBDev(event,tag))
        c.tag_bind(tmp,"<Leave>", lambda event,
                   tag = tmp: leaveBDev(event,tag))
        c.tag_bind(tmp,'<Button-1>',lambda event,
                   tag = tmp: clickBDev(event,tag))
        c.tag_bind(dev_box,'<Button-1>',lambda event,
                   tag = dev_box: clickBDev(event,tag))


        def enterTrade(event,tag):
            if not self.freeze:
                c.itemconfigure(tradeIn_box,fill = 'white')

        def leaveTrade(event,tag):
            if not self.freeze:
                c.itemconfigure(tradeIn_box,fill = '#C8C8C8')

        def clickTrade(event,tag):
            if not self.freeze and self.game.round > 1:
                #self.freeze = True
                self.tradeWindow()

        tradeIn_box = c.create_rectangle(915,910,1045,860,
                                     fill = '#C8C8C8', activefill='white')
        tmp = c.create_text(980,885,fill='black',font = 'Times 23 bold',
                            text = 'TRADE IN')
        c.tag_bind(tmp,"<Enter>", lambda event,
                   tag = tmp: enterTrade(event,tag))
        c.tag_bind(tmp,"<Leave>", lambda event,
                   tag = tmp: leaveTrade(event,tag))
        c.tag_bind(tmp,'<Button-1>',lambda event,
                   tag = tmp: clickTrade(event,tag))
        c.tag_bind(tradeIn_box,'<Button-1>',lambda event,
                   tag = tradeIn_box: clickTrade(event,tag))

        def enterTradeOther(event,tag):
            if not self.freeze:
                c.itemconfigure(tradeOther_box,fill = 'white')

        def leaveTradeOther(event,tag):
            if not self.freeze:
                c.itemconfigure(tradeOther_box,fill = '#E0E0E0')

        def clickTradeOther(event,tag):
            if not self.freeze and self.game.round > 1:
                #self.freeze = True
                self.tradeOtherWindow()

        tradeOther_box = c.create_rectangle(915,855,1045,805,
                                     fill = '#E0E0E0', activefill='white')
        tmp = c.create_text(980,830,fill='black',font = 'Times 19 bold',
                            text = '  TRADE \nPLAYERS')
        c.tag_bind(tmp,"<Enter>", lambda event,
                   tag = tmp: enterTradeOther(event,tag))
        c.tag_bind(tmp,"<Leave>", lambda event,
                   tag = tmp: leaveTradeOther(event,tag))
        c.tag_bind(tmp,'<Button-1>',lambda event,
                   tag = tmp: clickTradeOther(event,tag))
        c.tag_bind(tradeIn_box,'<Button-1>',lambda event,
                   tag = tradeOther_box: clickTradeOther(event,tag))



        """Create houses and cities"""

        houses = []
        house_positions = []
        settlements_to_vertices = {}
        boughtHomes = set()

        cities = []
        city_positions = []
        cities_to_vertices = {}
        boughtCities = set()

        house_to_city = {}

        #centers house around cooridinates
        def houseShape(x,y):
            points = [[15,0],[0,-10],[-15,0],[-15,20],[15,20]]

            return [[el[0]+x+center[0],el[1]+y+center[1]]
                    for el in points]

        def cityShape(x,y):
            points = [[35,0],[15,0],[0,-10],[-15,0],[-15,20],[35,20]]

            return [[el[0]+x+center[0],el[1]+y+center[1]]
                    for el in points]


        def buyHouse(event,tag):
            index =  settlements_to_vertices[tag]
            if self.game.moves['settlements'][index[0]][index[1]] and \
                    not self.freeze:
                c.itemconfigure(tag,fill=self.game.current_player.color,
                                outline='black')
                boughtHomes.add(tag)
                self.game.buySettlement(self.game.current_player.name,
                                        index)
                self.game.availableMoves()
                self.updateHand()
                c.tag_raise(house_to_city[tag])

        def enterHouse(event,tag):
            index =  settlements_to_vertices[tag]
            if self.game.moves['settlements'][index[0]][index[1]] and\
                    not self.freeze:
                c.itemconfigure(tag,fill='#D3D3D3')

        def leaveHouse(event,tag):
            if tag not in boughtHomes:
                c.itemconfigure(tag,fill='')

        def buyCity(event,tag):
            index =  cities_to_vertices[tag]
            if self.game.round > 1 and \
                    self.game.moves['cities'][index[0]][index[1]] and \
                    not self.freeze:
                c.itemconfigure(tag,fill=self.game.current_player.color,
                                outline='black')
                boughtCities.add(tag)
                self.game.buyCity(self.game.current_player.name,
                                        index)
                self.game.availableMoves()
                self.updateHand()

        def enterCity(event,tag):
            index =  cities_to_vertices[tag]
            if self.game.round > 1 and self.game.moves['cities'][index[0]][index[1]] and\
                    not self.freeze:
                c.itemconfigure(tag,fill='#D3D3D3')

        def leaveCity(event,tag):
            if tag not in boughtCities:
                c.itemconfigure(tag,fill='')



        startPoints = [[-3*pw+2,-4.1*pw],[-4*pw+2,-2.4*pw],
                       [-5*pw+2,-.7*pw],[-5*pw+2,.5*pw],[-4*pw+2,2.2*pw],
                       [-3*pw+2,3.9*pw]]

        for i in range(len(self.game.board.vertices)):
            row = []
            c_row = []
            position_row = []
            x = startPoints[i][0]
            y = startPoints[i][1]
            for q in range(len(self.game.board.vertices[0])):

                if self.game.board.vertices[i][q]:
                    home = c.create_polygon(houseShape(x,y),fill = '')
                    city = c.create_polygon(cityShape(x,y), fill = '')
                    c.tag_bind(home,"<Button-1>", lambda event,
                               tag = home: buyHouse(event,tag))
                    c.tag_bind(home,"<Enter>", lambda event,
                               tag = home: enterHouse(event,tag))
                    c.tag_bind(home,"<Leave>", lambda event,
                               tag = home: leaveHouse(event,tag))

                    c.tag_bind(city,"<Button-1>", lambda event,
                               tag = city: buyCity(event,tag))
                    c.tag_bind(city,"<Enter>", lambda event,
                               tag = city: enterCity(event,tag))
                    c.tag_bind(city,"<Leave>", lambda event,
                               tag = city: leaveCity(event,tag))




                    house_to_city[home] = city
                    row.append(home)
                    c_row.append(city)
                    position_row.append((x+center[0],y+center[1]+6))
                    settlements_to_vertices[home] = (i,q)
                    cities_to_vertices[city] = (i,q)
                    x +=  math.sqrt(.75*w**2) + 3.5

                    if i%2==0:
                        if q%2==0:
                            y -= .5*w
                        else:
                            y += .5*w

                    else:
                        if q%2==0:
                            y += .5*w
                        else:
                            y -= .5*w
                else:
                    row.append(None)
                    position_row.append(None)

            houses.append(row)
            house_positions.append(position_row)
            cities.append(row)
            city_positions.append(position_row)


        """Create roads"""

        boughtRoads = set()

        def buyRoad(event,tag):
            index =  roads_to_edges[tag]
            if index in self.game.moves['roads'] and not self.freeze:
                c.itemconfigure(tag,fill=self.game.current_player.color)
                boughtRoads.add(tag)
                self.game.buyRoad(self.game.current_player.name,index)
                self.game.availableMoves()
                if self.game.round < 2:
                    nextTurn()
                self.updateHand()

        def enterRoad(event,tag):
            index = roads_to_edges[tag]
            if index in self.game.moves['roads'] and not self.freeze:
                c.itemconfigure(tag,fill='#D3D3D3')

        def leaveRoad(event,tag):
            if tag not in boughtRoads:
                c.itemconfigure(tag,fill='')


        roads_to_edges = {}
        for edge in self.game.board.availableEdges:
            house_1 = edge[0]
            house_2 = edge[1]
            road = c.create_line(house_positions[house_1[0]][house_1[1]],
                                 house_positions[house_2[0]][house_2[1]],
                                 fill='',width=8)

            c.tag_bind(road,"<Button-1>", lambda event,
                       tag = road: buyRoad(event,tag))
            c.tag_bind(road,"<Enter>", lambda event,
                       tag = road: enterRoad(event,tag))
            c.tag_bind(road,"<Leave>", lambda event,
                       tag = road: leaveRoad(event,tag))

            roads_to_edges[road] = edge

        for key in settlements_to_vertices.keys():
            c.tag_raise(key)

        root.mainloop()

    #Reflects changes in hand after any transaction or at beginning of turn
    def updateHand(self):

        for key in self.hand.keys():
            self.c.itemconfigure(self.hand[key],
                        text = key.capitalize()+': '+ \
                                 str(self.game.current_player.hand[key]))

        self.c.itemconfigure(self.point_counter,
                             text = 'Points: '+ \
                             str(self.game.current_player.points))

    #Updates development cards at new turn/ after pruchase/ after use
    def updateDevs(self):

        self.c.itemconfigure(self.devs['knight'],
                    text = 'Knight x '+str(self.game.current_player.knight))

        self.c.itemconfigure(self.devs['monopoly'],
                    text = 'Monopoly x '+ \
                             str(self.game.current_player.monopoly))

        self.c.itemconfigure(self.devs['year_of_plenty'],
                    text = 'Year of Plenty x '+ \
                             str(self.game.current_player.year_of_plenty))

        self.c.itemconfigure(self.devs['road_builder'],
                    text = 'Road Builder x '+ \
                             str(self.game.current_player.road_builder))

        self.c.itemconfigure(self.devs['point_cards'],
                    text = 'Point Card x '+ \
                             str(self.game.current_player.point_cards))


    def takeCard(self,tile):

        players = set()
        for vertex in tile.vertices:
            if self.game.board.vertices[vertex[0]][vertex[1]].owner:

                players.add(self.game.board.\
                            vertices[vertex[0]][vertex[1]].owner)

        players = list(players)

        takeable = []

        for player in players:

            if player != self.game.current_player and \
                    sum(list(player.hand.values()))>0:
                takeable.append(player)

        if len(takeable)>0:

            root = Tk()
            b1 = Button(root,text=takeable[0].name,
                        command=lambda p = takeable[0]:takeOne(p))
            b1.grid(row=0,column=0)

            if len(takeable)>1:
                b2 = Button(root,text=takeable[1].name,
                        command=lambda p = takeable[1]:takeOne(p))
                b2.grid(row=1,column=0)

            if len(takeable)>2:
                b3 = Button(root,text=takeable[2].name,
                        command=lambda p = takeable[2]:takeOne(p))
                b3.grid(row=2,column=0)



            def takeOne(p):

                l = [[resource]*amount for resource, amount in \
                         zip(p.hand.keys(),p.hand.values())]

                cards = []

                for element in l:
                    cards += element

                taken = cards[random.randint(0,len(cards)-1)]
                p.hand[taken] -= 1
                self.game.current_player.hand[taken] += 1

                self.updateHand()
                self.game.availableMoves()
                root.destroy()

            root.mainloop()

    def monopolize(self):

        root = Tk()

        brick = Button(root,text='Brick',command = lambda r = 'brick': takeResource(r))
        brick.grid(row=0)

        brick = Button(root,text='Ore',command = lambda r = 'ore': takeResource(r))
        brick.grid(row=1)

        brick = Button(root,text='Sheep',command = lambda r = 'sheep': takeResource(r))
        brick.grid(row=2)

        brick = Button(root,text='Wheat',command = lambda r = 'wheat': takeResource(r))
        brick.grid(row=3)

        brick = Button(root,text='Wood',command = lambda r = 'wood': takeResource(r))
        brick.grid(row=4)



        def takeResource(resource):
            total = 0

            for player in self.game.players:

                if player != self.game.current_player:
                    total += player.hand[resource]

                    player.hand[resource] = 0

            self.game.current_player.hand[resource] += total
            self.updateHand()
            self.game.availableMoves()
            self.freeze = False
            root.destroy()

    def plentiful(self, count):

        root = Tk()

        brick = Button(root,text='Brick',command = lambda r = 'brick': takeResource(r))
        brick.grid(row=0)

        brick = Button(root,text='Ore',command = lambda r = 'ore': takeResource(r))
        brick.grid(row=1)

        brick = Button(root,text='Sheep',command = lambda r = 'sheep': takeResource(r))
        brick.grid(row=2)

        brick = Button(root,text='Wheat',command = lambda r = 'wheat': takeResource(r))
        brick.grid(row=3)

        brick = Button(root,text='Wood',command = lambda r = 'wood': takeResource(r))
        brick.grid(row=4)



        def takeResource(resource):

            nonlocal count
            self.game.current_player.hand[resource] += 1
            self.updateHand()
            count -= 1

            if count == 0:
                self.freeze = False
                self.game.availableMoves()
                root.destroy()


    def tradeWindow(self):

        root = Tk()
        Label(root,text = 'What to Trade In').grid(row=0)
        Button(root, text = 'Brick',command = lambda resource='brick':trade(resource)).grid(row=1)
        Button(root, text = 'Ore',command = lambda resource='ore':trade(resource)).grid(row=2)
        Button(root, text = 'Sheep',command = lambda resource='sheep':trade(resource)).grid(row=3)
        Button(root, text = 'Wheat',command = lambda resource='wheat':trade(resource)).grid(row=4)
        Button(root, text = 'Wood',command = lambda resource='wood':trade(resource)).grid(row=5)

        def trade(r):

            if self.game.current_player.ports[r] and self.game.current_player.hand[r] > 1:
                self.game.current_player.hand[r] -= 2
                self.plentiful(1)
                root.destroy()

            elif self.game.current_player.ports['3:1'] and self.game.current_player.hand[r] > 2:
                self.game.current_player.hand[r] -= 3
                self.plentiful(1)
                root.destroy()

            elif self.game.current_player.hand[r] > 3:
                self.game.current_player.hand[r] -= 4
                self.plentiful(1)
                root.destroy()

        root.mainloop()


    def tradeOtherWindow(self):

        root = Tk()

        n_give = []

        n_take = []

        def addInput():
            n_give = list(map(int,[e1.get(),e2.get(),e3.get(),e4.get(),e5.get()]))
            n_take = list(map(int,[e6.get(),e7.get(),e8.get(),e9.get(),e10.get()]))

            root.destroy()
            self.offerTrade(n_give,n_take)


        Label(root,text="Want I want to give").grid(row=0,column=0, columnspan = 2)
        Label(root,text="Want I want to give").grid(row=0, column = 2, columnspan=2)

        Label(root,
                 text="Brick").grid(row=1)
        Label(root,
                 text="Ore").grid(row=2)
        Label(root,
                 text="Sheep").grid(row=3)
        Label(root,
                 text="Wheat").grid(row=4)
        Label(root,
                 text="Wood").grid(row=5)


        e1 = Entry(root)
        e2 = Entry(root)
        e3 = Entry(root)
        e4 = Entry(root)
        e5 = Entry(root)

        e1.grid(row=1, column=1)
        e1.insert(0,0)
        e2.grid(row=2, column=1)
        e2.insert(0,0)
        e3.grid(row=3, column=1)
        e3.insert(0,0)
        e4.grid(row=4, column=1)
        e4.insert(0,0)
        e5.grid(row=5, column=1)
        e5.insert(0,0)


        Label(root,
                 text="Brick").grid(row=1,column=2)
        Label(root,
                 text="Ore").grid(row=2,column=2)
        Label(root,
                 text="Sheep").grid(row=3,column=2)
        Label(root,
                 text="Wheat").grid(row=4,column=2)
        Label(root,
                 text="Wood").grid(row=5,column=2)


        e6 = Entry(root)
        e7 = Entry(root)
        e8 = Entry(root)
        e9 = Entry(root)
        e10 = Entry(root)

        e6.grid(row=1, column=3)
        e6.insert(0,0)
        e7.grid(row=2, column=3)
        e7.insert(0,0)
        e8.grid(row=3, column=3)
        e8.insert(0,0)
        e9.grid(row=4, column=3)
        e9.insert(0,0)
        e10.grid(row=5, column=3)
        e10.insert(0,0)




        Button(root,
                  text='Offer Trade',
                  command=addInput).grid(row=6,
                                            sticky=W)


        root.mainloop()

    def offerTrade(self,n_give,n_take):

        root = Tk()

        res = ['brick','ore','sheep','wheat','wood']

        offering = 'Offering: ' + ' ,'.join([str(n)+ ' '+ r for n,r in zip(n_give,res) if n != 0])
        wants = 'For: ' + ' ,'.join([str(n)+ ' '+ r for n,r in zip(n_take,res) if n != 0])

        for n,r in zip(n_give,res):

            if self.game.current_player.hand[r] < n:
                root.destroy()

        takers = []

        for player in self.game.players:

            lacking = False
            for n,r in zip(n_take,res):

                if player.hand[r] < n:

                    lacking = True

            if not lacking:
                takers.append(player)

        Label(root,text = offering).grid(row = 0)
        Label(root,text = wants).grid(row = 1)
        Label(root,text = 'Who wants to take it? (Enter Name)').grid(row=2)
        e1 = Entry(root)
        e1.grid(row=3)

        def takeTrade():
            name = e1.get()

            if name not in self.game.player_dic:
                root.destroy()

            elif self.game.player_dic[name] in takers:

                for n,r in zip(n_take,res):
                    self.game.current_player.hand[r] += n
                    self.game.player_dic[name].hand[r] -= n

                for n,r in zip(n_give,res):
                    self.game.player_dic[name].hand[r] += n
                    self.game.current_player.hand[r] -= n

            self.updateHand()
            self.game.availableMoves()
            root.destroy()



        Button(root, text = 'Take Trade', command= takeTrade).grid(row=4,column=0)
        Button(root, text = 'None One Wants It', command = root.destroy).grid(row=4,column=1)


        if len(takers) == 0:
            root.destroy()


