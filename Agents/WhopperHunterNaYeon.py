"""
Agent name: WhopperHunterNaYeon
Writer : Jungwan Woo
Contact : friendship1@dgist.ac.kr
Description : Whooper and NY is MINE
"""

import numpy as np
import collections
import random

class WhopperHunterNaYeon:
    def __init__(self):
        self.player = None
        self.board = np.zeros((10,10))
        self.score_map = np.zeros((10,10))
        self.turn_cnt = 0

    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Initialize(self, game, player):
        self.board = np.zeros((10,10))
        self.score_map = np.zeros((10,10))
        self.player = player
        self.turn_cnt = 0
        
        for x in range(8):
            for y in range(8):
                if game.board[x,y] == 3:
                    self.board[x+1,y+1] = game.board[x,y]
        for x in range(10):
            for c in [0, 9]:
                self.board[x, c] = 3
                self.board[c, x] = 3
        deq = collections.deque()
        
        for x in range(1, 9):
            for y in range(1, 9):
                adjs = self.board[get_4adjs_np(x,y)]
                cnt = np.count_nonzero(adjs == 3)
                if cnt >= 2:
                    self.score_map[x,y] = 256
                    deq.append((x,y))
        
        # print(self.board)
        while(len(deq)):
            x,y = deq.popleft()
            adjs = get_8adjs_arr(x, y)
            for ax, ay in adjs:
                if inbound_10(ax, ay) and self.score_map[ax, ay] == 0:
                    self.score_map[ax,ay] = self.score_map[x,y] / -2
                    # deq.append((ax, ay))

        deq_list = []
        for x in range(1, 9):
            for y in range(1, 9):
                adjs = self.board[get_4adjs_np(x,y)]
                cnt = np.count_nonzero(adjs == 3)
                if cnt == 1 and self.score_map[x,y] == 0:
                    self.score_map[x,y] = 128
                    deq_list.append((x,y))

        random.shuffle(deq_list)
        for it in deq_list:
            deq.append(it)

        while(len(deq)):
            x,y = deq.popleft()
            adjs = get_8adjs_arr(x, y)
            for ax, ay in adjs:
                if inbound_10(ax, ay) and self.score_map[ax, ay] == 0:
                    self.score_map[ax,ay] = self.score_map[x,y] / -2
                    deq.append((ax, ay))
        # print(self.score_map)

    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        l = game.GetPossiblePositions(player)
        ll = []
        for i in l:
            ll.append(self.score_map[i[0]+1, i[1]+1])
        putpnt = l[ll.index(max(ll))]
        # self.score_map[putpnt[0], putpnt[1]] = 
        
        rocks = list(game.GetPiecesCount())
        if rocks[player-1] == 1 and self.turn_cnt > 2: # Greedy
            l = game.GetPossiblePositions(player)
            ll = []
            for i in l:
                ll.append(game.GetReversiblePiecesCount(player, i))
            return l[ll.index(max(ll))]
            
        self.turn_cnt += 1
        return putpnt

    """ Finish
        Called when every game is end. Use at your wish.
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Finish(self, game, player):
        pass

    def Wantam(self, game, player):
        pass

def inbound_10(x, y):
    if x >= 0 and y >= 0 and x < 10 and y <10:
        return True
    else:
        return False

def get_4adjs_np(x, y):
    return np.asarray([x-1, x+1, x, x]), np.asarray([y, y, y-1, y+1])

def get_8adjs_arr(x, y):
    return [(x-1, y-1), (x, y+1), (x+1, y+1), (x-1, y), (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]