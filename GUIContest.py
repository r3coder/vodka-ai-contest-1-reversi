"""
Writer : Lee Seunghyun
Contact : coder@dgist.ac.kr
Description : Simply randomly picks from possible moves
"""
import pygame
import timeit
import random

from Utils import Queue, COLOR, AddList, DrawText, DrawBoard, DrawHistory

import ReversiGame

class VAR:
    game = ReversiGame.Game()

    gameHistory = Queue()

    gamestateText = ["", "Current Player : Black", "Current Player : White", "Black Wins", "White Wins", "Game Draw"]
    class UI:
        boardPosition = [60, 60]
        boardCellSize = 60

##############################
# Include AI here
from Agents import ExampleRandom
from Agents import ExampleMC

##############################

def Draw(screen):
    # Fill Screen With White
    screen.fill((255, 255, 255))

    # Draw Gameboard and simple information
    DrawText(screen, AddList(VAR.UI.boardPosition, [0, -50]), VAR.gamestateText[VAR.game.gamestate])
    DrawBoard(screen, VAR.game, VAR.UI.boardPosition, VAR.UI.boardCellSize)
    _t1, _t2, _t3 = VAR.game.GetPiecesCount()
    DrawText(screen, AddList(VAR.UI.boardPosition, [VAR.UI.boardCellSize*8, VAR.UI.boardCellSize*8+10]), "B:{}, W:{}, E:{}".format(_t1, _t2, _t3), font="Small", align="rt")
    # Draw History (Below Gameboard)
    DrawHistory(screen, VAR.gameHistory, AddList(VAR.UI.boardPosition, [0, VAR.UI.boardCellSize*8+20]))

    # Finally, Flip
    pygame.display.flip()

def EventMouseDown(mouse):
    pass

def EventMouseUp():
    pass

def Main():
    pygame.init()
    
    
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
        Draw(screen)

if __name__=="__main__":
    Main()