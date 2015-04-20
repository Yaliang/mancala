
execfile("MancalaGUI.py")
from ywo130 import *

player1 = ywo130(1, Player.MINIMAX, 8)
player2 = ywo130(2, Player.CUSTOM)

startGame(player1, player2)