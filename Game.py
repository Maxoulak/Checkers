from PyQt5.QtCore import QPoint

from Square import Square

class Game:
    NB_PLATE_SQUARES = 8

    @staticmethod
    def searchPossibility(plate, pieceSelected):
        x = pieceSelected.x()
        y = pieceSelected.y()
        possibilities = []
        points = []
        if plate[y][x]["player"] == 1:
            points = [QPoint(x + 1, y - 1), QPoint(x + 1, y + 1)]
        else:
            points = [QPoint(x - 1, y - 1), QPoint(x - 1, y + 1)]
        for point in points:
            if Game.isValidSquare(plate, point):
                possibilities.append(point)
        return possibilities

    @staticmethod
    def isValidSquare(plate, point):
        if 0 <= point.x() < Game.NB_PLATE_SQUARES and 0 <= point.y() < Game.NB_PLATE_SQUARES:
            if Game.isEmptySquare(plate, point):
                return True
        return False

    @staticmethod
    def isEmptySquare(plate, point):
        if plate[point.y()][point.x()]["piece"] == Square.EMPTY:
            return True
        return False

    @staticmethod
    def isPointInArray(array, pointToSearch):
        for point in array:
            if point.x() == pointToSearch.x() and point.y() == pointToSearch.y():
                return True
        return False
