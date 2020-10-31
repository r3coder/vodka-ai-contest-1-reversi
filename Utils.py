

class Queue:
    def __init__(self, len=20):
        self.cap = len
        self.size = 0
        self.data = list()
    
    def Append(self, data):
        if self.size < self.cap:
            self.data.append(data)
            self.size += 1
        else:
            del self.data[0]
            self.data.append(data)

    def Pop(self):
        v = self.data[0]
        del self.data[0]
        self.size -= 1
        return v

    def Get(self, index):
        assert index < self.size
        return self.data[index]

    def Clear(self):
        self.data = list()
        self.size = 0


def AddList(l1, l2):
    assert len(l1) == len(l2)
    out = list()
    for i in range(len(l1)):
        out.append(l1[i]+l2[i])
    return out

import pygame

class COLOR:
    black = (0,0,0)
    white = (255,255,255)
    gray = (100,100,100)
    red = (255,0,0)
    redBright = (200, 60, 60)
    redDark = (90, 0, 0)
    green = (0,255,0)
    greenBright = (60, 200, 60)
    blue = (0,0,255)

# Fonts
pygame.font.init()
fontFamily = "Hack" # Edit this as your preferred font
fontBig = pygame.font.SysFont(fontFamily, 30)
fontMiddle = pygame.font.SysFont(fontFamily, 24)
fontSmall = pygame.font.SysFont(fontFamily, 18)

def DrawText(screen, position, text, col=COLOR.black, font="Big", align="lt"):
    assert font in ["Big", "Middle", "Small"]
    if font == "Big":
        f = fontBig
    elif font == "Middle":
        f = fontMiddle
    elif font == "Small":
        f = fontSmall
    to = f.render(text, False, col)    
    tr = to.get_rect()
    if   align[0] == "l": # Align horizontal [l, c, r]
        tr.center = (position[0] + tr.w/2, tr.center[1])
    elif align[0] == "c": 
        tr.center = (position[0]         , tr.center[1])
    elif align[0] == "r":
        tr.center = (position[0] - tr.w/2, tr.center[1])
    if   align[1] == "t": # Align vertical [t, m, b]
        tr.center = (tr.center[0], position[1] + tr.h/2)
    elif align[1] == "m":
        tr.center = (tr.center[0], position[1])
    elif align[1] == "b":
        tr.center = (tr.center[0], position[1] - tr.h/2)
    screen.blit(to,tr)

def DrawBoard(screen, game, position=[60, 60], cellSize=60, pieceRadius=25, moveSize=10):
    r = position; cs = cellSize; ps = pieceRadius; ms = moveSize
    # Draw Cells
    for ix in range(8):
        for iy in range(8):
            if game.board[ix, iy] == 3:
                pygame.draw.rect(screen, COLOR.redDark, [r[0]+iy*cs, r[1]+ix*cs, cs, cs],0)
            else:
                pygame.draw.rect(screen, COLOR.greenBright, [r[0]+iy*cs, r[1]+ix*cs, cs, cs],0)
            pygame.draw.rect(screen, COLOR.black, [r[0]+iy*cs, r[1]+ix*cs, cs, cs],2)

    # Draw Pieces
    for ix in range(8):
        for iy in range(8):
            if game.board[ix, iy] == 1: # black player
                pygame.draw.circle(screen, COLOR.black, [r[0]+(iy+0.5)*cs, r[1]+(ix+0.5)*cs], ps)
            elif game.board[ix, iy] == 2: # white player
                pygame.draw.circle(screen, COLOR.white, [r[0]+(iy+0.5)*cs, r[1]+(ix+0.5)*cs], ps)
            else:
                continue

    # Draw Possible Moves
    if game.gamestate in [1, 2]:
        lpm = game.GetPossiblePositions(game.gamestate)
        for i in lpm:
            pygame.draw.rect(screen, COLOR.redBright, [r[0]+(i[1]+0.5)*cs-ms/2, r[1]+(i[0]+0.5)*cs-ms/2, ms,ms],0)

def DrawHistory(screen, his, position=[60, 540], cell=48):
    DrawText(screen, position, "Recent History", font="Middle")

    for i in range(20):
        if i >= his.size:
            continue
        if his.Get(i) == 0:
            col = COLOR.gray
        elif his.Get(i) == 1:
            col = COLOR.black
        elif his.Get(i) == 2:
            col = COLOR.white
        pygame.draw.circle(screen, COLOR.black, AddList(position, [(i%10+0.5)*cell, (i//10)*cell+60]), cell*0.45)
        pygame.draw.circle(screen, col, AddList(position, [(i%10+0.5)*cell, (i//10)*cell+60]), cell*0.4)
    