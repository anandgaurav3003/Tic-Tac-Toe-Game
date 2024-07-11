from tkinter import *

# Initialize the root window
root = Tk()
root.geometry("330x550")
root.title("Tic Tac Toe")
root.resizable(0, 0)

# Create the frames
frame1 = Frame(root, bg="#FFCCBC")
frame1.pack()
titleLabel = Label(frame1, text="Tic Tac Toe", font=("Courier", 26, "bold"), bg="#FF5722", fg="white", width=16)
titleLabel.grid(row=0, column=0)

optionFrame = Frame(root, bg="#E64A19")
optionFrame.pack()

frame2 = Frame(root, bg="#FFCCBC")
frame2.pack()

# Initialize the board and other variables
board = {i: " " for i in range(1, 10)}
turn = "x"
game_end = False
mode = "singlePlayer"

def changeModeToSinglePlayer():
    global mode
    mode = "singlePlayer"
    singlePlayerButton["bg"] = "#FF7043"
    multiPlayerButton["bg"] = "#FFCCBC"

def changeModeToMultiplayer():
    global mode
    mode = "multiPlayer"
    multiPlayerButton["bg"] = "#FF7043"
    singlePlayerButton["bg"] = "#FFCCBC"

def updateBoard():
    for key in board.keys():
        buttons[key-1]["text"] = board[key]

def checkForWin(player):
    # Rows, columns, and diagonals
    win_conditions = [
        (1, 2, 3), (4, 5, 6), (7, 8, 9),
        (1, 4, 7), (2, 5, 8), (3, 6, 9),
        (1, 5, 9), (3, 5, 7)
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def checkForDraw():
    return all(board[i] != " " for i in board.keys())

def restartGame():
    global game_end, turn
    game_end = False
    turn = "x"
    for i in board.keys():
        board[i] = " "
    updateBoard()
    titleLabel.config(text="Tic Tac Toe")

def minimax(board, isMaximizing):
    if checkForWin("o"):
        return 1
    if checkForWin("x"):
        return -1
    if checkForDraw():
        return 0

    bestScore = -100 if isMaximizing else 100
    for key in board.keys():
        if board[key] == " ":
            board[key] = "o" if isMaximizing else "x"
            score = minimax(board, not isMaximizing)
            board[key] = " "
            if isMaximizing:
                bestScore = max(score, bestScore)
            else:
                bestScore = min(score, bestScore)
    return bestScore

def playComputer():
    bestScore = -100
    bestMove = 0
    for key in board.keys():
        if board[key] == " ":
            board[key] = "o"
            score = minimax(board, False)
            board[key] = " "
            if score > bestScore:
                bestScore = score
                bestMove = key
    board[bestMove] = "o"

def play(event):
    global turn, game_end
    if game_end:
        return

    button = event.widget
    clicked = int(button.grid_info()['row']) * 3 + int(button.grid_info()['column']) + 1

    if board[clicked] == " ":
        board[clicked] = turn
        updateBoard()
        if checkForWin(turn):
            titleLabel.config(text=f"{turn.upper()} wins the game")
            game_end = True
            return
        if checkForDraw():
            titleLabel.config(text="Game Draw")
            game_end = True
            return
        turn = "o" if turn == "x" else "x"
        if mode == "singlePlayer" and turn == "o":
            playComputer()
            updateBoard()
            if checkForWin("o"):
                titleLabel.config(text="O wins the game")
                game_end = True
            elif checkForDraw():
                titleLabel.config(text="Game Draw")
                game_end = True
            turn = "x"

# Change Mode options
singlePlayerButton = Button(optionFrame, text="SinglePlayer", width=13, height=1, font=("Courier", 15, "bold"), bg="#FFCCBC", relief=RAISED, borderwidth=5, command=changeModeToSinglePlayer)
singlePlayerButton.grid(row=0, column=0, sticky=NW)

multiPlayerButton = Button(optionFrame, text="Multiplayer", width=13, height=1, font=("Courier", 15, "bold"), bg="#FFCCBC", relief=RAISED, borderwidth=5, command=changeModeToMultiplayer)
multiPlayerButton.grid(row=0, column=1, sticky=NW)

# Tic Tac Toe Board
buttons = []
for i in range(3):
    for j in range(3):
        button = Button(frame2, text=" ", width=4, height=2, font=("Courier", 30, "bold"), bg="#FFAB91", relief=RAISED, borderwidth=5)
        button.grid(row=i, column=j)
        button.bind("<Button-1>", play)
        buttons.append(button)

restartButton = Button(frame2, text="Restart Game", width=19, height=1, font=("Courier", 20, "bold"), bg="#FF5722", relief=RAISED, borderwidth=5, command=restartGame)
restartButton.grid(row=4, column=0, columnspan=3)

root.mainloop()
