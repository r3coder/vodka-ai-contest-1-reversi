
# Import Basic Objects
import numpy as np


class Game:
    """
    Renegade Basic Rules
    1. Black always start first
    2. The player Have to place a piece on their turn if it is possible to place
    3. Players have to place a valid move on their turn
    4. If the player is not able to place a piece, then player have to skip the turn
    """
    def __init__(self, args=None):
        
        # State of the game [1:Black Turn] [2:White Turn] [3:Black win] [4:White win] [5:Draw]
        # Initial game state start from black's turn
        self.gamestate = 1

        # board information [0:empty] [1:black piece] [2:white piece]
        self.board = np.zeros((8,8))

        # history of placed values
        self.history = list()

        # Initialize Game
        self.Initialize()

    # Initialize the board
    def Initialize(self, preset=None):
        # Start with black
        self.gamestate = 1 

        # Reset History
        self.history = list()

        # Preset board
        self.board.fill(0)
        self.board[3,3] = 2
        self.board[3,4] = 1
        self.board[4,3] = 1
        self.board[4,4] = 2

    # Update the game progress
    def CheckGame(self):
        if not self.CheckPlayerIsAvailable(1) and not self.CheckPlayerIsAvailable(2):
            b, w, _ = self.GetPiecesCount()
            # Check gamestate
            if b == w:
                self.gamestate = 5
            elif b > w:
                self.gamestate = 3
            else:
                self.gamestate = 4
        pass
    

    # Check if a player is unavailable to place a piece
    def CheckPlayerIsAvailable(self, player):
        assert type(player) is int and player in [1, 2]
        if len(self.GetPossiblePositions(player)) > 0:
            return True
        return False

    """ PiecesCount
        Return number of pieces
        = return(int, int, int) black pieces, white pieces, empty pieces
    """
    def GetPiecesCount(self):
        pb = 0
        pw = 0
        for ix in range(8):
            for iy in range(8):
                if self.board[ix, iy] == 1:
                    pb += 1
                elif self.board[ix, iy] == 2:
                    pw += 1
        return pb, pw, 64-pb-pw
    
    # Changes Activated Player
    def ChangePlayer(self):
        if self.gamestate == 1:
            self.gamestate = 2
        elif self.gamestate == 2:
            self.gamestate = 1

    """ PlacePiece
        Place the piece, and return true if it was possible to place.
        - player(int) player to place the piece, [1:Black] [2:White]
        - pos(tuple(int, int)) pos of position to place the piece ([0, 7], [0, 7])
        = return(blue) true if piece is placed, false if piece is not placed
    """
    def PlacePiece(self, player, pos):
        assert type(player) is int and player in [1, 2]
        assert type(pos) is tuple
        assert type(pos[0]) is int and pos[0] >= 0 and pos[0] <= 7
        assert type(pos[1]) is int and pos[1] >= 0 and pos[1] <= 7

        # Gamestate doesn't allow to place pieces
        if self.gamestate not in [1, 2]:
            return False

        if pos in self.GetPossiblePositions(player):
            self.board[pos] = player
            for idd in range(8):
                dpl = self.GetDirectionPositions(idd, pos)
                # Check the placeablilty
                place = False
                if len(dpl) < 2:
                    continue
                for val in dpl:
                    if self.board[val] == 0: # If there is empty Square then skip
                        break
                    elif self.board[val] == player: # Found pieces to reverse
                        place = True
                        break
                if place:
                    for val in dpl:
                        if self.board[val] == player:
                            break
                        self.board[val] = player
            self.ChangePlayer()
            # Append Data to history
            self.history.append(pos)
            # If opponent's move is unavailable, return turn
            if len(self.GetPossiblePositions(self.gamestate)) == 0:
                self.ChangePlayer()
            self.CheckGame()
            return True
        else:
            return False

    """ GetReversiblePiecesCount
        Get the count of the reversible pieces
        - player(int) player to find the reversible pieces
        - pos(tuple(int, int)) position to find
        = return(int) number of piece that is reversible
    """
    def GetReversiblePiecesCount(self, player, pos):
        assert type(player) is int and player in [1, 2]
        assert type(pos) is tuple
        assert type(pos[0]) is int and pos[0] >= 0 and pos[0] <= 7
        assert type(pos[1]) is int and pos[1] >= 0 and pos[1] <= 7
        out = 0
        # Try place at position and check it is placed
        for idd in range(8):
            dpl = self.GetDirectionPositions(idd, pos)
            if len(dpl) < 2:
                continue
            for idl, val in enumerate(dpl):
                if self.board[val] == 0: # If there is empty Square then skip
                    break
                elif self.board[val] == player: # Found pieces to reverse
                    out += idl
                    break
        return out

    """ GetPossiblePositions
        Get the possible positions of the player on that board's state
        - player(int) player to find the possible position
        = return(list of tuple(int, int)) that contains possible positions
    """
    def GetPossiblePositions(self, player):
        assert type(player) is int and player in [1, 2]
        out = list()
        for idx in range(8):
            for idy in range(8):
                if self.board[idx, idy] != 0:
                    continue
                if self.GetReversiblePiecesCount(player, (idx, idy)) > 0:
                    out.append((idx, idy))
                
        return out

    """ GetDirectionPositions
        Get the list of the position on specific directions
        - direction(int) direction of the view, [0:right] [1:right down] [2:down] [3:left down] [4:left] [5:left up] [6:up] [7:right up]
        - pos(tuple (int, int)) location to check
        > includeSelf(bool) if this is true, list doesn't includes self
        = return(list of tuple(int, int)) that contains possible positions
    """
    def GetDirectionPositions(self, direction, pos, includeSelf=False):
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


