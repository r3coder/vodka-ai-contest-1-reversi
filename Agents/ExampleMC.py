"""
Agent name: Example Monte Carlo
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Select Best move decided by current state
"""

import random

class ExampleMC:
    def __init__(self):
        pass

    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Initialize(self, game, player):
        pass

    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        l = game.GetPossiblePositions(player)
        ll = []
        for i in l:
            ll.append(game.GetReversiblePiecesCount(player, i))
        return l[ll.index(max(ll))]
