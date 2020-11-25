"""
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Simply randomly picks from possible moves
"""
import pygame
import timeit
import random

from Utils import Queue, COLOR, AddList, MouseCheckRect, DrawTextMultiline, DrawText, DrawBoard, DrawHistory, UIButton, DrawButton, PrintColor

import ReversiGame

##############################
# Include AI here

from Agents import ExampleRandom, ExampleGreedy, CellValue, Nayeon, WhopperHunterNaYeon, hyun, LHM, ppp, Predictor
# from Agents import Predictor

##############################


def MouseDownModePractice():
    if DEBUG_LEVEL >= 2:
        PrintColor("GUI: Practice Mode Clicked", 'magenta')
    VAR.ButtonsMode.modePractice.clicked = True
    VAR.ButtonsMode.modePractice.highlight = True
    VAR.ButtonsMode.modeContest.highlight = False
    VAR.mode = 0

def MouseDownModeContest():
    if DEBUG_LEVEL >= 2:
        PrintColor("GUI: Contest Mode Clicked", 'magenta')
    VAR.ButtonsMode.modeContest.clicked = True
    VAR.ButtonsMode.modePractice.highlight = False
    VAR.ButtonsMode.modeContest.highlight = True
    VAR.mode = 1

def Reset():
    if DEBUG_LEVEL >= 2:
        PrintColor("Initialize Called", 'yellow')
    VAR.game.Initialize()
    VAR.timeSeg = [None, [], []]
    VAR.miss = [None, 0, 0]
    VAR.state = 0
    for i in range(1,3):
        if VAR.player[i] != None:
            try:
                VAR.player[i].Initialize(VAR.game, i)
                if DEBUG_LEVEL >= 2:
                    PrintColor("Agent %24s Initalize() Executed"%(type(VAR.player[i]).__name__), 'green')
            except:
                if DEBUG_LEVEL >= 1:
                    PrintColor("Agent %24s failed to execute: Initialize()"%(type(VAR.player[i]).__name__), 'red')
            
def Start():
    if DEBUG_LEVEL >= 2:
        PrintColor("Start Called", 'yellow')
    Reset()
    VAR.state = 1

def MouseDownPracticeReset():    
    if DEBUG_LEVEL >= 2:
        PrintColor("GUI: Practice - Reset Clicked", 'magenta')
    VAR.ButtonsPractice.reset.clicked = True
    VAR.repeat = False
    Reset()

def MouseDownPracticeRepeat():
    if DEBUG_LEVEL >= 2:
        PrintColor("GUI: Practice - Repeat Clicked", 'magenta')
    VAR.ButtonsPractice.repeat.clicked = True
    VAR.repeat = not VAR.repeat

def MouseDownPracticeStart():
    if DEBUG_LEVEL >= 2:
        PrintColor("GUI: Practice - Start Clicked", 'magenta')
    VAR.ButtonsPractice.start.clicked = True
    Start()


DEBUG_LEVEL = 2

class Player:
    pass

class VAR:
    game = ReversiGame.Game()

    # History
    gameHistory = Queue()

    # Player [None:Player] [Class - Selected AI]
    player = [None, None, None]
    playerHighlight = [None, 0, 0]

    timeSeg = [None, [], []]
    miss = [None, 0, 0]
    
    ##############################
    # Put your agents also here
    AIAgents = [Player,
                ExampleRandom.ExampleRandom,
                ExampleGreedy.ExampleGreedy,
                CellValue.CellValue,
                Nayeon.Nayeon,
                WhopperHunterNaYeon.WhopperHunterNaYeon,
                hyun.hyun,
                LHM.LHM,
                Predictor.Predictor]
    
    ##############################

    # App mode [0:Practice] [1:Contest]
    mode = 0

    # App State for practice [0:Ready, mode and AI change is possible]
    state = 0
    repeat = False

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
        reset = UIButton([600, 100, 170, 50],"Reset", col=COLOR.blueBright, onMouseDown=MouseDownPracticeReset)
        start = UIButton([800, 100, 170, 50],"Start", col=COLOR.green, onMouseDown=MouseDownPracticeStart)
        repeat = UIButton([1000, 100, 170, 50],"Repeat", col=COLOR.grayBright, colHighlight=COLOR.redBright, onMouseDown=MouseDownPracticeRepeat)
        select = []
        selectPosition = [600, 160]


