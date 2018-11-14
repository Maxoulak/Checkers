from PyQt5.QtCore import QPoint

from Square import Square

class Game:
    NB_PLATE_SQUARES = 8

    def __init__(self, plate):
        self.plate = plate
        self.turnJ1 = True

    def toggleTurn(self):
        self.turnJ1 = False if self.turnJ1 else True

    def isTurnJ1(self):
        return self.turnJ1

    def setPlate(self, plate):
        self.plate = plate

    def searchPossibility(self, pieceSelected):
        x = pieceSelected.x()
        y = pieceSelected.y()
        possibilities = []
        if self.turnJ1:
            points = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1)]
        else:
            points = [QPoint(x - 1, y - 1), QPoint(x - 1, y + 1)]
        for point in points:
            if self.isValidSquare(point):
                possibilities.append(point)
        return possibilities

    def isValidSquare(self, point):
        if 0 <= point.x() < Game.NB_PLATE_SQUARES and 0 <= point.y() < Game.NB_PLATE_SQUARES:
            if self.isEmptySquare(point):
                return True
        return False

    def isEmptySquare(self, point):
        if self.plate[point.y()][point.x()]["piece"] == Square.EMPTY:
            return True
        return False

    def isPointInArray(self, array, pointToSearch):
        for point in array:
            if point.x() == pointToSearch.x() and point.y() == pointToSearch.y():
                return True
        return False
