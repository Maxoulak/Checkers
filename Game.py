from PyQt5.QtCore import QPoint

from Square import Square

class Game:
    NB_PLATE_SQUARES = 8

    def __init__(self, plate):
        self.plate = plate
        self.turnJ1 = True
        self.nbPiecesJ1 = 12
        self.nbPiecesJ2 = 12

    def toggleTurn(self):
        self.turnJ1 = False if self.turnJ1 else True

    def removePieces(self, nbToRemove):
        if self.turnJ1:
            self.nbPiecesJ2 -= nbToRemove
        else:
            self.nbPiecesJ1 -= nbToRemove

    def isTurnJ1(self):
        return self.turnJ1

    def setPlate(self, plate):
        self.plate = plate

    def searchPossibility(self, piece):
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
            if self.isValidSquare(points[i]) and self.isEmptySquare(points[i]):
                possibilities.append(points[i])
            # Check hungry move
            elif self.isValidSquare(points[i]) and not self.isEmptySquare(points[i]):
                if self.isValidSquare(points[i + 2]) and self.isEmptySquare(points[i + 2]):
                    possibilities.append(points[i + 2])
            i += 1
        return possibilities

    def isValidSquare(self, point):
        if 0 <= point.x() < Game.NB_PLATE_SQUARES and 0 <= point.y() < Game.NB_PLATE_SQUARES:
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
