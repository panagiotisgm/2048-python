import random


SIZE = 4          # 4x4
WIN_VALUE = 2048  # value to win,constant


def reset_board():
    # empty 4x4 board
    board = []
    for i in range(SIZE):
        row = [None] * SIZE
        board.append(row)

    #  (row, col) position on the board
    cells = []
    for r in range(SIZE):
        for c in range(SIZE):
            cells.append((r, c))

    
    count = random.randint(2, 4)
    for r, c in random.sample(cells, count):  
        board[r][c] = 2

    return board


def merge(row):
    # remove None
    values = [x for x in row if x is not None]

    output = []
    points = 0

    
    while values:
        if len(values) >= 2 and values[0] == values[1]:
            merged = values[0] * 2
            output.append(merged)
            points += merged
            values = values[2:]  
        else:
            output.append(values[0])
            values = values[1:]

    # add None so the row stays SIZE long
    while len(output) < SIZE:
        output.append(None)

    return output, points


def move_left(board):

    board_after = []
    total_score = 0

    for row in board:
        row, points = merge(row)
        board_after.append(row)
        total_score += points

    return board_after, total_score

def move_right(board):

    board_after = []
    total_score = 0

    for row in board:
        row, points = merge(row[::-1])   # reverse row
        board_after.append(row[::-1])    
        total_score += points

    return board_after, total_score

def rows_to_columns(board):
    # allows us to use the same function merge by flipping the board
    result = []

    for c in range(SIZE):
        new_row = []
        for r in range(SIZE):
            new_row.append(board[r][c])  
        result.append(new_row)

    return result

def move_up(board):

    flipped, total = move_left(rows_to_columns(board))

    return flipped, total

def move_down(board):

    flipped, total = move_right(rows_to_columns(board))

    return rows_to_columns(flipped), total


def game_status(board):
    # check if we have reached the winning value
    for row in board:
        if WIN_VALUE in row:
            return "won"

    for row in board:
        if None in row:
            return "still playing"

    # check if anything can be merged horizontally
    for row in board:
        for c in range(SIZE - 1):
            if row[c] == row[c + 1]:
                return "still playing"

    # check if anything can be merged vertically
    for r in range(SIZE - 1):
        for c in range(SIZE):
            if board[r][c] == board[r + 1][c]:
                return "still playing"

    return "lost"

def generate_value(board):
    # find all empty cells on the board
    empties = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] is None]

    if not empties:
        return board 

    # more common to have 2 instead of 4
    r, c = random.choice(empties)
    board[r][c] = 2 if random.random() < 0.9 else 4

    return board


# map of direction strings to their functions
MOVES = {
    "left":  move_left,
    "right": move_right,
    "up":    move_up,
    "down":  move_down,
}

def play(board, direction):
    # validate the direction
    if direction not in MOVES:
        raise ValueError(f"not a valid direction: {direction}")

    # snapshot of the board before the move
    before = [row[:] for row in board]

    # apply the move
    after, points = MOVES[direction](before)

    # check if anything actually changed
    moved = after != before

    # only gnerate a new value in a tuple if the board changed
    if moved:
        generate_value(after)

    return after, points, moved