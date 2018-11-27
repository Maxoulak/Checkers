import functools
import sys
import time

from PyQt5 import QtTest
from PyQt5.QtCore import QSize, Qt, QRectF, QPoint, QTimer
from PyQt5.QtGui import QImage, QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication

from Game import Game
from Square import Square

class CheckersPlateWidget(QWidget):
    MARGIN = 10

    def __init__(self, size):
        super().__init__()

        self.pieceSelected = QPoint(-1, -1)
        self.squarePossibilities = []
        self.size = min(size.width(), size.height())
        self.setFixedSize(self.size, self.size)
        self.plate = []
        self.initPlate()
        self.initSquareDimension()
        self.isAnimationRunning = False
        self.game = Game(self.plate)

        self.initUI()

    def initSquareDimension(self):
        self.squareDimension = self.size / Game.NB_PLATE_SQUARES

    def initUI(self):
        self.image = QImage(QSize(self.size, self.size), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawPlate()

    def initPlate(self):
        for y in range(0, Game.NB_PLATE_SQUARES):
            self.plate.append([])
            for x in range(0, Game.NB_PLATE_SQUARES):
                self.plate[y].append({})
                compare = 0 if y % 2 == 0 else 1
                if x % 2 == compare:
                    self.plate[y][x]["square"] = Square.WHITE
                    self.plate[y][x]["piece"] = Square.EMPTY
                    self.plate[y][x]["player"] = 0
                elif x < 3:
                    self.plate[y][x]["square"] = Square.BLACK
                    self.plate[y][x]["piece"] = Square.WHITE
                    self.plate[y][x]["player"] = 1
                elif x > 4:
                    self.plate[y][x]["square"] = Square.BLACK
                    self.plate[y][x]["piece"] = Square.BLACK
                    self.plate[y][x]["player"] = 2
                else:
                    self.plate[y][x]["square"] = Square.BLACK
                    self.plate[y][x]["piece"] = Square.EMPTY
                    self.plate[y][x]["player"] = 0

    def drawPlate(self):
        for y in range(0, Game.NB_PLATE_SQUARES):
            for x in range(0, Game.NB_PLATE_SQUARES):
                pieceSelected = True if x == self.pieceSelected.x() and y == self.pieceSelected.y() else False
                squarePossibility = True if self.game.getPointInPossibilities(self.squarePossibilities, QPoint(x, y)) else False
                if self.plate[y][x]["square"] == Square.BLACK:
                    self.drawSquare(x, y, Qt.gray, squarePossibility)
                else:
                    self.drawSquare(x, y, Qt.lightGray, squarePossibility)
                if self.plate[y][x]["piece"] == Square.BLACK:
                    self.drawPiece(x, y, Qt.black, pieceSelected)
                elif self.plate[y][x]["piece"] == Square.WHITE:
                    self.drawPiece(x, y, Qt.white, pieceSelected)
        self.update()

    def drawSquare(self, x, y, color, possibilty):
        painter = QPainter(self.image)
        color = Qt.darkGray if possibilty else QColor(color)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(x * self.squareDimension, y * self.squareDimension, self.squareDimension - 1,
                         self.squareDimension - 1)

    def drawPiece(self, x, y, color, selected):
        painter = QPainter(self.image)
        color = QColor(color)
        if selected:
            color.setAlpha(120)
        painter.setBrush(color)
        painter.setPen(color)
        posX = x * self.squareDimension + self.MARGIN
        posY = y * self.squareDimension + self.MARGIN
        width = self.squareDimension - 2 * self.MARGIN
        painter.drawEllipse(posX, posY, width, width)

    def drawPieceFromFile(self, x, y, path):
        piece = QPixmap(path)
        painter = QPainter(self.image)
        posX = x * self.squareDimension + self.MARGIN
        posY = y * self.squareDimension + self.MARGIN
        width = self.squareDimension - 2 * self.MARGIN
        painter.drawPixmap(posX, posY, width, width, piece)

    # Paint Event (override method)
    #   Called on window focus or resize
    #   Draw the image on widget
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isAnimationRunning:
            x, y = self.getSelectedSquare(event)
            pos = QPoint(x, y)
            # Case cliquée + Clique sur une possibilité
            if self.pieceSelected.x() != -1 and self.pieceSelected.y() != -1\
                    and self.game.getPointInPossibilities(self.squarePossibilities, pos) is not None:
                player = 1 if self.game.isTurnJ1() else 2
                # Move piece
                possibility = self.game.getPointInPossibilities(self.squarePossibilities, pos)
                #if possibility.getNbPiecesEat() == 0:
                self.plate[y][x]["piece"] = self.plate[self.pieceSelected.y()][self.pieceSelected.x()]["piece"]
                self.plate[y][x]["player"] = self.plate[self.pieceSelected.y()][self.pieceSelected.x()]["player"]
                self.plate[self.pieceSelected.y()][self.pieceSelected.x()]["piece"] = Square.EMPTY
                self.plate[self.pieceSelected.y()][self.pieceSelected.x()]["player"] = 0
                # Hungry mode
                if possibility.getNbPiecesEat() > 0:
                    for pieceEat in possibility.getPosPiecesEat():
                        self.plate[pieceEat.y()][pieceEat.x()]["piece"] = Square.EMPTY
                        self.plate[pieceEat.y()][pieceEat.x()]["player"] = 0
                    self.game.removePieces(possibility.getNbPiecesEat())
                self.pieceSelected = QPoint(-1, -1)
                self.squarePossibilities = []
                self.game.toggleTurn()
            # Clique sur une case du plateau
            else:
                self.pieceSelected = QPoint(-1, -1)
                self.squarePossibilities = []
                player = 1 if self.game.isTurnJ1() else 2
                if self.plate[y][x]["piece"] != Square.EMPTY and self.plate[y][x]["player"] == player:
                    self.pieceSelected = pos
                    self.squarePossibilities = self.game.getPossibility(pos)
            self.game.setPlate(self.plate)
            self.drawPlate()
            self.update()

    def getSelectedSquare(self, event):
        for y in range(0, Game.NB_PLATE_SQUARES):
            posYMin = y * self.squareDimension
            posYMax = y * self.squareDimension + self.squareDimension
            if posYMin <= event.pos().y() <= posYMax:
                for x in range(0, Game.NB_PLATE_SQUARES):
                    posXMin = x * self.squareDimension
                    posXMax = x * self.squareDimension + self.squareDimension
                    if posXMin <= event.pos().x() <= posXMax:
                        return x, y
        return -1, -1

    def printPlate(self, piece):
        for row in self.plate:
            for square in row:
                if piece:
                    sys.stdout.write(str(square["piece"].value))
                else:
                    sys.stdout.write(str(square["square"].value))
            sys.stdout.write("\n")
        sys.stdout.flush()
