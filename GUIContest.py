"""
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Contest GUI
"""
import pygame
import timeit
import random
import numpy as np
import time

from Utils import Queue, COLOR, AddList, MouseCheckRect, DrawTextMultiline, DrawText, DrawBoard, DrawHistory, UIButton, DrawButton, PrintColor

import ReversiGame


from Agents import CellValue
from Agents import Nayeon
from Agents import WhopperHunterNaYeon
from Agents import hyun
from Agents import LHM
from Agents import ppp

def Start():
    if DEBUG_LEVEL >= 2:
        PrintColor("Start Called", 'yellow')
    Reset()
    VAR.state = 1

def MouseDownExecute():
    if DEBUG_LEVEL >= 2:
        PrintColor("GUI: Execute Clicked", 'magenta')
    VAR.Buttons.execute.clicked = True
    VAR.state = 1



DEBUG_LEVEL = 2

class Player:
    pass

class VAR:
    game = ReversiGame.Game()

    # Contest Setup
    playCount = 50
    playCurrent = 0
    playTable = list()

    # History
    gameHistory = Queue(length=playCount)

    # Player [Class - Selected AI]
    playerIndex = [None, None, None]

    timeSeg = [None, [], []]
    miss = [None, 0, 0]
    
    AIAgents = [CellValue.CellValue(),
                Nayeon.Nayeon(),
                WhopperHunterNaYeon.WhopperHunterNaYeon(),
                hyun.hyun(),
                LHM.LHM(),
                ppp.ppp()]
    
    agentWinrate = None # Winrate
    agentGamecount = None # Game done
    agentScores = list() # Obtained Score
    agentGames = list() # Win = 1, Loss = 2, Draw = 3

    # App State for practice [0:Ready, mode and AI change is possible]
    state = 0
    repeat = False

    # Clock for FPS
    clock = None

    gamestateText = ["", "Current Player : Black", "Current Player : White", "Black Wins", "White Wins", "Game Draw"]
    class UI:
        boardPosition = [60, 60]
        boardCellSize = 60

        infoPosition = [580, 30]
        gamePosition = [580, 400]
        controlPosition = [160, 560]

    class Buttons:
        execute = UIButton([340, 600, 140, 60],"Execute", col=COLOR.greenBright, onMouseDown=MouseDownExecute)

        select = []
        selectPosition = [600, 160]

# Setup Situation
def Setup():
    VAR.playCurrent = 0
    VAR.gameHistory.Clear()
    pass

# Initialize Game
def InitializeGame():
    VAR.game.Initialize()
    VAR.timeSeg = [None, [], []]
    VAR.miss = [None, 0, 0]
    
    for i in range(1,3):
        if VAR.playerIndex[i] != None:
            agent = VAR.AIAgents[VAR.playerIndex[i]]
            try:
                t_ = timeit.default_timer()
                agent.Initialize(VAR.game, i)
                VAR.timeSeg[i].append(timeit.default_timer()-t_)
                if DEBUG_LEVEL >= 2:
                    PrintColor("Agent %24s Initalize() Executed"%(type(agent).__name__), 'green')
            except:
                if DEBUG_LEVEL >= 1:
                    PrintColor("Agent %24s failed to execute: Initialize()"%(type(agent).__name__), 'red')
        
def Move():
    g = VAR.game.gamestate
    
    agent = VAR.AIAgents[VAR.playerIndex[g]]
    try:
        t_ = timeit.default_timer()
        pp = agent.NextMove(VAR.game, g)
        VAR.timeSeg[g].append(timeit.default_timer()-t_)
        v = VAR.game.PlacePiece(g, pp)
        if DEBUG_LEVEL >= 3:
            PrintColor("Agent %24s placed %s piece to %s"%(type(agent).__name__, "Black" if g == 1 else "White", str(pp)))
    except:
        v = False
        if DEBUG_LEVEL >= 1:
            PrintColor("Agent %24s failed to execute: NextMove()"%(type(agent).__name__), 'red')
    
    if not v: # Place at random position
        VAR.miss[g] += 1
        ind = random.randint(0,len(VAR.game.GetPossiblePositions(g))-1)
        VAR.game.PlacePiece(g, VAR.game.GetPossiblePositions(g)[ind])

