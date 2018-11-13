import sys

from PyQt5.QtCore import QSize, Qt, QRectF, QPoint
from PyQt5.QtGui import QImage, QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget

from Square import Square

class CheckersPlateWidget(QWidget):
    NB_PLATE_SQUARES = 8
    MARGIN = 10

    def __init__(self, size):
        super().__init__()

        self.pieceSelected = QPoint(-1, -1)
        self.squarePossibility = []
        self.size = min(size.width(), size.height())
        self.setFixedSize(self.size, self.size)
        self.plate = []
        self.initPlate()
        self.initSquareDimension()

        self.initUI()

    def initSquareDimension(self):
        self.squareDimension = self.size / self.NB_PLATE_SQUARES

    def initUI(self):
        self.image = QImage(QSize(self.size, self.size), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawPlate()

    def initPlate(self):
        for i in range(0, self.NB_PLATE_SQUARES):
            self.plate.append([])
            for j in range(0, self.NB_PLATE_SQUARES):
                self.plate[i].append({})
                compare = 0 if i % 2 == 0 else 1
                if j % 2 == compare:
                    self.plate[i][j]["square"] = Square.WHITE
                    self.plate[i][j]["piece"] = Square.EMPTY
                    self.plate[i][j]["player"] = 0
                elif j < 3:
                    self.plate[i][j]["square"] = Square.BLACK
                    self.plate[i][j]["piece"] = Square.WHITE
                    self.plate[i][j]["player"] = 1
                elif j > 4:
                    self.plate[i][j]["square"] = Square.BLACK
                    self.plate[i][j]["piece"] = Square.BLACK
                    self.plate[i][j]["player"] = 2
                else:
                    self.plate[i][j]["square"] = Square.BLACK
                    self.plate[i][j]["piece"] = Square.EMPTY
                    self.plate[i][j]["player"] = 0

    def drawPlate(self):
        for y in range(0, self.NB_PLATE_SQUARES):
            for x in range(0, self.NB_PLATE_SQUARES):
                pieceSelected = True if x == self.pieceSelected.x() and y == self.pieceSelected.y() else False
                squarePossibility = True if self.isPointInArray(self.squarePossibility, QPoint(x, y)) else False
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
        if event.button() == Qt.LeftButton:
            x, y = self.getSelectedSquare(event)
            self.squarePossibility = []
            self.pieceSelected = QPoint(x, y)
            #if self.plate[y][x]["piece"] != Square.EMPTY:
            #    self.searchPossibility()
            self.drawPlate()
            self.update()

    def getSelectedSquare(self, event):
        for y in range(0, self.NB_PLATE_SQUARES):
            posYMin = y * self.squareDimension
            posYMax = y * self.squareDimension + self.squareDimension
            if posYMin <= event.pos().y() <= posYMax:
                for x in range(0, self.NB_PLATE_SQUARES):
                    posXMin = x * self.squareDimension
                    posXMax = x * self.squareDimension + self.squareDimension
                    if posXMin <= event.pos().x() <= posXMax:
                        return x, y
        return -1, -1

    def isPointInArray(self, array, pointToSearch):
        for point in array:
            if point.x() == pointToSearch.x() and point.y() == pointToSearch.y():
                return True
        return False

    def printPlate(self, piece):
        for row in self.plate:
            for square in row:
                if piece:
                    sys.stdout.write(str(square["piece"].value))
                else:
                    sys.stdout.write(str(square["square"].value))
            sys.stdout.write("\n")
        sys.stdout.flush()
