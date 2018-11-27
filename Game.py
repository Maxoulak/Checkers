from PyQt5.QtCore import QPoint

from ClickablePiece import ClickablePiece
from Possibility import Possibility
from Square import Square

class Game:
    NB_PLATE_SQUARES = 8

    def __init__(self, plate):
        self.plate = plate
        self.turnJ1 = True
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
                    clickablePiece.setPossibilities(self.searchPossibility(QPoint(x, y), 0, [], []))
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

    def searchPossibility(self, piece, nbPiecesEat, posPiecesEat, pieceMoves):
        possibilities = []
        i = 0
        points = self.getPotentialMovesForPlayer(piece)
        inc = int(len(points) / 2)
        while i < inc:
            # Check simple move
            if self.isValidSquare(points[i]) and self.isEmptySquare(points[i]) and nbPiecesEat == 0:
                possibilities.append(Possibility(points[i], 0, QPoint(-1, -1), []))
            # Check hungry move
            elif self.isValidSquare(points[i]) and self.canBeEat(points[i]):
                if self.isValidSquare(points[i + inc]) and self.isEmptySquare(points[i + inc]):
                    nbPiecesEat += 1
                    posPiecesEat.append(points[i])
                    pieceMoves.append(points[i + inc])
                    possibilities.append(Possibility(points[i + inc], nbPiecesEat, posPiecesEat, pieceMoves))
                    possibilities += self.searchPossibility(points[i + inc], nbPiecesEat, posPiecesEat, pieceMoves)
            i += 1
        return possibilities

    def checkSimpleMove(self, piece, possibleMove):
        possibilities = []


    def getPotentialMovesForPlayer(self, piece):
        x = piece.x()
        y = piece.y()
        # points : [cell1, cell2, cell1 + 1, cell2 + 1]
        # or [cell1, cell2, cell3, cell4, cell1 + 1, cell2 + 1, cell3 + 1, cell4 + 1] if queen
        pointsJ1 = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1), QPoint(x + 2, y - 2), QPoint(x + 2, y + 2)]
        pointsJ2 = [QPoint(x - 1, y - 1), QPoint(x - 1, y + 1), QPoint(x - 2, y - 2), QPoint(x - 2, y + 2)]
        points = pointsJ1 if self.isTurnJ1() else pointsJ2
        if self.plate[y][x]["queen"]:
            points = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1), QPoint(x - 1, y - 1), QPoint(x - 1, y + 1),
                      QPoint(x + 2, y - 2), QPoint(x + 2, y + 2), QPoint(x - 2, y - 2), QPoint(x - 2, y + 2)]
        return points

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