def UpdateWinrate():
    for a in range(len(VAR.AIAgents)):
        if len(VAR.agentGames[a]) == 0:
            VAR.agentWinrate[a] = 0.0
        else:
            w = 0
            for i in VAR.agentGames[a]:
                if i == 1:
                    w += 1
            VAR.agentWinrate[a] = w / len(VAR.agentGames[a]) * 100


def Finish():
    for i in range(1,3):
        agent = VAR.AIAgents[VAR.playerIndex[i]]
        try:
            t_ = timeit.default_timer()
            agent.Finish(VAR.game, i)
            VAR.timeSeg[i].append(timeit.default_timer()-t_)
            if DEBUG_LEVEL >= 2:
                PrintColor("Agent %24s Finish() Executed"%(type(agent).__name__), 'blue')
        except:
            if DEBUG_LEVEL >= 1:
                PrintColor("Agent %24s failed to execute: Finish()"%(type(agent).__name__), 'red')

    # Handling End-game situations
    VAR.gameHistory.Append(VAR.game.gamestate - 3)

    # TODO : Record Log...?
    bp, wp = VAR.playerIndex[1], VAR.playerIndex[2]
    bs, ws = 0, 0
    g = VAR.game.gamestate
    if g == 3: # Black wins
        bs += 10
        VAR.agentGames[bp].append(1)
        VAR.agentGames[wp].append(2)
    elif g == 4:
        ws += 10
        VAR.agentGames[bp].append(2)
        VAR.agentGames[wp].append(1)
    else:
        bs += 5
        ws += 5
        VAR.agentGames[bp].append(3)
        VAR.agentGames[wp].append(3)

    bs -= min(VAR.miss[1], 5)
    ws -= min(VAR.miss[2], 5)
    bs -= min(max(sum(VAR.timeSeg[1]), 0), 5)
    ws -= min(max(sum(VAR.timeSeg[2]), 0), 5)
    VAR.agentGamecount[bp] += 1
    VAR.agentGamecount[wp] += 1
    VAR.agentScores[bp].append(bs)
    VAR.agentScores[wp].append(ws)

    UpdateWinrate()


def Execute():
    if VAR.state == 0: # Idle
        pass
    elif VAR.state == 1: # Triggers Start
        VAR.state = 2
    elif VAR.state == 2: # Initialize game
        play = True
        for i in range(1,3):
            if VAR.playerIndex[i] == None:
                PrintColor("Agent is not properly selected", 'red')
                VAR.state = 0
                play = False
        if VAR.playTable[VAR.playerIndex[1]][VAR.playerIndex[2]]:
            PrintColor("Already Played", 'red')
            VAR.state = 0
            play = False
        if play:
            InitializeGame()
            if DEBUG_LEVEL >= 2:
                PrintColor("Initialized Game", 'yellow')
            VAR.state = 3
    elif VAR.state == 3: # Game
        # Execute AI
        if VAR.game.gamestate in [1,2]:
            Move()
        else: # End of the game
            VAR.state = 4
    elif VAR.state == 4: # Pause
        Finish()
        if DEBUG_LEVEL >= 2:
            PrintColor("Finished Game", 'yellow')
        # Checks Everything is end
        VAR.playCurrent += 1
        if VAR.playCount > VAR.playCurrent:
            VAR.state = 5
        else:
            VAR.playTable[VAR.playerIndex[1]][VAR.playerIndex[2]] = True
            VAR.state = 0
    elif VAR.state == 5: # Sleep for 1 second and return to initialing       
        # time.sleep(1)
        VAR.state = 2


