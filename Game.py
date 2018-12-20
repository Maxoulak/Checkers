from PyQt5.QtCore import QPoint, QTime, QTimer
from PyQt5.QtWidgets import QMessageBox

from AI.Ai import AiPlayer
from ClickablePiece import ClickablePiece
from Possibility import Possibility
from Square import Square

# Game Class
#   Contains all information about the current game
class Game:
    NB_PLATE_SQUARES = 8
    NB_LINE_OCCUPED = 3
    NB_PIECE_PER_PLAYER = 12
    NB_MIN_PER_PLAYER = 5;
    NB_SEC_PER_PLAYER = 0;

    # Init Method
    #   Init Class variables
    def __init__(self, plate, container):
        self.Ai = False
        self.container = container
        self.initGameVariables(plate)

    # Init Game Variables
    #   Init all game's variables
    def initGameVariables(self, plate):
        self.setPlate(plate)
        self.ai = AiPlayer(self)
        self.turnJ1 = True
        self.clickablePieces = []
        self.nbPiecesJ1 = self.NB_PIECE_PER_PLAYER
        self.nbPiecesJ2 = self.NB_PIECE_PER_PLAYER
        self.timerJ1 = self.NB_MIN_PER_PLAYER * 60 + self.NB_SEC_PER_PLAYER
        self.timerJ2 = self.NB_MIN_PER_PLAYER * 60 + self.NB_SEC_PER_PLAYER
        self.gameRunning = False
        self.justWon = False
        self.setClickablePieces()

    # Restart Game
    #   Init back the game variables to restart the game
    def restartGame(self, plate):
        self.initGameVariables(plate)

    # Toggle Turn
    #   Toggle player (or AI) turn
    #   Search all player's (or AI's) possibilities
    def toggleTurn(self):
        self.turnJ1 = False if self.turnJ1 else True
        self.setClickablePieces()
        self.container.updateUI()
        if self.isAi() and not self.isTurnJ1():
            self.ai.play()

    # Launch Game
    #   Start the game and the timers
    def launchGame(self):
        self.gameRunning = True
        self.decTimer()

    # Has won
    #   Return true if someone just won, false otherwise
    def hasWon(self):
        return self.justWon;

    # Is Game Running
    #   Return true if a game is running, false otherwise
    def isGameRunning(self):
        return self.gameRunning

    # Stop Game
    #   Stop the current game
    def stopGame(self, won):
        self.gameRunning = False
        self.justWon = won

    # Dec Timer
    #   Decrement the player's (or AI's) timer
    #   Show a message on win
    def decTimer(self):
        if not self.gameRunning:
            return
        if self.turnJ1:
            self.timerJ1 -= 1
        else:
            self.timerJ2 -= 1
        self.container.updateTimerUI()
        if self.timerJ1 <= 0 or self.timerJ2 <= 0:
            player = "Black" if not self.turnJ1 else "White"
            if not self.Ai:
                QMessageBox.about(self.container, "Win !", "Player " + player + " won ! (out of time)")
            elif self.turnJ1:
                QMessageBox.about(self.container, "Loose !", "You loose ... AI won ! (out of time)")
            else:
                QMessageBox.about(self.container, "Win !", "You win against the AI ! (out of time)")
            self.stopGame(True)
        else:
            QTimer.singleShot(1000, self.decTimer)

    # Get Player 1 Timer Minutes
    #   Return the remaining minutes for player 1
    def getTimeMinJ1(self):
        return self.timerJ1 / 60

    # Get Player 1 Timer Seconds
    #   Return the remaining seconds for player 1
    def getTimeSecJ1(self):
        return self.timerJ1 % 60

    # Get Player 2 Timer Minute
    #   Return the remaining minutes for player 2
    def getTimeMinJ2(self):
        return self.timerJ2 / 60

    # Get Player 2 Timer Seconds
    #   Return the remaining seconds for player 2
    def getTimeSecJ2(self):
        return self.timerJ2 % 60

    # Remove Pieces
    #   Remove nbToRemove pieces to a player
    def removePieces(self, nbToRemove):
        if self.turnJ1:
            self.nbPiecesJ2 -= nbToRemove
        else:
            self.nbPiecesJ1 -= nbToRemove

    # Get Nb Pieces Player 1
    #   Return number of player 1's remaining pieces
    def getNbPiecesPlayer1(self):
        return self.nbPiecesJ1

    # Get Nb Pieces Player 2
    #   Return number of player 2's remaining pieces
    def getNbPiecesPlayer2(self):
        return self.nbPiecesJ2

    # Is Turn J1
    #   Return true if it's player 1's turn, false otherwise
    def isTurnJ1(self):
        return self.turnJ1

    # Is Turn AI
    #   Return true if it's AI's turn, false otherwise
    def isTurnAI(self):
        return True if not self.isTurnJ1() and self.isAi() else False

    # Is AI
    #   Return true if AI is enabled, false otherwise
    def isAi(self):
        return self.Ai

    # Set Plate
    #   Set the current game plate
    def setPlate(self, plate):
        self.plate = plate

    # Set Clickable Pieces
    #   Search all pieces which can be selected and move by the user (or AI)
    def setClickablePieces(self):
        self.clickablePieces = []
        player = 1
        if not self.isTurnJ1():
            player = 2
        for y in range(0, self.NB_PLATE_SQUARES):
            for x in range(0, self.NB_PLATE_SQUARES):
                square = self.plate[y][x]
                if square["player"] == player:
                    clickablePiece = ClickablePiece(QPoint(x, y), square["queen"])
                    clickablePiece.setPossibilities(self.searchPossibility(QPoint(x, y)))
                    if clickablePiece.getNbPossibilities() > 0:
                        self.clickablePieces.append(clickablePiece)

    # Get Clickable Pieces
    #   Return all current clickable pieces
    def getClickablePieces(self):
        return self.clickablePieces

    # Get Possibility
    #   Return possible moves for a piece
    def getPossibility(self, point):
        for clickablePiece in self.clickablePieces:
            pos = clickablePiece.getPos()
            if pos.x() == point.x() and pos.y() == point.y():
                return clickablePiece.getPossibilities()
        return []

    # Search Possibility
    #   Search all possible moves for a piece
    def searchPossibility(self, piece):
        possibilities = []
        i = 0
        isQueen = self.plate[piece.y()][piece.x()]["queen"]
        possibleMoves = self.getPotentialMovesForPlayer(piece, isQueen)
        inc = int(len(possibleMoves) / 2)
        while i < inc:
            possibilities += self.checkSimpleMove(possibleMoves[i], piece)
            i += 1
        possibilities += self.checkHungryMove(piece, Possibility(QPoint(-1, -1), 0, [], [], piece), isQueen)
        return possibilities

    # Check Simple Move
    #   Check if a piece can move
    def checkSimpleMove(self, move, piece):
        if self.isValidSquare(move) and self.isEmptySquare(move):
            possibility = Possibility(move, 0, [], [move], piece)
            if self.checkGonnaBeQueen(move):
                possibility.gonnaBeQueen()
            return [possibility]
        return []

    # Check Hungry Move
    #   Check if a piece can eat
    def checkHungryMove(self, piece, possibility, isQueen):
        possibilities = []
        i = 0
        potentialMoves = self.getPotentialMovesForPlayer(piece, isQueen)
        inc = int(len(potentialMoves) / 2)
        while i < inc:
            eatPos = potentialMoves[i]
            if self.isValidSquare(eatPos) and self.canBeEat(eatPos):
                if self.isValidSquare(potentialMoves[i + inc]) and self.isEmptySquare(potentialMoves[i + inc]):
                    currentPossibility = Possibility(potentialMoves[i + inc], possibility.getNbPiecesEat(),
                                                     list(possibility.getPosPiecesEat()), list(possibility.getPieceMoves()),
                                                     possibility.getSrc())
                    if self.checkGonnaBeQueen(potentialMoves[i + inc]):
                        currentPossibility.gonnaBeQueen()
                    currentPossibility.addNbPiecesEat()
                    currentPossibility.posPiecesEat.append(eatPos)
                    currentPossibility.pieceMoves.append(potentialMoves[i + inc])
                    eatPiece = self.plate[eatPos.y()][eatPos.x()]["piece"]
                    eatQueen = self.plate[eatPos.y()][eatPos.x()]["queen"]
                    eatPlayer = self.plate[eatPos.y()][eatPos.x()]["player"]
                    self.movePiece(piece, potentialMoves[i + inc], self.plate, False)
                    self.eatPiece(eatPos, self.plate)
                    possibilities.append(currentPossibility)
                    possibilities += self.checkHungryMove(potentialMoves[i + inc], currentPossibility, isQueen)
                    self.movePiece(potentialMoves[i + inc], piece, self.plate, False)
                    self.addPiece(eatPos, eatPiece, eatQueen, eatPlayer, self.plate)
            i += 1
        return possibilities

    # Eat Piece
    #   Remove a piece from the plate
    def eatPiece(self, pieceEat, plate):
        plate[pieceEat.y()][pieceEat.x()]["piece"] = Square.EMPTY
        plate[pieceEat.y()][pieceEat.x()]["queen"] = False
        plate[pieceEat.y()][pieceEat.x()]["player"] = 0

    # Add Piece
    #   Add a piece on the plate
    def addPiece(self, pos, piece, queen, player, plate):
        plate[pos.y()][pos.x()]["piece"] = piece
        plate[pos.y()][pos.x()]["queen"] = queen
        plate[pos.y()][pos.x()]["player"] = player

    # Move Piece
    #   Move a piece on the plate
    def movePiece(self, src, dest, plate, becomeQueen):
        plate[dest.y()][dest.x()]["piece"] = plate[src.y()][src.x()]["piece"]
        plate[dest.y()][dest.x()]["player"] = plate[src.y()][src.x()]["player"]
        plate[dest.y()][dest.x()]["queen"] = plate[src.y()][src.x()]["queen"]
        plate[src.y()][src.x()]["piece"] = Square.EMPTY
        plate[src.y()][src.x()]["player"] = 0
        plate[src.y()][src.x()]["queen"] = False
        if becomeQueen:
            self.checkQueen(dest, plate)

    # Check Queen
    #   Change the piece to queen if it has to be
    def checkQueen(self, position, plate):
        if self.checkGonnaBeQueen(position):
            plate[position.y()][position.x()]["queen"] = True

    # Check Gonna Be Queen
    #   Return true if the piece will become a queen, false otherwise
    def checkGonnaBeQueen(self, position):
        requiredX = 0 if self.isTurnJ1() else self.NB_PLATE_SQUARES - 1
        if position.x() == requiredX:
            return True
        return False

    # Get Potential Moves For Player
    #   Get the possible moves for a piece depending on the player and queen
    def getPotentialMovesForPlayer(self, piece, isQueen):
        x = piece.x()
        y = piece.y()
        potentialMovesFirstJ1 = [QPoint(x - 1, y - 1), QPoint(x - 1, y + 1)]
        potentialMovesSecondJ1 = [QPoint(x - 2, y - 2), QPoint(x - 2, y + 2)]
        potentialMovesFirstJ2 = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1)]
        potentialMovesSecondJ2 = [QPoint(x + 2, y - 2), QPoint(x + 2, y + 2)]
        potentialMoves = potentialMovesFirstJ1 + potentialMovesSecondJ1
        if not self.isTurnJ1():
            potentialMoves = potentialMovesFirstJ2 + potentialMovesSecondJ2
        if isQueen:
            potentialMoves = potentialMovesFirstJ1 + potentialMovesFirstJ2 + potentialMovesSecondJ1 + potentialMovesSecondJ2
        return potentialMoves

    # Can Be Eat
    #   Check if the piece can be eat
    def canBeEat(self, point):
        player = 1 if self.isTurnJ1() else 2
        if not self.isEmptySquare(point):
            if self.plate[point.y()][point.x()]["player"] != player:
                return True
        return False

    # Is Valid Square
    #   Return true if the cell is valid, false otherwise
    def isValidSquare(self, point):
        if 0 <= point.x() < Game.NB_PLATE_SQUARES and 0 <= point.y() < Game.NB_PLATE_SQUARES:
            return True
        return False

    # Is Empty Square
    #   Return true if the square is empty, false otherwise
    def isEmptySquare(self, point):
        if self.plate[point.y()][point.x()]["piece"] == Square.EMPTY:
            return True
        return False

    # Get Point In Possibilities
    #   Check if the cell is in the possibilities
    def getPointInPossibilities(self, possibilities, pointToSearch):
        for possibility in possibilities:
            if possibility.getPos().x() == pointToSearch.x() and possibility.getPos().y() == pointToSearch.y():
                return possibility
        return None
