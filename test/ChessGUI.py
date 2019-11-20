from tkinter import *
import chess
import chess.engine
#from PIL import Image

window = Tk()  # This thing is the window.
board = chess.Board()  # The chess board on which you'll be playing.
engine = chess.engine.SimpleEngine.popen_uci(
    'stockfish-10-win/Windows/stockfish_10_x64.exe')  # The engine you're gonna lose to.
ai = TRUE  # Boolean to decide if we're playing against the AI. DO NOT TOUCH AS IT CURRENTLY BREAKS THE CODE
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

#outputLabel = Label(window, text="", height=2, width=4).grid(column=12, row=12)

# Function to send the move to the board, input it into the AI if active, and update the GUI
def sendMove(moveToSend):
    global moveCounter
    #move = inputMove.get()
    move = moveToSend
    try:
        board.push_san(move)
    except:
        print("dat mag niet boef")

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


first_pos = ''

def callback(POS):
    global first_pos

    if first_pos == '':
        first_pos = POS
        Label(window, text=POS, height=2, width=4).grid(column=12, row=12)
    else:
        old_pos = first_pos;
        sanMove  = old_pos + POS
        sendMove(sanMove)
        Label(window, text=sanMove, height=2, width=4).grid(column=12, row=12)
        first_pos = ''






def generateBoard():
    counterY = 1
    counterX = 1

    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]

    posArray = list(str(board))
    while ' ' in posArray: posArray.remove(' ')
    for x in posArray:
        Label(window, text=9-counterY, height=2, width=4).grid(column=0, row=counterY) #getallen aan de zijkant
        Label(window, text=letters[8-counterY], height=2, width=4).grid(column=9 - counterY, row=0)  # getallen aan de zijkant

        if x != '\n':
            #            piecePic = switch(x)
            currentLetter = letters[counterX-1]
            currentPos = currentLetter + str(9-counterY)
            currentText = x+currentPos;
            click = lambda n: lambda: callback(n)

            if x != ".":  # image = piecePic
                btn = Button(window, text=x, height=2, width=4, command=click(currentText)).grid(column=counterX, row=counterY)
            else:
                btn = Button(window, text=x, height=2, width=4, command=click(currentText)).grid(column=counterX, row=counterY)
            counterX = counterX + 1
        else:
            counterY = counterY + 1
            counterX = 1

#invoeren van een move via de entry
inputMove = Entry(window)
inputMove.grid(column=10, row=10)
submit = Button(window, text="send move")
submit.bind("<Button-1>", sendMove)
submit.grid(column=11, row=10)
generateBoard()
window.mainloop()