def Draw(screen):
    # Fill Screen With White
    screen.fill((255, 255, 255))
    DrawText(screen, [10, 690], "fps:"+str(int(VAR.clock.get_fps())), font="Small")
    
    # Draw Gameboard and simple information
    DrawText(screen, AddList(VAR.UI.boardPosition, [0, -50]), VAR.gamestateText[VAR.game.gamestate])
    DrawBoard(screen, VAR.game, VAR.UI.boardPosition, VAR.UI.boardCellSize)
    _t1, _t2, _t3 = VAR.game.GetPiecesCount()
    DrawText(screen, AddList(VAR.UI.boardPosition, [VAR.UI.boardCellSize*8, VAR.UI.boardCellSize*8+10]), "B:{}, W:{}, E:{}".format(_t1, _t2, _t3), font="Small", align="rt")
 
    DrawButton(screen, VAR.Buttons.execute)


    DrawText(screen, VAR.UI.infoPosition, "Information", col="brown")
    DrawText(screen, AddList(VAR.UI.infoPosition, (0, 60)), "Agent Name",col="brown", font="Middle")
    DrawText(screen, AddList(VAR.UI.infoPosition, (280, 60)), "%9s"%"Games",col="brown", font="Middle")
    DrawText(screen, AddList(VAR.UI.infoPosition, (420, 60)), "Win Rate",col="brown", font="Middle")
    DrawText(screen, AddList(VAR.UI.infoPosition, (560, 60)), "%8s"%"Score",col="brown", font="Middle")
    for i in range(len(VAR.AIAgents)):
        DrawText(screen, AddList(VAR.UI.infoPosition, (0, 100+i*35)), type(VAR.AIAgents[i]).__name__, font="Middle")
        DrawText(screen, AddList(VAR.UI.infoPosition, (280, 100+i*35)),
                "%4d/%4d"%(len(VAR.agentScores[i]), VAR.playCount * 2 * (len(VAR.AIAgents) - 1)), font="Middle")
        DrawText(screen, AddList(VAR.UI.infoPosition, (420, 100+i*35)),
                "%8s"%("%2.3f%%"%(VAR.agentWinrate[i])), font="Middle")
        DrawText(screen, AddList(VAR.UI.infoPosition, (560, 100+i*35)),
                "%8s"%("%4.2f"%(sum(VAR.agentScores[i]))), font="Middle")
        
        for j in range(len(VAR.AIAgents)):
            if i == j:
                continue
            if VAR.playTable[i][j]: # Already Played
                    continue
            a = AddList(VAR.UI.controlPosition, (i*25, j*25))
            b = UIButton((a[0], a[1], 20, 20), "")
            DrawButton(screen, b)
        
    DrawText(screen, VAR.UI.gamePosition, "Current Game", col="red")
    DrawText(screen, AddList(VAR.UI.gamePosition,(0,40)), "Black Player", col="black", font="Middle")
    if VAR.playerIndex[1] != None:
        DrawText(screen, AddList(VAR.UI.gamePosition,(0,70)), type(VAR.AIAgents[VAR.playerIndex[1]]).__name__, col="blue", font="Middle")
    DrawText(screen, AddList(VAR.UI.gamePosition,(300,40)), "White Player", col="black", font="Middle")
    if VAR.playerIndex[2] != None:
        DrawText(screen, AddList(VAR.UI.gamePosition,(300,70)), type(VAR.AIAgents[VAR.playerIndex[2]]).__name__, col="blue", font="Middle")
    # Draw History
    DrawHistory(screen, VAR.gameHistory, AddList(VAR.UI.gamePosition, [0, 120]), cell=32, div=20)

    # Finally, Flip
    pygame.display.flip()

def EventMouseDown(mouse):
    if VAR.state == 0:
        if MouseCheckRect(mouse, VAR.Buttons.execute.rect):
            VAR.Buttons.execute.onMouseDown()
        else:
            for i in range(len(VAR.AIAgents)):
                for j in range(len(VAR.AIAgents)):
                    if i == j:
                        continue
                    if VAR.playTable[i][j]: # Already Played
                        continue
                    a = AddList(VAR.UI.controlPosition, (i*25, j*25))
                    if MouseCheckRect(mouse, (a[0], a[1], 20, 20)):
                        VAR.playerIndex = [-1, i, j]
                        if DEBUG_LEVEL >= 2:
                            PrintColor("Selected (%d, %d)"%(i, j), 'yellow')
                        Setup()


def EventMouseUp():
    VAR.Buttons.execute.clicked = False

def Main():
    pygame.init()
    VAR.clock = pygame.time.Clock()

    l = len(VAR.AIAgents)
    VAR.agentGamecount = np.zeros(l, dtype="int")
    VAR.agentWinrate = np.zeros(l)
    for i in range(l):
        VAR.agentScores.append(list())
        VAR.agentGames.append(list())
        t = list()
        for j in range(l):
            t.append(False)
        VAR.playTable.append(t)

    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_icon(pygame.image.load("./Resources/logo.png"))
    pygame.display.set_caption("VODKA Reversi AI Contest")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Button down
                EventMouseDown(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                EventMouseUp()
        VAR.clock.tick(120)
        Draw(screen)
        Execute()

if __name__=="__main__":
    Main()
