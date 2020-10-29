"""
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Simply randomly picks from possible moves
"""
import pygame
import timeit

import RenegadeGame

rg = RenegadeGame.Game()

##############################
# Include AI here
from Agents import ExampleRandom
from Agents import ExampleMC

##############################


class GUI:
    appState = 0 # [0:Ready, 1:Start, 2:Finish]
    # Players [0:player] [1~:AIAgents]
    playerBlack = 1
    playerWhite = 2
    ##############################
    # Put your agents also here
    AIAgentsBlack = [None,
                ExampleRandom.ExampleRandom(),
                ExampleMC.ExampleMC()]
    ##############################
    AIAgentsWhite = []

    pBlackTimeSegment = []
    pBlackMiss = 0
    pWhiteTimeSegment = []
    pWhiteMiss = 0

    # Time
    class time:
        start = 0
        

    # Fonts
    pygame.font.init()
    font30 = pygame.font.SysFont('Comic Sans MS', 30)
    font15 = pygame.font.SysFont('Comic Sans MS', 18)
    # Colors
    class COL:
        black = (0, 0, 0)
        white = (255, 255, 255)
        lightRed = (255, 100, 100)

    # Text
    class textState:
        values = ["", "Current Player : Black", "Current Player : White", "Black Wins", "White Wins", "Game Draw"]
        X = 60
        Y = 10
    class textStatus:
        X = 60
        Y = 550

    # Buttons
    class buttonReset:
        active = True
        clicked = False
        rect = [570+ 10,  10+  10, 180,  60]
        colDisabled = ( 70,  70,  70)
        colIdle = (255, 200, 200)
        colClicked = (200, 150, 150)
        text = "Reset"
    class buttonStart:
        active = True
        clicked = False
        state = 1 # [0:Disabled] [1:Idle] [2:Clicked]
        rect = [770+ 10,  10+  10, 180,  60]
        colDisabled = ( 70,  70,  70)
        colIdle = (200, 255, 200)
        colClicked = (150, 200, 150)
        text = "Start"

    class agent:
        rect = [560, 100, 420, 480]
        pass

    # Cell
    class board:
        rect = [60, 60]
        cellSize = 60
        outlineCol = (0, 0, 0)
        fillCol = (60, 200, 60)
        pieceSize = 25


def CreateButton(screen, o):
    if not o.active:
        pygame.draw.rect(screen, o.colDisabled, o.rect, 0)
    elif o.clicked:
        pygame.draw.rect(screen, o.colClicked, o.rect, 0)
    else:
        pygame.draw.rect(screen, o.colIdle, o.rect, 0)
    pygame.draw.rect(screen, GUI.COL.black, o.rect, 2)
    t = GUI.font30.render(o.text, False, GUI.COL.black)
    tr = t.get_rect()
    tr.center = o.rect[0]+o.rect[2]/2, o.rect[1]+o.rect[3]/2
    screen.blit(t,tr)


