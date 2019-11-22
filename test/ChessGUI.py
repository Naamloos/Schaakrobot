from tkinter import *
import chess
import chess.engine
from tkinter import *

#installeer het CHEQ.TT.TTF bestand voor het custom font


window = Tk()
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci('stockfish-10-win/Windows/stockfish_10_x64.exe')  #Engine

ai = TRUE  # Boolean to decide if we're playing against the AI. DO NOT TOUCH AS IT CURRENTLY BREAKS THE CODE
moveCounter = 0  # Counter for if we're gonna be playing human versus human
window.title("Chess GUI")  # Setting a nice title.
window.geometry('1100x700')
squares = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8",
           "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8",
           "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8",
           "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8",
           "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8",
           "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8",
           "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8",
           "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]

chess_font = "Chess-7 18"
tile_height = 2
tile_width = 3

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


# outputLabel = Label(window, text="", height=2, width=4).grid(column=12, row=12)

# Function to send the move to the board, input it into the AI if active, and update the GUI
def sendMove(moveToSend):
    global moveCounter
    userMoveValid = TRUE

    # move = inputMove.get()
    move = moveToSend
    try:
        board.push_san(move)
    except:
        print("dat mag niet boef")
        userMoveValid = FALSE

    if userMoveValid:
        # Are we playing against the AI? Default is TRUE for now.
        if ai == TRUE:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            stockfishMove = result.move
            board.push(stockfishMove)

        # Update the board after the move was set.
        generateBoard()
        # change_pos(POS, selectedPiece, 'lightgrey')

        # Are we playing against AI?
        if ai == TRUE:
            movesToPrint = move + "-" + str(stockfishMove) + "\n"  # TODO: BRAM ZET DIT MOOI NEER
        # No, we're not.
        # TODO:BRAM check if u need this
        else:
            moveCounter += 1
            # Is player 2 playing?
            if moveCounter % 2 != 0:
                movesToPrint = move
            else:
                movesToPrint = "-" + move + "\n"
            print(moveCounter)
        print(movesToPrint)


click = lambda n, m: lambda: callback(n, m)

selectedPiece = "0"
piece_start_pos = ""


def callback(POS, PIECE):
    global selectedPiece
    global piece_start_pos
    if selectedPiece == "0":
        if PIECE != "." and PIECE.isupper():
            selectedPiece = PIECE
            piece_start_pos = POS

            # maakt de knop rood
            change_pos(POS, PIECE, "pink")
            for move in squares:
                if POS!= move:
                    gluePos = POS + move
                    compare = chess.Move.from_uci(gluePos)
                    if compare in board.legal_moves:
                        print(gluePos) #TODO: Colour the squares
                        change_color(gluePos)
            Label(window, text=PIECE, height=2, width=4).grid(column=12, row=12)
    else:
        moved_piece = selectedPiece
        # als het een pion is moet er geen P voor
        if moved_piece == 'P' or moved_piece == 'p':
            san_move = piece_start_pos + POS
        else:
            san_move = moved_piece + POS

        change_pos(POS, PIECE, "white")
        change_pos(piece_start_pos, selectedPiece, 'white')
        for move in squares:
            if piece_start_pos != move:
                gluePos = piece_start_pos + move
                compare = chess.Move.from_uci(gluePos)
                if compare in board.legal_moves:
                    print(gluePos)  # TODO: Colour the squares
                    change_color_white(gluePos)

        sendMove(san_move)
        Label(window, text=san_move, height=2, width=4).grid(column=12, row=12)
        selectedPiece = "0"



def change_color_white(possiblePosition):
    column = letters.index(possiblePosition[2]) + 1
    row = 9 - int(possiblePosition[3])
    for i in window.grid_slaves(row, column):
        i.configure(background='white')

def change_color(possiblePosition):
    column = letters.index(possiblePosition[2]) + 1
    row = 9 - int(possiblePosition[3])
    for i in window.grid_slaves(row, column):
        if i.cget('text') == ".":
            i.configure(background='lightgreen')
        else:
            i.configure(background='yellow')

def change_pos(pos, piece, color):
    if piece.isupper():
        textcolor = "red"
    else:
        textcolor = "blue"
    Xval = letters.index(pos[0]) + 1 #bepaald de xpositie en zet deze om naar een rij
    Yval = 9 - int(pos[1])          #zet de ypositie om naar een kolom
    Button(window, text=piece, height=tile_height, width=tile_width, bg=color, font=chess_font,
           fg=textcolor, highlightthickness=0, bd=0, command=click(pos, piece)).grid(column=Xval, row=Yval)


def generateBoard():
    counterY = 1
    counterX = 1

    posArray = list(str(board))
    while ' ' in posArray: posArray.remove(' ')
    for x in posArray:
        Label(window, text=9 - counterY, height=2, width=4).grid(column=0, row=counterY)  # getallen aan de zijkant
        Label(window, text=letters[8 - counterY], height=2, width=4).grid(column=9 - counterY,
                                                                          row=0)  # getallen aan de zijkant

        if x != '\n':
            #            piecePic = switch(x)
            currentLetter = letters[counterX - 1]
            currentPos = currentLetter + str(9 - counterY)
            # currentText = x+currentPos;

            if x != ".":  # image = piecePic
                if x.isupper():
                    btn = Button(window, text=x, height=tile_height, width=tile_width, foreground="red",
                                 highlightthickness=0, bd=2, bg="white",
                                 font=chess_font, highlightbackground="black",
                                 command=click(currentPos, x)).grid(column=counterX, row=counterY)
                else:
                    btn = Button(window, text=x,  height=tile_height, width=tile_width, foreground="blue", highlightthickness=0, bd=2, bg="white",
                                 font=chess_font, highlightbackground="black", command=click(currentPos, x)).grid(column=counterX, row=counterY)
            else:
                #btn = Button(window, text=x, height=2, width=4, command=click(currentPos, x)).grid(column=counterX,row=counterY)

                btn = Button(window, text=x, height=tile_height, width=tile_width, highlightthickness=0, bd=2, highlightbackground="black",
                             bg="white", font=chess_font, foreground="white", command=click(currentPos, x)).grid(column=counterX, row=counterY)

            counterX = counterX + 1
        else:
            counterY = counterY + 1
            counterX = 1
    if board.is_game_over():
        Label(window, font="Helvetica 30 bold", width=4).grid(column=10, row=4)  # getallen aan de zijkant
        Label(window, text="GAME OVER", font="Helvetica 30 bold").grid(column=11, row=4)  # getallen aan de zijkant



# invoeren van een move via de entry

    #move = inputMove.get()

def type_move():
    sendMove
#invoeren van een move via de entry

# load = Image.open("SchaakstukkenPNGs/PionBlauw.png")
# render = ImageTk.PhotoImage(load)
# img = Label(self, image=render)
# img.image = render
# img.place(x=0, y=0)

# inputMove = Entry(window)
# inputMove.grid(column=10, row=10)
# submit = Button(window, text="send move")
# submit.bind("<Button-1>", sendMove)
# submit.grid(column=11, row=10)
generateBoard()
window.mainloop()
