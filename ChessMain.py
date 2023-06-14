"""
file for user input
"""
import pygame as p

import ChessEngine
from ChessEngine import GameState

WIDTH = HEIGHT = 512  # 400 is another option
DIMENSIONS = 8  # dimension of  a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}

"""    
 Initialize a global dictionary of images. This will be called exactly once in main
"""


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
The main  driver for our code. This will handle user input and update the graphics
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    # print(gs.board)
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made

    loadImages()

    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: row, col)
    playerClicks = []  # keep track of the player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:  # after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                    sqSelected = ()  # reset user clicks
                    playerClicks = []

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when z is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all the graphics withing a current game states 
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draw Squares on the board
    # add in pieces highlighting or move suggestions
    drawPieces(screen, gs.board)  # to draw pieces on top of those squares


'''
Draw the squares on  the board. The top left square is always  light
'''


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]

    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''


def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]

            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
