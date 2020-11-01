from game import Game
from player import Player
from robot import Robot
import random
import copy
import functools


def getState(game):
   # homes,cities,roads = game.availableMoves()
    playerBoard =  [[0]*21 for i in range(11)]
    opposingBoard = [[0]*21 for i in range(11)]

    for i in range(len(game.board.vertices)):
        for q in range(len(game.board.vertices[0])):
            if game.board.vertices[i][q]:
                if game.board.vertices[i][q].owner == game.current_player:
                    playerBoard[i*2][q*2] = 1 + int(game.board.vertices[i][q] == True)
                elif game.board.vertices[i][q].owner:
                    opposingBoard[i*2][q*2] = 1

            if ((i,q),(i,q+1)) in game.board.edges:
                if game.board.edges[((i,q),(i,q+1))].owner == game.current_player:
                    playerBoard[i*2][q*2+1] = 1
                elif game.board.edges[((i,q),(i,q+1))].owner:
                    opposingBoard[i*2][q*2+1] = 1

            if ((i,q),(i+1,q)) in game.board.edges:
                if game.board.edges[((i,q),(i+1,q))].owner == game.current_player:
                    playerBoard[i*2+1][q*2] = 1
                elif game.board.edges[((i,q),(i+1,q))].owner:
                    opposingBoard[i*2+1][q*2] = 1

    state = [playerBoard,opposingBoard]
    for key in game.current_player.hand:
        state.append([[game.current_player.hand[key]]*21 for i in range(11)])

    state.append([[len(game.current_player.cities)]*21 for i in range(11)])
    state.append([[game.current_player.played_knights]*21 for i in range(11)])
    state.append([[game.current_player.point_cards]*21 for i in range(11)])

    return state

def switch(game,state,r1,r2,v1,v2):
    hand = game.current_player.hand
    key_index = {key:i+2 for key,i in zip(hand.keys(),list(range(5)))}
    c_state = copy.deepcopy(state)
    c_state[key_index[r1]] = [[hand[r1] - v1]*21]*11
    c_state[key_index[r2]] = [[hand[r2] + 1]*21]*11
    return c_state

def processActions(game,state):

    actions = [['E',[]]]
    new_states = [copy.deepcopy(state)]
    game.availableMoves()
    moves = game.moves
    shtetles = moves['settlements']

    for i in range(len(shtetles)):
        for q in range(len(shtetles[0])):
            if shtetles[i][q]:
                c_state = copy.deepcopy(state)
                # board level
                c_state[0][i*2][q*2] = 1
                actions.append(['S',(i,q)])
                new_states.append(c_state)

    cities = [[]]
    if 'cities' in moves:
        cities = moves['cities']

    for i in range(len(cities)):
        for q in range(len(cities[0])):
            if cities[i][q]:
                c_state = copy.deepcopy(state)
                # board level
                c_state[0][i*2][q*2] = 2
                actions.append(['C',(i,q)])
                new_states.append(c_state)


    roads = moves['roads']
    for v1,v2 in roads:

        c_state = copy.deepcopy(state)
        #downwards road
        if v2[0] - v1[0] == 1:
            #board level
            c_state[0][v1[0]*2+1][v1[1]*2] = 1

        #sideways road
        else:
            c_state[0][v1[0]*2][v1[1]*2+1] = 1

        actions.append(['R',(v1,v2)])
        new_states.append(c_state)

    #trades
    hand = game.current_player.hand
    for resource in hand.keys():

        if game.current_player.ports[resource] and hand[resource] >= 2:
            for el in hand.keys():
                if el != resource:
                    new_states.append(switch(game,state,resource,el,2,1))
                    actions.append(['T',(resource,el,2,1)])

        elif hand[resource] >= 3 and  game.current_player.ports['3:1']:
            for el in hand:
                if el != resource:
                    new_states.append(switch(game,state,resource,el,3,1))
                    actions.append(['T',(resource,el,3,1)])

        elif hand[resource] >= 4:
            for el in hand:
                if el!= resource:
                    new_states.append(switch(game,state,resource,el,4,1))
                    actions.append(['T',(resource,el,4,1)])

    return new_states,actions

#this is where the network will be
def selectAction(game,new_states,actions):

    i = random.randint(0,len(actions)-1)
    if game.round < 2 and len(actions) > 1:
        i = random.randint(1,len(actions)-1)
    action,spec = actions[i]
    if action == 'S':
        game.buySettlement(game.current_player.name,spec)
    elif action == 'C':
        game.buyCity(game.current_player.name,spec)
    elif action == 'R':
        game.buyRoad(game.current_player.name,spec)
    elif action == 'T':
        game.current_player.hand[spec[0]] -= spec[2]
        game.current_player.hand[spec[1]] += spec[3]

    else:
        #print(game.current_player.name)
        #print(game.turn)
        #print(game.current_player.points)
        won = game.current_player.points >= 10
        game.turn += 1
        game.round = game.turn//3
        game.playerUpdate()
        if game.round > 1:
            game.rollDice()
        return won

@functools.lru_cache(maxsize= 50)
def permutations(to_drop,r,hand):

    if to_drop == 0:
        return [hand]
    if r == len(hand):
        return []

    h = list(hand)

    ans = []
    for i in range(min(hand[r],to_drop)+1):

        nh= h.copy()
        nh[r] = nh[r] - i
        for el in permutations(to_drop-i,r+1,tuple(nh)):
            ans.append(el)

    return ans

def dropCards(game):

    for player in game.players:
        total = sum(player.hand.values())
        if total > 7:
            to_drop = total//2

            perms = permutations(to_drop,0,tuple(player.hand.values()))
            #print(player.hand)
            #print(player.hand.values())
            #print(perms)
            randHand = perms[random.randint(0,len(perms)-1)]
            for key,i in zip(player.hand,range(5)):
                player.hand[key] = randHand[i]



def threeBot():

    bots = [Robot() for i in range(3)]
    game = Game(player_names = [bot.name for bot in bots])
    for i in range(500):
        if game.dieRoll == 7:
            dropCards(game)
        state = getState(game)
        new_states, actions = processActions(game,state)
        if selectAction(game,new_states,actions):
            print(i)
            break

threeBot()
