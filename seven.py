from player import Player
from tkinter import *

class Seven:

    def rolled(vis,players):
        vis.freeze = True
        need_to_drop = []
        vis.robber_move = True

        for player in players:
            if sum(list(player.hand.values())) > 7:
                need_to_drop.append(player)

        if len(need_to_drop) > 0:
            root = Tk()
            root.title('Seven Rolled')

            def checkIfDone():
                nonlocal  n_drop
                nonlocal player

                c_lab.configure(text = str(n_drop) +' to Drop')

                if n_drop == 0:

                    if len(need_to_drop) == 0:
                        vis.updateHand()
                        root.destroy()

                    else:
                        player = need_to_drop.pop()
                        n_drop = sum(list(player.hand.values()))//2

                        n_lab.configure(text = player.name)
                        wo_label.configure(text=str(player.hand['wood']))
                        o_label.configure(text=str(player.hand['ore']))
                        s_label.configure(text=str(player.hand['sheep']))
                        wh_label.configure(text=str(player.hand['wheat']))
                        b_label.configure(text=str(player.hand['brick']))


                        c_lab.configure(text = str(n_drop) +' to Drop')
                else:
                    wo_label.configure(text=str(player.hand['wood']))
                    o_label.configure(text=str(player.hand['ore']))
                    s_label.configure(text=str(player.hand['sheep']))
                    wh_label.configure(text=str(player.hand['wheat']))
                    b_label.configure(text=str(player.hand['brick']))

                    c_lab.configure(text = str(n_drop) +' to Drop')



            def removeBrick():
                nonlocal n_drop
                nonlocal player
                if player.hand['brick'] > 0 and n_drop > 0:
                    player.hand['brick'] -= 1
                    n_drop -= 1
                    checkIfDone()

            def removeOre():
                nonlocal n_drop
                nonlocal player
                if player.hand['ore'] > 0 and n_drop > 0:
                    player.hand['ore'] -= 1
                    n_drop -= 1
                    checkIfDone()

            def removeSheep():
                nonlocal n_drop
                nonlocal player
                if player.hand['sheep'] > 0 and n_drop > 0:
                    player.hand['sheep'] -= 1
                    n_drop -= 1
                    checkIfDone()

            def removeWheat():
                nonlocal n_drop
                nonlocal player
                if player.hand['wheat'] > 0 and n_drop > 0:
                    player.hand['wheat'] -= 1
                    n_drop -= 1
                    checkIfDone()

            def removeWood():
                nonlocal n_drop
                nonlocal player
                if player.hand['wood'] > 0 and n_drop > 0:
                    player.hand['wood'] -= 1
                    n_drop -= 1
                    checkIfDone()




            player = need_to_drop.pop()
            n_drop = sum(list(player.hand.values()))//2
            n_lab = Label(root,text=player.name)
            n_lab.grid(row=0,column=0)
            c_lab = Label(root,text=str(n_drop) + ' to Drop')
            c_lab.grid(row=0,column=1)

            #brick
            b_button = Button(root, text='Brick',command = removeBrick)
            b_button.grid(row=1,column=0)
            b_label = Label(root, text = str(player.hand['brick']))
            b_label.grid(row=1,column=1)

            #ore
            o_button = Button(root, text='Ore',command = removeOre)
            o_button.grid(row=2,column=0)
            o_label = Label(root, text = str(player.hand['ore']))
            o_label.grid(row=2,column=1)

            #sheep
            s_button = Button(root, text='Sheep',command = removeSheep)
            s_button.grid(row=3,column=0)
            s_label = Label(root, text = str(player.hand['sheep']))
            s_label.grid(row=3,column=1)

            #wood
            wo_button = Button(root, text='Wood',command = removeWood)
            wo_button.grid(row=5,column=0)
            wo_label = Label(root, text = str(player.hand['wood']))
            wo_label.grid(row=5,column=1)

            #wheat
            wh_button = Button(root, text='Wheat',command = removeWheat)
            wh_button.grid(row=4,column=0)
            wh_label = Label(root, text = str(player.hand['wheat']))
            wh_label.grid(row=4,column=1)

            root.mainloop()
