from tkinter import *
import chess
import chess.engine
from PIL import Image

window = Tk()  # This thing is the window.
board = chess.Board()  # The chess board on which you'll be playing.
engine = chess.engine.SimpleEngine.popen_uci(
    'stockfish-10-win/Windows/stockfish_10_x64.exe')  # The engine you're gonna lose to.
ai = FALSE  # Boolean to decide if we're playing against the AI. DO NOT TOUCH AS IT CURRENTLY BREAKS THE CODE
moveCounter = 0  # Counter for if we're gonna be playing human versus human
window.title("Chess GUI")  # Setting a nice title.
window.geometry('680x700')  # TODO: BRAM VIND MOOIE RESOLUTIE


# Makeshift Switch function that converts the letters into pictures.
# @arg: The letter we're gonna convert.
def switch(arg):  # TODO: BRAM ZORG DAT DIT WERKT
    switch = {
        "p": Image.open("SchaakstukkenPNGs/PionBlauw.png"),
        "P": Image.open("SchaakstukkenPNGs/PionRood.png"),
        "r": Image.open("SchaakstukkenPNGs/TorenBlauw.png"),
        "R": Image.open("SchaakstukkenPNGs/TorenRood.png"),
        "n": Image.open("SchaakstukkenPNGs/PaardBlauw.png"),
        "N": Image.open("SchaakstukkenPNGs/PaardRood.png"),
        "b": Image.open("SchaakstukkenPNGs/LoperBlauw.png"),
        "B": Image.open("SchaakstukkenPNGs/LoperRood.png"),
        "q": Image.open("SchaakstukkenPNGs/KoniningBlauw.png"),
        "Q": Image.open("SchaakstukkenPNGs/KoniningRood.png"),
        "k": Image.open("SchaakstukkenPNGs/KoningBlauw.png"),
        "K": Image.open("SchaakstukkenPNGs/KoningRood.png")
    }
    file = switch.get(arg, ".")
    return file


# Function to send the move to the board, input it into the AI if active, and update the GUI
def sendMove(moveToSend):
    global moveCounter
    move = inputMove.get()
    board.push_san(move)
    # Are we playing against the AI? Default is TRUE for now.
    if ai == TRUE:
        result = engine.play(board, chess.engine.Limit(time=0.1))
        stockfishMove = result.move
        board.push(stockfishMove)
    # Update the board after the move was set.
    generateBoard()
    #    print(board)
    # Are we playing against AI?
    if ai == TRUE:
        movesToPrint = move + "-" + str(stockfishMove) + "\n"  # TODO: BRAM ZET DIT MOOI NEER
    # No, we're not.
    #TODO:BRAM check if u need this
    else:
        moveCounter += 1
        # Is player 2 playing?
        if moveCounter % 2 != 0:
            movesToPrint = move
        else:
            movesToPrint = "-" + move + "\n"
    print(movesToPrint)
    print(moveCounter)


def generateBoard():
    counterY = 0
    counterX = 0
    posArray = list(str(board))
    while ' ' in posArray: posArray.remove(' ')
    for x in posArray:
        if x != '\n':
            #            piecePic = switch(x)
            if x != ".":  # image = piecePic
                piece = Button(window, text=x, height=5, width=10).grid(column=counterX, row=counterY)
            else:
                piece = Button(window, text=x, height=5, width=10).grid(column=counterX, row=counterY)
            counterX = counterX + 1
        else:
            counterY = counterY + 1
            counterX = 0


inputMove = Entry(window)
inputMove.grid(column=0, row=9)
submit = Button(window, text="send move")
submit.bind("<Button-1>", sendMove)
submit.grid(column=1, row=9)
generateBoard()
window.mainloop()
