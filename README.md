# catan

The goal of this project is to create an AI for playing Catan. This initial version does not yet support an AI but can be used to play  3-4 person games of Catan. Simply download the repostiory and run using python main.py.

## Playing

These instruciton assume a knowledge of the rules of Catan. 

### Rolling Dice

Dice can be rolled by clicking Roll in the bottom left corner. One can play developemnt cards before rolling.
Note: a turn cannot be endedbefore rolling

### Picking up Cards

In this version you cannot forget to pick up cards, it is done automatically after the "dice" are rolled.

### Building Settlements, Roads, and Cities

In all of the above cases assuming you have the cards required to build you simply move the cursor to the position you want to build. If it's possible to build there you will see a grey house/road/city pop up. To buy it simply click.

### Building Developemnt Cards

This is done by click the Buy Dev Card button on the bottom right. The order of Development cards is determined randomly.

### Playing Development Cards

Development cards are played by clicking on the respective text in the white box. Year of plenty, knights, and monoploy will open a window pormpting further action. Note for a knight the robber needs to be moved first.

### Rolling a seven and moving the robber

When a seven is rolled the game will freeze while the three actions play out:
1) A window will open promping players who have more than 7 cards to drop cards. If no player has more than seven cards the window will not open.
2) The robber must be moved. In order to do that simply click on any tile on which you want to move the robber.
3) A window will pop up prompting the player to select which other player to take a card from.

### Trading with the Bank

To trade with the bank simply click the 'Trade In" button. A screen will pop up and prompy you to to choose what you trade in. Then another window will pop up prompting you to choose to choose what you want. You will always get the best deal based on your ports. If you don'thave suffiecient resources to trade nothing will happen.

### Trading with Others

Click the 'Trade Others' button. A screen will pop asking what you want to trade for what. Simply put in the number of each. If there are any players that can fulfill the trade a window will pop asking for the name of a player who would like to take the deal.

### Game ending

The game will not automatically end at ten points (mainly because I like to play passed that in three person games). So end whenever you want.



Note: If you are running certain versions of macOS you might get a segmenation fault error when exiting the program. My advice is to not worry about it.
