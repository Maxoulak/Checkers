from PyQt5.QtCore import QPoint, QTime, QTimer
from PyQt5.QtWidgets import QMessageBox

from AI.Ai import AiPlayer
from ClickablePiece import ClickablePiece
from Possibility import Possibility
from Square import Square

class Game:
    NB_PLATE_SQUARES = 8
    NB_PIECE_PER_PLAYER = 12

    def __init__(self, plate, container):
        self.Ai = True
        self.container = container
        self.initGameVariables(plate)

    def initGameVariables(self, plate):
        self.ai = AiPlayer(self)
        self.setPlate(plate)
        self.turnJ1 = True
        self.clickablePieces = []
        self.nbPiecesJ1 = 12
        self.nbPiecesJ2 = 12
        self.timerJ1 = 0
        self.timerJ2 = 0
        self.gameRunning = False
        self.setClickablePieces()

    def restartGame(self, plate):
        self.initGameVariables(plate)

    def toggleTurn(self):
        self.turnJ1 = False if self.turnJ1 else True
        self.setClickablePieces()
        self.container.updateUI()
        if self.isAi() and not self.isTurnJ1():
            self.ai.play()
            self.toggleTurn()

    def launchGame(self):
        self.gameRunning = True
        self.incTimer()

    def isGameRunning(self):
        return self.gameRunning

    def stopGame(self):
        self.gameRunning = False

    def incTimer(self):
        if not self.gameRunning:
            return
        if self.turnJ1:
            self.timerJ1 += 1
        else:
            self.timerJ2 += 1
        self.container.updateTimerUI()
        QTimer.singleShot(1000, self.incTimer)

    def getTimeMinJ1(self):
        return self.timerJ1 / 60

    def getTimeSecJ1(self):
        return self.timerJ1 % 60

    def getTimeMinJ2(self):
        return self.timerJ2 / 60

    def getTimeSecJ2(self):
        return self.timerJ2 % 60

    def removePieces(self, nbToRemove):
        if self.turnJ1:
            self.nbPiecesJ2 -= nbToRemove
        else:
            self.nbPiecesJ1 -= nbToRemove

    def getNbPiecesPlayer1(self):
        return self.nbPiecesJ1

    def getNbPiecesPlayer2(self):
        return self.nbPiecesJ2

    def isTurnJ1(self):
        return self.turnJ1

    def isAi(self):
        return self.Ai

    def setPlate(self, plate):
        self.plate = plate

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

    def getClickablePieces(self):
        return self.clickablePieces

    def getPossibility(self, point):
        for clickablePiece in self.clickablePieces:
            pos = clickablePiece.getPos()
            if pos.x() == point.x() and pos.y() == point.y():
                return clickablePiece.getPossibilities()
        return []

    def searchPossibility(self, piece):
        possibilities = []
        i = 0
        isQueen = self.plate[piece.y()][piece.x()]["queen"]
        possibleMoves = self.getPotentialMovesForPlayer(piece, isQueen)
        inc = int(len(possibleMoves) / 2)
        while i < inc:
            possibilities += self.checkSimpleMove(possibleMoves[i])
            i += 1
        possibilities += self.checkHungryMove(piece, Possibility(QPoint(-1, -1), 0, [], []), isQueen)
        return possibilities

    def checkSimpleMove(self, move):
        if self.isValidSquare(move) and self.isEmptySquare(move):
            possibility = Possibility(move, 0, [], [move])
            if self.checkGonnaBeQueen(move):
                possibility.gonnaBeQueen()
            return [possibility]
        return []

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
                                                     list(possibility.getPosPiecesEat()), list(possibility.getPieceMoves()))
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

    def eatPiece(self, pieceEat, plate):
        plate[pieceEat.y()][pieceEat.x()]["piece"] = Square.EMPTY
        plate[pieceEat.y()][pieceEat.x()]["queen"] = False
        plate[pieceEat.y()][pieceEat.x()]["player"] = 0

    def addPiece(self, pos, piece, queen, player, plate):
        plate[pos.y()][pos.x()]["piece"] = piece
        plate[pos.y()][pos.x()]["queen"] = queen
        plate[pos.y()][pos.x()]["player"] = player

    def movePiece(self, src, dest, plate, becomeQueen):
        plate[dest.y()][dest.x()]["piece"] = plate[src.y()][src.x()]["piece"]
        plate[dest.y()][dest.x()]["player"] = plate[src.y()][src.x()]["player"]
        plate[dest.y()][dest.x()]["queen"] = plate[src.y()][src.x()]["queen"]
        plate[src.y()][src.x()]["piece"] = Square.EMPTY
        plate[src.y()][src.x()]["player"] = 0
        plate[src.y()][src.x()]["queen"] = False
        if becomeQueen:
            self.checkQueen(dest, plate)

    def checkQueen(self, position, plate):
        if self.checkGonnaBeQueen(position):
            plate[position.y()][position.x()]["queen"] = True

    def checkGonnaBeQueen(self, position):
        requiredX = 0 if self.isTurnJ1() else self.NB_PLATE_SQUARES - 1
        if position.x() == requiredX:
            return True
        return False

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

    def canBeEat(self, point):
        player = 1 if self.isTurnJ1() else 2
        if not self.isEmptySquare(point):
            if self.plate[point.y()][point.x()]["player"] != player:
                return True
        return False

    def isValidSquare(self, point):
        if 0 <= point.x() < Game.NB_PLATE_SQUARES and 0 <= point.y() < Game.NB_PLATE_SQUARES:
            return True
        return False

    def isEmptySquare(self, point):
        if self.plate[point.y()][point.x()]["piece"] == Square.EMPTY:
            return True
        return False

    def getPointInPossibilities(self, possibilities, pointToSearch):
        for possibility in possibilities:
            if possibility.getPos().x() == pointToSearch.x() and possibility.getPos().y() == pointToSearch.y():
                return possibility
        return None