def Draw(screen):
    screen.fill( GUI.COL.white )

    # Text State
    textState = GUI.font30.render(GUI.textState.values[rg.gamestate], False, GUI.COL.black)
    screen.blit(textState,(GUI.textState.X,GUI.textState.Y))
    sa, sb, sc = rg.GetPiecesCount()
    statusStr = "Black {}, White {}, Empty {}".format(sa, sb, sc)
    textStatus = GUI.font15.render(statusStr, False, GUI.COL.black)
    screen.blit(textStatus,(GUI.textStatus.X,GUI.textStatus.Y))
    
    # Draw Cells
    for ix in range(8):
        for iy in range(8):
            pygame.draw.rect(screen, GUI.board.fillCol,
                    [GUI.board.rect[0]+ix*GUI.board.cellSize,
                    GUI.board.rect[1]+iy*GUI.board.cellSize,
                    GUI.board.cellSize,GUI.board.cellSize],0)
            pygame.draw.rect(screen, GUI.board.outlineCol, 
                    [GUI.board.rect[0]+ix*GUI.board.cellSize,
                    GUI.board.rect[1]+iy*GUI.board.cellSize,
                    GUI.board.cellSize,GUI.board.cellSize],2)

    # Draw
    for ix in range(8):
        for iy in range(8):
            if rg.board[ix, iy] == 0:
                continue
            elif rg.board[ix, iy] == 1: # black player
                col = GUI.COL.black
            elif rg.board[ix, iy] == 2:
                col = GUI.COL.white
            
            pygame.draw.circle(screen, col,
                    [GUI.board.rect[0]+(ix+0.5)*GUI.board.cellSize,
                    GUI.board.rect[1]+(iy+0.5)*GUI.board.cellSize], GUI.board.pieceSize)

    # Reset Button and Start Button
    CreateButton(screen, GUI.buttonReset)
    CreateButton(screen, GUI.buttonStart)
    
    # Draw AI Selection
    # TODO : Code is quite Mess, fix later maybe?
    pygame.draw.rect(screen, GUI.COL.black, GUI.agent.rect, 2)
    # Black Side Text
    textPlayerBlack = GUI.font30.render("Black Side", False, GUI.COL.black)
    screen.blit(textPlayerBlack,(GUI.agent.rect[0]+10,GUI.agent.rect[1]+10))
    # White Side Text
    textPlayerBlack = GUI.font30.render("White Side", False, GUI.COL.black)
    screen.blit(textPlayerBlack,(GUI.agent.rect[0]+210,GUI.agent.rect[1]+10))
    # Stats
    if len(GUI.pBlackTimeSegment)>0:
        t = GUI.font15.render("T Seg:%.4f"%(GUI.pBlackTimeSegment[-1]), False, GUI.COL.black)
    else:
        t = GUI.font15.render("T Seg:0.0", False, GUI.COL.black)
    screen.blit(t,(GUI.agent.rect[0]+10,GUI.agent.rect[1]+50))
    t = GUI.font15.render("T Total:%.4f"%sum(GUI.pBlackTimeSegment), False, GUI.COL.black)
    screen.blit(t,(GUI.agent.rect[0]+10,GUI.agent.rect[1]+70))
    t = GUI.font15.render("Miss:%d"%GUI.pBlackMiss, False, GUI.COL.black)
    screen.blit(t,(GUI.agent.rect[0]+10,GUI.agent.rect[1]+90))
    if len(GUI.pWhiteTimeSegment)>0:
        t = GUI.font15.render("T Seg:%.4f"%(GUI.pWhiteTimeSegment[-1]), False, GUI.COL.black)
    else:
        t = GUI.font15.render("T Seg:0.0", False, GUI.COL.black)
    screen.blit(t,(GUI.agent.rect[0]+210,GUI.agent.rect[1]+50))
    t = GUI.font15.render("T Total:%.4f"%sum(GUI.pWhiteTimeSegment), False, GUI.COL.black)
    screen.blit(t,(GUI.agent.rect[0]+210,GUI.agent.rect[1]+70))
    t = GUI.font15.render("Miss:%d"%GUI.pWhiteMiss, False, GUI.COL.black)
    screen.blit(t,(GUI.agent.rect[0]+210,GUI.agent.rect[1]+90))
    # Draw Buttons
    pygame.draw.rect(screen, GUI.COL.lightRed, [GUI.agent.rect[0]+10,GUI.agent.rect[1]+120+40*GUI.playerBlack,180,30], 0)
    pygame.draw.rect(screen, GUI.COL.lightRed, [GUI.agent.rect[0]+10+210,GUI.agent.rect[1]+120+40*GUI.playerWhite,180,30], 0)
    for tw in range(2):
        for idx in range(len(GUI.AIAgentsWhite)):
            pygame.draw.rect(screen, GUI.COL.black, [GUI.agent.rect[0]+10+tw*210,GUI.agent.rect[1]+120+40*idx,180,30], 2)
            if idx == 0:
                t = GUI.font15.render("Player", False, GUI.COL.black)
            else:
                t = GUI.font15.render("%s"%type(GUI.AIAgentsWhite[idx]).__name__, False, GUI.COL.black)
            tr = t.get_rect()
            tr.center = (GUI.agent.rect[0]+10+90+tw*210,GUI.agent.rect[1]+120+40*idx+15)
            screen.blit(t,tr)
    
    # Draw Blocker if game is not playing
    if GUI.appState != 1:
        s = pygame.Surface((GUI.board.cellSize*8, GUI.board.cellSize*8))
        s.set_alpha(100)
        s.fill(GUI.COL.black)
        screen.blit(s, (GUI.board.rect[0], GUI.board.rect[1]))


    pygame.display.flip()