def Execute():
    if VAR.state == 1:
        # Execute AI
        if VAR.game.gamestate in [1,2]:
            g = VAR.game.gamestate
            if VAR.player[g] != None:
                t_ = timeit.default_timer()
                try:
                    pp = VAR.player[g].NextMove(VAR.game, g)
                    v = VAR.game.PlacePiece(g, pp)
                    if DEBUG_LEVEL >= 3:
                        PrintColor("Agent %24s placed %s piece to %s"%(type(VAR.player[g]).__name__, "Black" if g == 1 else "White", str(pp)))
                except:
                    v = False
                    if DEBUG_LEVEL >= 1:
                        PrintColor("Agent %24s failed to execute: NextMove()"%(type(VAR.player[g]).__name__), 'red')
                VAR.timeSeg[g].append(timeit.default_timer()-t_)
                if not v: # Place at random position
                    VAR.miss[g] += 1
                    ind = random.randint(0,len(VAR.game.GetPossiblePositions(g))-1)
                    VAR.game.PlacePiece(g, VAR.game.GetPossiblePositions(g)[ind])
    if VAR.state == 1 and VAR.game.gamestate in [3, 4, 5]:
        for i in range(1,3):
            try:
                VAR.player[i].Finish(VAR.game, i)
                if DEBUG_LEVEL >= 2:
                    PrintColor("Agent %24s Finish() Executed"%(type(VAR.player[i]).__name__), 'blue')
            except:
                if DEBUG_LEVEL >= 1:
                    PrintColor("Agent %24s failed to execute: Finish()"%(type(VAR.player[i]).__name__), 'red')
        VAR.state = 0
        VAR.gameHistory.Append(VAR.game.gamestate - 3)
        if VAR.repeat:
            Reset()
            VAR.state = 1


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
        if VAR.state == 1:
            VAR.ButtonsPractice.start.active = False
        else:
            VAR.ButtonsPractice.start.active = True
        DrawButton(screen, VAR.ButtonsPractice.start)
        VAR.ButtonsPractice.repeat.highlight = VAR.repeat
        DrawButton(screen, VAR.ButtonsPractice.repeat)

        # Selection Draw
        t = [None, "Black", "White"]
        for i in range(1,3):
            bp = AddList(VAR.ButtonsPractice.selectPosition, [(i-1)*330,0])
            DrawText(screen, AddList(bp, [0,0]), t[i] + " Player")
            if len(VAR.timeSeg[i]) == 0:
                seg = 0
            else:
                seg = VAR.timeSeg[i][-1]
            s = "Segment Time %2.4f\nTime Total % 2.4f\nMiss %d"%(seg,sum(VAR.timeSeg[i]),VAR.miss[i])
            DrawTextMultiline(screen, AddList(bp, [0,40]), s)
            
            for ia in range(len(VAR.AIAgents)):
                DrawButton(screen, VAR.ButtonsPractice.select[i-1][ia])
        # Set Highlight Active
        for i in range(1,3):
            for ix in range(len(VAR.AIAgents)):
                VAR.ButtonsPractice.select[i-1][ix].highlight = False # Highlight 
            VAR.ButtonsPractice.select[i-1][VAR.playerHighlight[i]].highlight = True

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
    elif VAR.mode == 0: # Practice Mode
        if MouseCheckRect(mouse, VAR.ButtonsPractice.reset.rect):
            VAR.ButtonsPractice.reset.onMouseDown()
        elif MouseCheckRect(mouse, VAR.ButtonsPractice.start.rect):
            VAR.ButtonsPractice.start.onMouseDown()
        elif MouseCheckRect(mouse, VAR.ButtonsPractice.repeat.rect):
            VAR.ButtonsPractice.repeat.onMouseDown()
        if VAR.state == 0:
            for i in range(1,3):
                for ix in range(len(VAR.AIAgents)): # Activator
                    if MouseCheckRect(mouse, VAR.ButtonsPractice.select[i-1][ix].rect):
                        VAR.ButtonsPractice.select[i-1][ix].clicked = True
                        if ix == 0:
                            VAR.player[i] = None
                            if DEBUG_LEVEL >= 2:
                                PrintColor("Agent %d Changed to Player"%(i), 'yellow')
                        else:
                            VAR.player[i] = VAR.AIAgents[ix]()
                            if DEBUG_LEVEL >= 2:
                                PrintColor("Agent %d Changed to %s"%(i, type(VAR.player[i]).__name__), 'yellow')
                        VAR.playerHighlight[i] = ix



def EventMouseUp():
    VAR.ButtonsMode.modePractice.clicked = False
    VAR.ButtonsMode.modeContest.clicked = False
    VAR.ButtonsPractice.reset.clicked = False
    VAR.ButtonsPractice.start.clicked = False
    VAR.ButtonsPractice.repeat.clicked = False
    for b in VAR.ButtonsPractice.select[0]:
        b.clicked = False
    for b in VAR.ButtonsPractice.select[1]:
        b.clicked = False

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
