'''
Connect 4 Game in console
- Red represented by number 1 in matrix
- Black represented by number 2 in matrix
'''

# represents game board, empty 6 x 7 grid
BOARD = [[ 0 for x in range(7)] for x in range(6)]
# tracks the total number of moves in case of tie
COUNT = 0
# Booleans to check either win
RED_WIN = False
BLACK_WIN = False
# Defines a single piece, either black or red color, and the location of the piece
class piece:
    def __init__(self, color, loc):
        self.color = color
        self.loc = loc
    # causes the piece to move to the lowest available position in selected column
    def place(self):
        global BOARD, COUNT
        spot = 0;
        if BOARD[spot][self.loc ] != 0:
            return False
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
            COUNT += 1
            return True

# prints out entire game board
def printGrid():
    for row in BOARD:
        for elem in row:
            print(elem, end = ' ')
        print()

# checks for 4 in a row in a single row
def checkRow():
    global RED_WIN, BLACK_WIN
    for row in BOARD:
        for x in range(4):
            if row[x] != 0 and len(set(row[x:x+4])) == 1:
                if row[x] == 2:
                    BLACK_WIN = True
                else:
                    RED_WIN = True
                return True
    return False

# checks for 4 in a row in a single column
def checkCol():
    global RED_WIN, BLACK_WIN
    for c in range (7):
        col = [BOARD[r][c] for r in range(6)]
        for r in range(3):
            if col[r] != 0 and len(set(col[r:r+4])) == 1:
                if col[r] == 2:
                    BLACK_WIN = True
                else:
                    RED_WIN = True
                return True
    return False

# helper to check diagonals in forward direction
def forwardHelper(start):
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
        if countHelper(count_red, count_black):
            return True
    return False

# helper to check diagonals in backward direction
def backwardhelper(val):
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
        if countHelper(count_red, count_black):
            return True
    return False

# used to count the consecutive red or black pieces in a diagonal
def countHelper(r, b):
    global RED_WIN, BLACK_WIN
    if r >= 4:
        RED_WIN = True
        return True
    elif b >= 4:
        BLACK_WIN = True
        return True

# checks for four in a row in diagonals using helper functions
def checkDiag():
    # forward diagonals along top left column
    global RED_WIN, BLACK_WIN
    if forwardHelper(True):
        return True
    # forward diagonals along top left row
    elif forwardHelper(False):
        return True
    # backward diagonals along top right row
    elif backwardhelper(False):
        return True
    # backward diagonals along top right column
    elif backwardhelper(True):
        return True
    return False

# signals game over due to tie or victory
def endGame():
    if RED_WIN:
        print('Red Wins')
    elif BLACK_WIN:
        print('Black Wins')
    else:
        print('Tie Game')

run = True
print('Welcome to Connect Four')
cur = 0;

# main game loop
while run:
    col = -1
    while col < 0 or col > 6:
        col = int(input('Enter a column to place piece: '))
    if cur == 0:
        color = 'red'
        cur = 1
    else:
        color = 'black'
        cur = 0
    cur_piece = piece(color, col)
    while not cur_piece.place():
        col = int(input('Column is Full, Enter a different column: '))
        cur_piece = piece(color, col)
    printGrid()
    if checkCol() or checkRow() or checkDiag() or COUNT == 42:
        endGame()
        run = False

        


