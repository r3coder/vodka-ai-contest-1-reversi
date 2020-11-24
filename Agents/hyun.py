"""
Agent name: hyun
Contact : hyunsj05@dgist.ac.kr
"""


class hyun:
    def __init__(self):
        self.qq=True
        self.ed=[]
        self.sss=0
        self.f=[]
        self.myed=[]
        for i in range(2,6):
            for j in range(2,6):
                self.f.append((i,j))
        
    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def ch_ed(self,po):
        co=0
        s=[]
        d=[]
        for i in [1,0,-1]:
            for j in [1,0,-1]:
                if [i,j]!=[0,0]:
                    if self.a[po[0]+i][po[1]+j]==3:
                        co=co+1
                        s.append([po[0]+i,po[1]+j])
                        d.append([i,j])
        if co>4:
            return True
        if co==4:
            for p,i in enumerate(s):
                te=d[p]
                if [po[0]-te[0],po[1]-te[1]] in s:
                    co=co-1
                    if co<4:
                        return False
            return True
        return False
    def co_ed(self,map):
        self.a=list(map)
        for po,i in enumerate(self.a):
            self.a[po]=list(i)
        self.a.insert(0,[3,3,3,3,3,3,3,3,3,3])
        self.a.append([3,3,3,3,3,3,3,3,3,3])
        for i in range(1,10):
            self.a[i].insert(0,3)
            self.a[i].append(3)
        for po,i in enumerate(self.a):
            for po2,j in enumerate(i):
                if self.a[po][po2]==0:
                    c=self.ch_ed([po,po2])
                    if c:
                        self.ed.append((po-1,po2-1))
        return None
        
        
    def near(self,b):
        for po,i in enumerate(self.ed):
            if abs(b[0]-i[0])<2 and abs(b[1]-i[1])<2:
                return [po,i]
        return -1
    def near2(self,b):
        for po,i in enumerate(self.myed):
            if abs(b[0]-i[0])<2 and abs(b[1]-i[1])<2:
                return [po,i]
        return -1
    def Initialize(self, game, player):
        self.qq=True
        self.ed=[]
        self.myed=[]
        # self.co_ed(game.board)
        # print(self.ed)
    def getmypos(self,m,player):
        re=[]
        for p,i in enumerate(m):
            for p2,j in enumerate(i):
                if j==player:
                    re.append((p,p2))
        return re
    def dicision(self,pos,a):
        te=[]
        for j in a:
            tem=0
            for po,i in enumerate(pos):
                if abs(j[0]-i[0])<3 and abs(j[1]-i[1])<3:
                    tem+=1
            te.append(tem)
        return a[te.index(max(te))]
    def dicision2(self,pos,a):
        te=[]
        for j in a:
            tem=0
            for po,i in enumerate(pos):
                if abs(j[0]-i[0])<2 and abs(j[1]-i[1])<2:
                    tem+=1
            te.append(tem)
        return a[te.index(min(te))]
    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        l = game.GetPossiblePositions(player)
        if self.qq:
            self.co_ed(game.board)
            self.qq=False
        
        for i in l:
            if i in self.ed:
                self.ed.remove(i)
                self.myed.append(i)
                return i
        meme=self.getmypos(game.board, player)
        if player==1:
            me=self.getmypos(game.board, 2)
        if player==2:
            me=self.getmypos(game.board, 1)
        if len(meme)==1:
            ll = []
            for i in l:
                ll.append(game.GetReversiblePiecesCount(player, i))
            return l[ll.index(max(ll))]
        
        te=[]
        for i in l:
            if i in self.f:
                # print("small box",i)
                te.append(i)
                # return i
        if len(te):
            return self.dicision(meme,te)
        te=[]
        for i in l:
            if self.near(i)==-1 and self.near2(i)!=-1:
                return i
        if len(te):
            return self.dicision2(me,te)
        te=[]
        for i in l:
            if (0 in i) or (7 in i):
                return i
        if len(te):
            return self.dicision2(me,te)
        te=[]
        for i in l:
            if self.near(i)==-1:
                return i
        if len(te):
            return self.dicision(meme,te)
        
        return l[0]
    """ Finish
        Called when every game is end. Use at your wish.
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Finish(self, game, player):
        pass