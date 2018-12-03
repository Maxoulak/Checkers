from PyQt5.QtCore import QPoint

from ClickablePiece import ClickablePiece
from Possibility import Possibility
from Square import Square

class Game:
    NB_PLATE_SQUARES = 8

    def __init__(self, plate):
        self.plate = plate
        self.turnJ1 = True
        self.Ai = True
        self.clickablePieces = []
        self.nbPiecesJ1 = 12
        self.nbPiecesJ2 = 12
        self.setClickablePieces()

    def toggleTurn(self):
        self.turnJ1 = False if self.turnJ1 else True
        self.setClickablePieces()

    def removePieces(self, nbToRemove):
        if self.turnJ1:
            self.nbPiecesJ2 -= nbToRemove
        else:
            self.nbPiecesJ1 -= nbToRemove

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
                    clickablePiece = ClickablePiece(QPoint(x, y))
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

    def checkHungryMove(self, piece, possibility, isQueen):
        try:
            possibilities = []
            i = 0
            potentialMoves = self.getPotentialMovesForPlayer(piece, isQueen)
            inc = int(len(potentialMoves) / 2)
            while i < inc:
                tmpPossibility = Possibility(potentialMoves[i + inc], possibility.getNbPiecesEat(),
                                             list(possibility.getPosPiecesEat()), list(possibility.getPieceMoves()))
                if self.isValidSquare(potentialMoves[i]) and self.canBeEat(potentialMoves[i]):
                    if self.isValidSquare(potentialMoves[i + inc]) and self.isEmptySquare(potentialMoves[i + inc]):
                        tmpPossibility.addNbPiecesEat()
                        tmpPossibility.posPiecesEat.append(potentialMoves[i])
                        tmpPossibility.pieceMoves.append(potentialMoves[i + inc])
                        possibilities.append(tmpPossibility)
                        possibilities += self.checkHungryMove(potentialMoves[i + inc], tmpPossibility, isQueen)
                i += 1
        except Exception as e:
            print(e)
        return possibilities

    def checkSimpleMove(self, move):
        if self.isValidSquare(move) and self.isEmptySquare(move):
            return [Possibility(move, 0, [], [])]
        return []

    def getPotentialMovesForPlayer(self, piece, isQueen):
        x = piece.x()
        y = piece.y()
        # points : [cell1, cell2, cell1 + 1, cell2 + 1]
        # or [cell1, cell2, cell3, cell4, cell1 + 1, cell2 + 1, cell3 + 1, cell4 + 1] if queen
        potentialMovesJ1 = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1), QPoint(x + 2, y - 2), QPoint(x + 2, y + 2)]
        potentialMovesJ2 = [QPoint(x - 1, y - 1), QPoint(x - 1, y + 1), QPoint(x - 2, y - 2), QPoint(x - 2, y + 2)]
        potentialMoves = potentialMovesJ1 if self.isTurnJ1() else potentialMovesJ2
        if isQueen:
            potentialMoves = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1), QPoint(x - 1, y - 1), QPoint(x - 1, y + 1),
                              QPoint(x + 2, y - 2), QPoint(x + 2, y + 2), QPoint(x - 2, y - 2), QPoint(x - 2, y + 2)]
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
