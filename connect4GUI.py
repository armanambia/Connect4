'''
Connect 4 Graphical User Interface
- pygame used to create GUI
- methodology based on Sudoku GUI by TechwithTim on youtube
'''

import pygame
import time
import random


pygame.font.init()

BOARD = [[0 for x in range(7)] for x in range(6)]
COUNT = 0
RED_WIN = False
BLACK_WIN = False

class GameBoard:

    def __init__(self, win, row, col, width, height):
        self.rows = row
        self.cols = col
        self.width = width
        self.height = height
        self.win = win
        self.spaces = [[Space('none', i, j, width, height, win) for j in range(col)] for i in range(row)]
    def updateModel(self):
        self.spaces = [[Space('none', i, j, self.width, self.height, self.win) for j in range(self.cols)] for i in range(self.rows)]
        for r in range (6):
            for c in range(7):
                if BOARD[r][c] == 1:
                    self.spaces[r][c].color = 'red'
                elif BOARD[r][c] == 2:
                    self.spaces[r][c].color = 'black'
    def checkRow(self):
        global RED_WIN, BLACK_WIN
        for row in BOARD:
            for x in range(4):
                if row[x] != 0 and len(set(row[x:x + 4])) == 1:
                    if row[x] == 2:
                        BLACK_WIN = True
                    else:
                        RED_WIN = True
                    return True
        return False
    def checkCol(self):
        global RED_WIN, BLACK_WIN
        for c in range(7):
            col = [BOARD[r][c] for r in range(6)]
            for r in range(3):
                if col[r] != 0 and len(set(col[r:r + 4])) == 1:
                    if col[r] == 2:
                        BLACK_WIN = True
                    else:
                        RED_WIN = True
                    return True
        return False

    # helper to check diagonals in forward direction
    def forwardHelper(self, start):
        r = 3 if start else 4
        for x in range(r):
            row = x if start else 0
            col = 0 if start else x
            count_red = 0
            count_black = 0
            while row < 6 and col < 7:
                if BOARD[row][col] == 1:
                    count_red += 1
                elif BOARD[row][col] == 2:
                    count_black += 1
                row += 1
                col += 1
            if self.countHelper(count_red, count_black):
                return True
        return False

    # helper to check diagonals in backward direction
    def backwardhelper(self, val):
        start = 6 if val else 2
        stop = 2 if val else -1
        for x in range(start, stop, -1):
            row = 0 if val else x
            col = x if val else 6
            count_red = 0
            count_black = 0
            while row < 6 and col > -1:
                if BOARD[row][col] == 1:
                    count_red += 1
                elif BOARD[row][col] == 2:
                    count_black += 1
                row += 1
                col -= 1
            if self.countHelper(count_red, count_black):
                return True
        return False

    # used to count the consecutive red or black pieces in a diagonal
    def countHelper(self, r, b):
        global RED_WIN, BLACK_WIN
        if r >= 4:
            RED_WIN = True
            return True
        elif b >= 4:
            BLACK_WIN = True
            return True

    # checks for four in a row in diagonals using helper functions
    def checkDiag(self):
        # forward diagonals along top left column
        global RED_WIN, BLACK_WIN
        if self.forwardHelper(True):
            return True
        # forward diagonals along top left row
        elif self.forwardHelper(False):
            return True
        # backward diagonals along top right row
        elif self.backwardhelper(False):
            return True
        # backward diagonals along top right column
        elif self.backwardhelper(True):
            return True
        return False

    def checkWin(self):
        return self.checkDiag() or self.checkCol() or self.checkRow()

    # signals game over due to tie or victory
    def endGame(self):
        if RED_WIN:
            return 'Red Wins'
        elif BLACK_WIN:
            return'Black Wins'
        else:
            return 'Tie Game'

    # clear board
    def clear(self):
        global BOARD
        BOARD = [[0 for x in range(7)] for x in range(6)]
        self.updateModel()

    def draw(self):
        space = self.width / 7
        for i in range(self.rows + 1):
            pygame.draw.line(self.win, (0, 0, 0), (0, i * space + 90), (self.width, i * space + 90), 3)
        for i in range(self.cols + 1):
            pygame.draw.line(self.win, (0, 0, 0), (i * space, 90), (i * space, self.height + 90), 3)
        for row in self.spaces:
            for elem in row:
                elem.draw()

