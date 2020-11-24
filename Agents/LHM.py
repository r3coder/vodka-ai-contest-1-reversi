"""
Agent name: LHM
Contact : chaos7ds@dgist.ac.kr
"""

import numpy

class LHM:
    def __init__(self):
        pass

    """ Initialize
        Called between every game, reset every other stuffs if you use in-game
    """
    def Initialize(self, game, player):
        pass

    def Finish(self, game, player):
        pass

    """ NextMove
        Called when every agent's turn. Should return the tuple. Also, move should be valid. Otherwise, it will skip this Agent's Turn
        - game(RenegadeGame) game object that holding game information
        = player(int) player [1:black] [2:white]
    """
    def NextMove(self, game, player):
        choices = game.GetPossiblePositions(player)
        """
        pq = [[], [], []]
        for i in choices:
            if i[0] == 0 or i[0] == 7 and i[1] == 0 or i[1] == 7:
                pq[0].append(i)
            elif i[0] == 0 or i[0] == 7 or i[1] == 0 or i[1] == 7:
                pq[1].append(i)
            else:
                pq[2].append(i)
        count = []
        for i in pq:
            if len(i) != 0:
                for j in i:
                    count.append(game.GetReversiblePiecesCount(player, j))
                return i[count.index(max(count))]"""
        max_of_partner = []
        partner = (player + 1) % 2 + 1
        for i in choices:
            board = numpy.copy(game.board)
            board[i[0], i[1]] = player
            dir_vec = [(0, 1), (1, 1), (1, 0), (1, -1),
                       (0, -1), (-1, -1), (-1, 0), (-1, 1)]
            for j in range(8):
                k = 1
                tmp = (i[0]+dir_vec[j][0]*k, i[1]+dir_vec[j][1]*k)
                if tmp[0] < 0 or tmp[0] > 7 or tmp[1] < 0 or tmp[1] > 7:
                    continue
                while board[tmp[0], tmp[1]] == partner:
                    board[tmp[0], tmp[1]] = player
                    k = k + 1
                    tmp = (i[0]+dir_vec[j][0]*k, i[1]+dir_vec[j][1]*k)
                    if tmp[0] < 0 or tmp[0] > 7 or tmp[1] < 0 or tmp[1] > 7:
                        break

            choices_of_partner = self.LocalGetPossiblePositions(partner, board)
            max_count = 0
            for j in choices_of_partner:
                tmp = self.LocalGetReversiblePiecesCount(partner, j, board)
                max_count = max(max_count, tmp)
            max_of_partner.append(max_count)
        return choices[max_of_partner.index(min(max_of_partner))]

    def LocalGetPossiblePositions(self, player, board):
        assert type(player) is int and player in [1, 2]
        out = list()
        for idx in range(8):
            for idy in range(8):
                if board[idx, idy] != 0:
                    continue
                if self.LocalGetReversiblePiecesCount(player, (idx, idy), board) > 0:
                    out.append((idx, idy))

        return out

    def LocalGetReversiblePiecesCount(self, player, pos, board):
        assert type(player) is int and player in [1, 2]
        assert type(pos) is tuple
        assert type(pos[0]) is int and pos[0] >= 0 and pos[0] <= 7
        assert type(pos[1]) is int and pos[1] >= 0 and pos[1] <= 7
        out = 0
        # Try place at position and check it is placed
        for idd in range(8):
            dpl = self.LocalGetDirectionPositions(idd, pos)
            if len(dpl) < 2:
                continue
            for idl, val in enumerate(dpl):
                if board[val] == 0 or board[val] == 3: # If there is empty square and hole, then skip
                    break
                elif board[val] == player: # Found pieces to reverse
                    out += idl
                    break
        return out

    def LocalGetDirectionPositions(self, direction, pos, includeSelf=False):
        assert type(direction) is int and direction >= 0 and direction <= 7
        assert type(pos) is tuple
        assert type(pos[0]) is int and pos[0] >= 0 and pos[0] <= 7
        assert type(pos[1]) is int and pos[1] >= 0 and pos[1] <= 7
        assert type(includeSelf) is bool

        out = list()
        if includeSelf:
            out.append(pos)
        while True:
            if   direction == 0:
                pos = (pos[0]+1, pos[1]  )
            elif direction == 1:
                pos = (pos[0]+1, pos[1]+1)
            elif direction == 2:
                pos = (pos[0]  , pos[1]+1)
            elif direction == 3:
                pos = (pos[0]-1, pos[1]+1)
            elif direction == 4:
                pos = (pos[0]-1, pos[1]  )
            elif direction == 5:
                pos = (pos[0]-1, pos[1]-1)
            elif direction == 6:
                pos = (pos[0]  , pos[1]-1)
            elif direction == 7:
                pos = (pos[0]+1, pos[1]-1)
            if pos[0] > 7 or pos[1] > 7 or pos[0] < 0 or pos[1] < 0:
                break
            out.append(pos)
        return out