def MouseCheckRect(mouse, rect):
    if mouse[0]>=rect[0] and mouse[0]<rect[0]+rect[2] and mouse[1]>=rect[1] and mouse[1]<rect[1]+rect[3]:
        return True
    else:
        return False

def ResetGame():
    GUI.pBlackTimeSegment = []
    GUI.pBlackMiss = 0
    GUI.pWhiteTimeSegment = []
    GUI.pWhiteMiss = 0

    rg.Initialize()

def StartGame():
    GUI.time.start = timeit.default_timer()

def AgentAction():
    if GUI.playerBlack != 0 and rg.gamestate == 1 and GUI.appState == 1:
        v = rg.PlacePiece(1, GUI.AIAgentsBlack[GUI.playerBlack].NextMove(rg, 1))
        if v == False: # Skip turn
            GUI.playerBlack += 1
            rg.gamestate = 2
        a = timeit.default_timer()
        GUI.pBlackTimeSegment.append(a-GUI.time.start)
        GUI.time.start = a
    if GUI.playerWhite != 0 and rg.gamestate == 2 and GUI.appState == 1:
        v = rg.PlacePiece(2, GUI.AIAgentsBlack[GUI.playerWhite].NextMove(rg, 2))
        if v == False: # Skip turn
            GUI.playerWhite += 1
            rg.gamestate = 2
        a = timeit.default_timer()
        GUI.pWhiteTimeSegment.append(a-GUI.time.start)
        GUI.time.start = a
        

def MouseDown(mouse):
    # print(mouse[0], mouse[1])
    if mouse[0] >= GUI.board.rect[0] and mouse[0] < GUI.board.rect[0] + GUI.board.cellSize * 8 \
        and mouse[1] >= GUI.board.rect[1] and mouse[1] < GUI.board.rect[1] + GUI.board.cellSize * 8:
        cx = (mouse[0] - GUI.board.rect[0]) // GUI.board.cellSize
        cy = (mouse[1] - GUI.board.rect[1]) // GUI.board.cellSize
        # TODO : Place actions here
        if GUI.appState == 1:
            if GUI.playerBlack == 0 and rg.gamestate == 1:
                rg.PlacePiece(1, (cx, cy))
            if GUI.playerWhite == 0 and rg.gamestate == 2:
                rg.PlacePiece(2, (cx, cy))
    elif MouseCheckRect(mouse, GUI.buttonReset.rect):
        # Reset Button Clicked
        GUI.appState = 0
        GUI.buttonStart.active = True
        GUI.buttonReset.clicked = True
        ResetGame()
    elif MouseCheckRect(mouse, GUI.buttonStart.rect):
        if GUI.appState == 0:
            GUI.appState = 1
            GUI.buttonStart.clicked = True
            GUI.buttonStart.active = False
            StartGame()
    elif MouseCheckRect(mouse, GUI.agent.rect): # Select AI
        for idx in range(len(GUI.AIAgentsWhite)):
            if MouseCheckRect(mouse, [GUI.agent.rect[0]+10    ,GUI.agent.rect[1]+120+40*idx,180,30]):
                GUI.playerBlack = idx
            if MouseCheckRect(mouse, [GUI.agent.rect[0]+10+210,GUI.agent.rect[1]+120+40*idx,180,30]):
                GUI.playerWhite = idx

def MouseUp():
    GUI.buttonStart.clicked = False
    GUI.buttonReset.clicked = False


def Main():
    pygame.init()
    
    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_icon(pygame.image.load("./Resources/logo.png"))
    pygame.display.set_caption("VODKA Renegade AI Contest - Practice")
    running = True

    # Add every agents to white, too
    for i in GUI.AIAgentsBlack:
        GUI.AIAgentsWhite.append(i)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Button down
                MouseDown(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                MouseUp()
        AgentAction()
        Draw(screen)

if __name__=="__main__":
    Main()

    