class selector:
    def __init__(self, color, loc = 0):
        self.color = color
        self.locations = [30 +60*x for x in range(7)]
        self.loc = loc
        self.setLoc(0)
        self.y = 60

    def setLoc(self, loc):
        self.x = self.locations[self.loc]
    def moveLoc(self, dir):
        if dir:
            if self.loc < 6:
                self.loc += 1
                self.setLoc(self.loc)
        else:
            if self.loc > 0:
                self.loc -= 1
                self.setLoc(self.loc)
    def draw(self, win):
        font = pygame.font.SysFont('monospace', 25, True)
        if self.color == 'red':
            text = font.render('↓', True, (255, 0, 0))
        elif self.color == 'black':
            text = font.render('↓', True, (0, 0, 0))
        win.blit(text, (self.x, self.y))

class Space:
    def __init__(self, color, row, col, width, height, win):
        self.color = color
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.win = win
        self.placing = False

    def draw(self):
        gap = self.width / 7
        x = self.col * gap
        y = self.row * gap + 90
        if self.color == 'black':
            pygame.draw.circle(self.win, (0, 0, 0), (int(x + gap / 2), int(y + gap / 2)), 20)
        elif self.color == 'red':
            pygame.draw.circle(self.win, (255, 0, 0), (int(x + gap / 2), int(y + gap / 2)), 20)

class piece:

    def __init__(self, color, loc):
        self.color = color
        self.loc = loc
    def place(self):
        global board
        spot = 0;
        if BOARD[spot][self.loc ] != 0:
            pass
        else:
            index = len(BOARD)-1
            while spot != len(BOARD):
                if BOARD[spot][self.loc ] == 0:
                    spot += 1
                else:
                    index = spot - 1
                    spot = len(BOARD)

            if self.color == 'red':
                BOARD[index][self.loc] = 1
            elif self.color == 'black':
                BOARD[index][self.loc] = 2

    def draw(self):
        pass
    # causes the piece to move to the lowest available position in selected column

def redraw_window(win, board, selector, turn):
    win.fill((255, 255, 255))
    board.draw()
    selector.draw(win)
    createText(turn, win)
    pygame.display.update()


def createText(value, win):
    font = pygame.font.SysFont('monospace', 30)
    text = font.render(value, 3, (0, 0, 0))
    win.blit(text, (210 - text.get_width() / 2, 45 - text.get_height() / 2))
    pygame.display.update()

def main():
    global RED_WIN, BLACK_WIN
    win = pygame.display.set_mode((420, 450))
    win.fill((255, 255, 255))
    board = GameBoard(win, 6, 7, 420, 360)
    pygame.display.set_caption("Connect 4")
    createText('Welcome to Connect 4!', win)
    board.draw()
    pygame.display.update()
    pygame.time.delay(2000)
    run = True
    cur = random.randint(0, 1)
    finishedTurn = False
    if cur == 0:
        color = 'red'
        cur = 1
    else:
        color = 'black'
        cur = 0
    position = selector(color)
    running = True
    while run:
        pygame.time.delay(100)
        if finishedTurn:
            if cur == 0:
                color = 'red'
                cur = 1
            else:
                color = 'black'
                cur = 0
            position = selector(color, position.loc)
            finishedTurn = False
        if running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        position.moveLoc(False)
                    elif event.key == pygame.K_RIGHT:
                        position.moveLoc(True)
                    elif event.key == pygame.K_RETURN:
                        current = piece(color, position.loc)
                        current.place()
                        board.updateModel()
                        finishedTurn = True
            if board.checkWin():
                running = False
                redraw_window(win, board, position, board.endGame())
                pygame.time.delay(5000)
            elif cur == 1:
                redraw_window(win, board, position, "Red's Turn")
            else:
                redraw_window(win, board, position, "Black's Turn")
        else:
            redraw_window(win, board, position, 'Click to Play Again')
            RED_WIN = False
            BLACK_WIN = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.clear()
                    running = True
                    continue


main()
