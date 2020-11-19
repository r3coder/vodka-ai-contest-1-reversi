"""
Agent name: Nayeon
Writer : Kim Jeonggyun
Contact : sslktong@dgist.ac.kr
Description : I Love NY
"""

class Nayeon:
    def __init__(self):
        self.scoreboard = [[0 for _ in range(10)] for _ in range(10)]
        self.fil = {}
        data = '''000000000 30.3001
000000120 -23.2217
000000121 10.0124
000000200 -50.3382
000000211 1.9738
000002111 -30.3341
000221111 10.9666
001001112 -3.44385
001021111 35.8619
002001002 10.2975
002001212 2.6724
021002001 -3.62696
021002002 -4.51827
100100100 50.3007
100120112 19.9092
100200121 4.12924
100200122 -0.466183
110120110 6.42528
110121111 1.36536
111120000 15.3322
111121001 35.4324
111122001 5.37869
111202001 -1.83038
111202002 -1.42722
111221001 30.4671
111221011 4.41673
111221021 -3.2873
112001002 -3.30868
112002001 -2.17426
120100120 -5.0268
120200000 5.16028
121001001 -4.16577
122002001 4.46733
200000200 -15.8881
200100112 -1.58567
200100120 -2.61318
200100121 1.1482
200100122 -1.68769
200121111 7.92742
200200100 -9.03515
200200122 -0.258548
202000002 7.5098
202001001 -0.373561
202001002 4.50907
202002001 3.96621
211021021 5.61547
212002001 -1.90782
221001001 -14.1863
221021011 11.474'''
        data = data.splitlines()
        for i in range(len(data)):
            data[i] = data[i].split()
            self.fil[data[i][0]] = float(data[i][1])

    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """

    def rotate(self, s):
        now = [[0 for _ in range(3)] for _ in range(3)]
        nxt = [[0 for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                now[i][j] = s[i * 3 + j]

        for i in range(3):
            for j in range(3):
                nxt[j][2 - i] = now[i][j]

        ret = ''
        for i in range(3):
            for j in range(3):
                ret += nxt[i][j]
        return ret

    def flip(self, s):
        now = [[0 for _ in range(3)] for _ in range(3)]
        nxt = [[0 for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                now[i][j] = s[i * 3 + j]

        for i in range(3):
            for j in range(3):
                nxt[i][2 - j] = now[i][j]

        ret = ''
        for i in range(3):
            for j in range(3):
                ret += nxt[i][j]
        return ret

    def Initialize(self, game, player):
        board = [[0 for _ in range(10)] for _ in range(10)]
        self.color = player + 2

        for i in range(10):
            for j in range(10):
                if i == 0 or i == 9 or j == 0 or j == 9:
                    board[i][j] = 1
                elif game.board[i - 1][j - 1] == 3:
                    board[i][j] = 1

        loc = [[0, 1], [1, 0], [1, 1], [-1, 1]]

        for i in range(1, 9):
            for j in range(1, 9):
                if board[i][j] == 1:
                    continue
                cnt = 0
                for k in range(4):
                    if board[i + loc[k][0]][j + loc[k][1]] == 1 or board[i - loc[k][0]][j - loc[k][1]] == 1:
                        cnt += 1
                if cnt == 4:
                    board[i][j] = 2


        for i in range(1, 9):
            for j in range(1, 9):
                s = ''
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        s += str(board[i + ii][j + jj])

                for k in range(4):
                    if s in self.fil:
                        self.scoreboard[i][j] = self.fil[s]
                    s = self.rotate(s)
                s = self.flip(s)
                for k in range(4):
                    if s in self.fil:
                        self.scoreboard[i][j] = self.fil[s]
                    s = self.rotate(s)
        

    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        board = [[0 for _ in range(10)] for _ in range(10)]

        for i in range(10):
            for j in range(10):
                if i == 0 or i == 9 or j == 0 or j == 9:
                    board[i][j] = 1
                elif game.board[i - 1][j - 1] != 0:
                    if game.board[i - 1][j - 1] == 1:
                        board[i][j] = 3
                    if game.board[i - 1][j - 1] == 2:
                        board[i][j] = 4
                    if game.board[i - 1][j - 1] == 3:
                        board[i][j] = 1

        position = self.get_possible_position(board, self.color)
        if len(position) == 0:
            return (-1, -1)

        mx = -999999999999
        for u in position:
            if self.scoreboard[u[0]][u[1]] > mx:
                mx = self.scoreboard[u[0]][u[1]]
                pos = u
        return (pos[0] - 1, pos[1] - 1)


    def get_possible_position(self, board, color):
        loc = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        ret = []
        for i in range(1, 9):
            for j in range(1, 9):
                if board[i][j] != 0:
                    continue
                for k in range(8):
                    x = i + loc[k][0]
                    y = j + loc[k][1]
                    opp_encounter = 0
                    while True:
                        if color == 3:
                            if board[x][y] == 4:
                                opp_encounter = 1
                            else:
                                break
                        else:
                            if board[x][y] == 3:
                                opp_encounter = 1
                            else:
                                break
                        x += loc[k][0]
                        y += loc[k][1]

                    if opp_encounter and board[x][y] == color:
                        ret.append((i, j))
                        break
        return ret;


    def BestChoice(self, board, turn, depth, skip):
        from copy import deepcopy

        if depth == 0:
            return ((-1, -1), self.score(board))

        position = self.get_possible_position(board, turn);
        if len(position) == 0:
            if skip:
                return ((-1, -1), self.score(board))
            else:
                return ((-1, -1), self.BestChoice(board, 7 - turn, depth, 1)[1])

        board_new = deepcopy(board)
        if turn == self.color:
            mx = -9999999999999
            for u in position:
                self.put(board_new, u[0], u[1], turn)
                if skip:
                    now = self.BestChoice(board_new, 7 - turn, depth, 0);
                else:
                    now = self.BestChoice(board_new, 7 - turn, depth - 1, 0);
                if now[1] > mx:
                    mx = now[1]
                    pos = u
            return (pos, mx)
        else:
            mi = 9999999999999
            for u in position:
                self.put(board_new, u[0], u[1], turn)
                if skip:
                    now = self.BestChoice(board_new, 7 - turn, depth, 0);
                else:
                    now = self.BestChoice(board_new, 7 - turn, depth - 1, 0);
                if now[1] < mi:
                    mi = now[1]
                    pos = u
            return (pos, mi)

    def score(self, board):
        ret = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if board[i][j] == self.color:
                    ret += self.scoreboard[i][j]
#                elif board[i][j] == 7 - self.color:
#                    ret -= self.scoreboard[i][j]
        return ret

    def put(self, board, i, j, color):
        loc = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        for k in range(8):
            x = i + loc[k][0]
            y = j + loc[k][1]
            opp_encounter = 0
            while 1:
                if color == 3:
                    if board[x][y] == 4:
                        opp_encounter = 1
                    else:
                        break
                else:
                    if board[x][y] == 3:
                        opp_encounter = 1
                    else:
                        break
                x += loc[k][0]
                y += loc[k][1]

            if opp_encounter and board[x][y] == color:
                ii = i
                jj = j
                while ii != x or jj != y:
                    board[ii][jj] = color
                    ii += loc[k][0]
                    jj += loc[k][1]


    """ Finish
        Called when every game is end. Use at your wish.
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def Finish(self, game, player):
        pass
