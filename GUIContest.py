"""
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Simply randomly picks from possible moves
"""
import pygame
import timeit
import random

from Utils import Queue, COLOR, AddList, MouseCheckRect, DrawTextMultiline, DrawText, DrawBoard, DrawHistory, UIButton, DrawButton

import ReversiGame

##############################
# Include AI here

from Agents import ExampleRandom
from Agents import ExampleMC

##############################

def MouseDownModePractice():
    VAR.ButtonsMode.modePractice.clicked = True
    VAR.ButtonsMode.modePractice.highlight = True
    VAR.ButtonsMode.modeContest.highlight = False
    VAR.mode = 0

def MouseDownModeContest():
    VAR.ButtonsMode.modeContest.clicked = True
    VAR.ButtonsMode.modePractice.highlight = False
    VAR.ButtonsMode.modeContest.highlight = True
    VAR.mode = 1

def MouseDownPracticeAIChange(pl, index):
    VAR.player[pl] = VAR.AIAgents[index]

def MouseDownPracticeReset():
    VAR.game.Initialize()
    VAR.state = 0

def MouseDownPracticeStart():
    if VAR.state == 0:
        VAR.state = 1


class Player:
    pass

class VAR:
    game = ReversiGame.Game()

    # History
    gameHistory = Queue()

    # App State [0:Ready, mode and AI change is possible]
    state = 0

    # Player [None:Player] [Class - Selected AI]
    player = [None, None, None]
    
    ##############################
    # Put your agents also here
    AIAgents = [Player,
                ExampleRandom.ExampleRandom,
                ExampleMC.ExampleMC]
    ##############################

    # App mode [0:Practice] [1:Contest]
    mode = 0

    # Clock for FPS
    clock = None

    gamestateText = ["", "Current Player : Black", "Current Player : White", "Black Wins", "White Wins", "Game Draw"]
    class UI:
        boardPosition = [60, 60]
        boardCellSize = 60
    
    class ButtonsMode:
        modePractice = UIButton([600, 30, 300, 50],"Practice Mode", highlight=True, onMouseDown=MouseDownModePractice)
        modeContest = UIButton([930, 30, 300, 50],"Contest Mode", onMouseDown=MouseDownModeContest)

    class ButtonsPractice:
        reset = UIButton([600, 100, 150, 50],"Reset", onMouseDown=MouseDownPracticeReset)
        start = UIButton([800, 100, 150, 50],"Start", onMouseDown=MouseDownPracticeStart)
        select = []
        selectPosition = [600, 160]


##############################
# Include AI here
from Agents import ExampleRandom
from Agents import ExampleMC

##############################

def Execute():
    pass


def Draw(screen):
    # Fill Screen With White
    screen.fill((255, 255, 255))
    DrawText(screen, [10, 690], "fps:"+str(int(VAR.clock.get_fps())), font="Small")
    # Draw Gameboard and simple information
    DrawText(screen, AddList(VAR.UI.boardPosition, [0, -50]), VAR.gamestateText[VAR.game.gamestate])
    DrawBoard(screen, VAR.game, VAR.UI.boardPosition, VAR.UI.boardCellSize)
    _t1, _t2, _t3 = VAR.game.GetPiecesCount()
    DrawText(screen, AddList(VAR.UI.boardPosition, [VAR.UI.boardCellSize*8, VAR.UI.boardCellSize*8+10]), "B:{}, W:{}, E:{}".format(_t1, _t2, _t3), font="Small", align="rt")
    # Draw History (Below Gameboard)
    DrawHistory(screen, VAR.gameHistory, AddList(VAR.UI.boardPosition, [0, VAR.UI.boardCellSize*8+20]))

    # Draw menu buttons
    DrawButton(screen, VAR.ButtonsMode.modePractice)
    DrawButton(screen, VAR.ButtonsMode.modeContest)


    if VAR.mode == 0:
        # Draw practice buttons
        DrawButton(screen, VAR.ButtonsPractice.reset)
        DrawButton(screen, VAR.ButtonsPractice.start)

        # Selection Draw
        t = [None, "Black", "White"]
        for i in range(1,3):
            bp = AddList(VAR.ButtonsPractice.selectPosition, [(i-1)*330,0])
            DrawText(screen, AddList(bp, [0,0]), t[i] + " Player")
            s = "Segment Time %2.4f\nTime Total % 2.4f\nMiss %d"%(2,3,0)
            DrawTextMultiline(screen, AddList(bp, [0,40]), s)
            
            for ia in range(len(VAR.AIAgents)):
                DrawButton(screen, VAR.ButtonsPractice.select[i-1][ia])

    # Finally, Flip
    pygame.display.flip()

def EventMouseDown(mouse):
    # Check if input is in table
    if MouseCheckRect(mouse, [VAR.UI.boardPosition[0],VAR.UI.boardPosition[1], VAR.UI.boardCellSize*8, VAR.UI.boardCellSize*8]):
        # Game is available to input, app's state is in game, agent is player
        if VAR.game.gamestate in [1, 2] and VAR.state == 1 and VAR.player[VAR.game.gamestate] == None:
            cy = (mouse[0] - VAR.UI.boardPosition[0]) // VAR.UI.boardCellSize
            cx = (mouse[1] - VAR.UI.boardPosition[0]) // VAR.UI.boardCellSize
            VAR.game.PlacePiece(VAR.game.gamestate, (cx, cy))
    # Check title buttons
    elif MouseCheckRect(mouse, VAR.ButtonsMode.modePractice.rect):
        VAR.ButtonsMode.modePractice.onMouseDown()
    elif MouseCheckRect(mouse, VAR.ButtonsMode.modeContest.rect):
        VAR.ButtonsMode.modeContest.onMouseDown()

def EventMouseUp():
    VAR.ButtonsMode.modePractice.clicked = False
    VAR.ButtonsMode.modeContest.clicked = False
    VAR.ButtonsPractice.reset.clicked = False
    VAR.ButtonsPractice.start.clicked = False

def Main():
    pygame.init()
    VAR.clock = pygame.time.Clock()

    # Create buttons
    for i in range(1,3):
        k = []
        for ia in range(len(VAR.AIAgents)):
            b = UIButton([
                VAR.ButtonsPractice.selectPosition[0]+330*(i-1),
                VAR.ButtonsPractice.selectPosition[1]+150+40*ia,
                300,30],"%s"%VAR.AIAgents[ia].__name__,textFont="Small")
            k.append(b)
        VAR.ButtonsPractice.select.append(k)

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