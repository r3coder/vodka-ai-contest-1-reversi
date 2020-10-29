"""
Agent name: Example Random Agent
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Simply randomly picks from possible moves
"""

import random

class ExampleRandom:
    def __init__(self):

        self.Initialize()

    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
    """
    def Initialize(self):
        pass

    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        l = game.GetPossiblePositions(player)
        ind = random.randint(0,len(l)-1)
        return l[random.randint(0,len(l)-1)]
