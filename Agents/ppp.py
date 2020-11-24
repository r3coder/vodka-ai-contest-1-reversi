"""
Agent name: ppp
Contact : sg549@dgist.ac.kr
"""

import random
import time
import numpy as np

class ppp:
    def __init__(self):
        pass

    def Initialize(self, game, player):
        self.cooor=[(0,0),(7,0),(0,7),(7,7)]
        self.newcorner = []
        self.xxx2 = []
        self.xxx1=[]
        self.cnew=[]
        self.crrrr=[(0,1),(0,6),(1,0),(1,7),(6,0),(6,7),(7,1),(7,6)]
        self.xrrrr=[(1,1),(1,6),(6,1),(6,6)]
        holes=game.GetHolePositions()
        for i in holes:
            if i[0]==0:
                self.newcorner.append((0, i[1] + 1))
                self.newcorner.append((0, i[1] - 1))
                self.xxx1.append((1, i[1]))
                self.xxx2.append((1, i[1] - 2))
                self.xxx2.append((1, i[1] + 2))
                self.cnew.append((1, i[1] + 1))
                self.cnew.append((1, i[1] - 1))
            if i[0]==7:
                self.newcorner.append((7, i[1] + 1))
                self.newcorner.append((7, i[1] - 1))
                self.xxx1.append((6, i[1]))
                self.xxx2.append((6, i[1] - 2))
                self.xxx2.append((6, i[1] + 2))
                self.cnew.append((6, i[1] + 1))
                self.cnew.append((6, i[1] - 1))
            if i[1]==0:
                self.newcorner.append((i[0] + 1, 0))
                self.newcorner.append((i[0] - 1, 0))
                self.xxx1.append((i[0], 1))
                self.xxx2.append((i[1] - 2, 1))
                self.xxx2.append((i[1] + 2, 1))
                self.cnew.append((i[1] + 1, 1))
                self.cnew.append((i[1] - 1, 1))
            if i[1]==7:
                self.newcorner.append((i[0] + 1, 7))
                self.newcorner.append((i[0] - 1, 7))
                self.xxx1.append((i[0], 6))
                self.xxx2.append((i[1] - 2, 6))
                self.xxx2.append((i[1] + 2, 6))
                self.cnew.append((i[1] + 1, 6))
                self.cnew.append((i[1] - 1, 6))



    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Move(self,game,player,l):
        ll=[]
        lll=[]
        for i in range(len(l)):
            if l[i] in self.cooor:
                ll.append(game.GetReversiblePiecesCount(player, l[i]))
                lll.append(l[i])
        if len(ll)>0:
            return lll[ll.index(max(ll))]
        ll=[]
        lll=[]
        for i in range(len(l)):
            if l[i] in self.newcorner:
                ll.append(game.GetReversiblePiecesCount(player,l[i]))
                lll.append(l[i])
        if len(ll)>0:
            return lll[ll.index(max(ll))]
        ll=[]
        lll=[]
        for i in range(len(l)):
            if 1<l[i][0]<6 and 1<l[i][1]<6 :
                ll.append(game.GetReversiblePiecesCount(player,l[i]))
                lll.append(l[i])
        if len(ll)>0:
            if len(game.history)>8:
                return lll[ll.index(max(ll))]
            else:
                return lll[random.randint(0,len(ll)-1)]
        ll=[]
        lll=[]
        for i in range(len(l)):
            if l[i] not in (*self.xxx2, *self.xxx1, *self.cnew, *self.crrrr, *self.xrrrr):
                ll.append(game.GetReversiblePiecesCount(player,l[i]))
                lll.append(l[i])
        if len(ll)>0:
            return lll[ll.index(max(ll))]
        for j in [self.cnew, self.crrrr, self.xxx2, self.xxx1, self.xrrrr]:
            ll=[]
            lll=[]
            for i in range(len(l)):
                if l[i] in j:
                    ll.append(game.GetReversiblePiecesCount(player,l[i]))
                    lll.append(l[i])
            if len(ll)>0:
                return lll[ll.index(max(ll))]

    def NextMove(self, game, player):
        lbasic = list(game.GetPossiblePositions(player))
        badlist=[]
        goodlist=[]
        l=lbasic[:]
        for pos in l:
            reverselist=[0,0,0,0,0,0,0,0]
            reversesave=[0,0,0,0,0,0,0,0]
            for direction in range(8):
                posdirectionlist=game.GetDirectionPositions(direction,pos)
                if len(posdirectionlist)<2:
                    continue
                for index,temppos in enumerate(posdirectionlist):
                    # print(index,temppos,game.board[temppos])
                    if game.board[temppos]==0 or game.board[temppos]==3:
                        break
                    elif game.board[temppos]==player:
                        reverselist[direction]+=index
                        try:
                            if game.board[posdirectionlist[index+1]] not in [0,3,player]:
                                adfsa=(direction+4)%8
                                ttpos=game.GetDirectionPositions(adfsa,pos)
                                for ioio,tpos in enumerate(ttpos):
                                    ttstone=game.board(tpos)
                                    if ttstone==player:
                                        if ioio==len(ttpos)-1:
                                            reversesave[direction]=1
                                        continue
                                    elif ttstone==0:
                                        reversesave[direction] =-1
                                        break
                                    elif ttstone==3:
                                        break
                                    else:
                                        break
                            elif game.board[posdirectionlist[index+1]] in [0]:
                                adfsa = (direction + 4) % 8
                                ttpos = game.GetDirectionPositions(adfsa, pos)
                                if game.board[ttpos[0]] not in [0,3,player]:
                                    reversesave[direction]=-1
                        except:
                            pass
            if reverselist.count(0)==7:
                if sum(reversesave)<0:
                    try:
                        badlist.append(pos)
                    except:
                        pass
                    try:
                        l.remove(pos)
                    except:
                        pass

        #결과
        if len(l)<1:
            if len(badlist)<1:
                return self.Move(game,player,lbasic)
            else:
                return self.Move(game,player,badlist)
        else:
            return self.Move(game,player,l)
        # result = self.Move(game, player, l)
        # if result == None:
        #     result == self.Move(game, player, badlist)
        #     if result == None:
        #         return self.Move(game.player, lbasic)
        #     else:
        #         return result
        # else:
        #     return result







        # print('gamestate')
        # print(game.gamestate)
        # print('board')
        # print(game.board)
        # print('history')
        # print(game.history)
        # print('getholepositions')
        # print(game.GetHolePositions())
        # print('get piecescount()')
        # print(game.GetPiecesCount())
        # print('getreversiblepiece')
        # print(game.GetReversiblePiecesCount(player, (2, 2)))
        # print('get possible position')
        # print(game.GetPossiblePositions(player))
        # print('getdirectionpositon')
        # print(game.GetDirectionPositions(7, (4, 4)))
        # print('^^')
        # print()
        # print()
        # print(l)
        # print(ll)




    def Finish(self, game, player):
        pass

    def Findlast():
        pass