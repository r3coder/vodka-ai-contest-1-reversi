"""
Agent name: Cell Value
Writer : Seunghyun Lee
Contact : coder@dgist.ac.kr
Description : Calculates cell values, and place pieces based on that values
"""

import random
import numpy as np

class CellValue:
    def __init__(self):
        pass


    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Initialize(self, game, player):
        # This is scoreboard, which stores values
        self.score = np.zeros((8,8),dtype=int)
        
        # Calculation of the tables
        
        # First step: calculate edge components
        self.holes = game.GetHolePositions()
        self.corner = np.zeros((8,8),dtype=int)
        for ix in range(8):
            for iy in range(8):
                if self.CheckDisabled((ix-1,iy-1)) or self.CheckDisabled((ix+1,iy+1)):
                    self.corner[ix,iy] += 1
                if self.CheckDisabled((ix  ,iy-1)) or self.CheckDisabled((ix  ,iy+1)):
                    self.corner[ix,iy] += 1
                if self.CheckDisabled((ix-1,iy+1)) or self.CheckDisabled((ix+1,iy-1)):
                    self.corner[ix,iy] += 1
                if self.CheckDisabled((ix-1,iy  )) or self.CheckDisabled((ix+1,iy  )):
                    self.corner[ix,iy] += 1
        for h in self.holes:
            self.corner[h] = 9
        
        # Second Step: Calculate the position based on the holes
        for ix in range(8):
            for iy in range(8):
                if self.corner[ix, iy] == 4: # Most important part - Not able to reverse if a piece is placed
                    self.score[ix, iy] += 100
                    for iex in range(-1, 2):
                        if ix+iex < 0 or ix+iex > 7:
                            continue
                        if iy-1 >= 0:
                            self.score[ix+iex, iy-1] -= 10
                        if iy+1 <= 7:
                            self.score[ix+iex, iy+1] -= 10
                    for iey in range(-1, 2):
                        if iy+iey < 0 or iy+iey > 7:
                            continue
                        if ix-1 >= 0:
                            self.score[ix-1, iy+iey] -= 10
                        if ix+1 <= 7:
                            self.score[ix+1, iy+iey] -= 10
                elif self.corner[ix, iy] == 3: # Edges
                    self.score[ix, iy] += 5
                else: # Center is still better than around cells
                    if ix <= 5 and ix >= 2 and iy <= 5 and iy >= 2:
                        self.score[ix, iy] = 1
        # -200 for holes...
        for ix in range(8):
            for iy in range(8):
                if (ix, iy) in self.holes:
                    self.score[ix, iy] = -200

    def CheckDisabled(self, pos):
        if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
            return True
        if pos in self.holes:
            return True
        return False

    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        locations = game.GetPossiblePositions(player)
        values = []
        for l in locations:
            values.append(self.score[l])
        maxV = max(values)
        res = []
        for i, l in enumerate(locations):
            if values[i] == maxV:
                res.append(l)
        ind = random.randint(0,len(res)-1)

        return res[ind]

    """ Finish
        Called when every game is end. Use at your wish.
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Finish(self, game, player):
        pass