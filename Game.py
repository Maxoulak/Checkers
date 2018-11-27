from PyQt5.QtCore import QPoint

from ClickablePiece import ClickablePiece
from Possibility import Possibility
from Square import Square

class Game:
    NB_PLATE_SQUARES = 8
    FORCE_HUNGRY_MODE = True

    def __init__(self, plate):
        self.plate = plate
        self.turnJ1 = True
        self.clickablePieces = []
        self.nbPiecesJ1 = 12
        self.nbPiecesJ2 = 12
        self.atLeastOneHungryMode = False
        self.setClickablePieces()

    def toggleTurn(self):
        self.atLeastOneHungryMode = False
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
        self.clickablePieces = self.removeAllNoHungryMode(self.clickablePieces)

    # Remove all clickablepiece which aren't hungry mode (if at leat one is possible)
    def removeAllNoHungryMode(self, clickablePieces):
        if not self.FORCE_HUNGRY_MODE:
            return self.clickablePieces
        finalClickablePieces = []
        if self.atLeastOneHungryMode:
            print("hungry")
            for clickablePiece in clickablePieces:
                isHungry = False
                for possibility in clickablePiece.getPossibilities():
                    if possibility.getNbPiecesEat() > 0:
                        isHungry = True
                        break
                if isHungry:
                    finalClickablePieces.append(clickablePiece)
            return finalClickablePieces
        return clickablePieces


    def getClickablePieces(self):
        return self.clickablePieces

    def getPossibility(self, point):
        for clickablePiece in self.clickablePieces:
            pos = clickablePiece.getPos()
            if pos.x() == point.x() and pos.y() == point.y():
                return clickablePiece.getPossibilities()
        return []

    def searchPossibility(self, piece, nbPiecesEat, posPiecesEat, pieceMoves):
        x = piece.x()
        y = piece.y()
        possibilities = []
        i = 0
        # points : [cell1, cell2, cell1 + 1, cell2 + 1]
        # J2 Init
        points = [QPoint(x - 1, y - 1), QPoint(x - 1, y + 1), QPoint(x - 2, y - 2), QPoint(x - 2, y + 2)]
        # J1 Init
        if self.turnJ1:
            points = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1), QPoint(x + 2, y - 2), QPoint(x + 2, y + 2)]
        while i < 2:
            # Check simple move
            if self.isValidSquare(points[i]) and self.isEmptySquare(points[i]) and nbPiecesEat == 0:
                possibilities.append(Possibility(points[i], 0, QPoint(-1, -1), []))
            # Check hungry move
            elif self.isValidSquare(points[i]) and self.canBeEat(points[i]):
                if self.isValidSquare(points[i + 2]) and self.isEmptySquare(points[i + 2]):
                    nbPiecesEat += 1
                    posPiecesEat.append(points[i])
                    pieceMoves.append(points[i + 2])
                    tmpPossibilities = self.searchPossibility(points[i + 2], nbPiecesEat, posPiecesEat, pieceMoves)
                    if len(tmpPossibilities) == 0:
                        possibilities.append(Possibility(points[i + 2], nbPiecesEat, posPiecesEat, pieceMoves))
                    possibilities += tmpPossibilities
            i += 1
        return self.removeAllNoHungryModeForPossibilites(possibilities)

    # Remove all possibilites which aren't hungry mode (if at leat one is possible)
    def removeAllNoHungryModeForPossibilites(self, possibilities):
        if not self.FORCE_HUNGRY_MODE:
            return possibilities
        atLeastOneHungryMode = False
        for possibility in possibilities:
            if possibility.nbPiecesEat > 0:
                self.atLeastOneHungryMode = True
                atLeastOneHungryMode = True
                break
        if atLeastOneHungryMode:
            finalPossibilities = []
            for possibility in possibilities:
                if possibility.nbPiecesEat > 0:
                    finalPossibilities.append(possibility)
            return finalPossibilities
        return possibilities

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
