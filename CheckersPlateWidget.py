import functools
import sys
import time

from PyQt5 import QtTest
from PyQt5.QtCore import QSize, Qt, QRectF, QPoint, QTimer
from PyQt5.QtGui import QImage, QPainter, QPen, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from AI.Ai import AiPlayer
from Game import Game
from Square import Square

# Checkers Plate Widget Class
#   Contains the plate
class CheckersPlateWidget(QWidget):
    MARGIN = 10
    MARGIN_CROWN = 25
    TIMER_AI_TURN_MS = 150

    # Init Method
    #   Init plate size and class variables
    def __init__(self, size, container):
        super().__init__()

        self.container = container
        self.highlightPossibilities = True
        self.size = min(size.width(), size.height())
        self.setFixedSize(self.size, self.size)
        self.initSquareDimension()
        self.initGameVariables(False)

    # Init Game Variables
    #   Init the game's variables
    def initGameVariables(self, restart):
        self.pieceSelected = QPoint(-1, -1)
        self.squarePossibilities = []
        self.plate = []
        self.initPlate()
        self.isAnimationRunning = False
        self.currentAnimationIndex = 0
        self.currentAnimationPossibility = None
        self.currentAnimationOldPos = QPoint(-1, -1)
        if restart:
            self.game.setPlate(self.plate)
        else:
            self.game = Game(self.plate, self.container)
        self.initUI()

    # Init UI Method
    #   Create the image where the plate is draw and draw it
    def initUI(self):
        self.image = QImage(QSize(self.size, self.size), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawPlate()

    # Restart Game
    #   Init back the variables and restart the game
    def restartGame(self):
        self.initGameVariables(True)
        self.game.restartGame(self.plate)

    # Toggle AI
    #   Restart the game et toggle AI
    def toggleAI(self):
        ai = self.game.Ai
        self.container.restartGame()
        self.game.Ai = False if ai else True

    # Init Square Dimension
    #   Calculate squares' dimension
    def initSquareDimension(self):
        self.squareDimension = self.size / Game.NB_PLATE_SQUARES

    # Init Plate
    #   Init the plate in a double array
    def initPlate(self):
        for y in range(0, Game.NB_PLATE_SQUARES):
            self.plate.append([])
            for x in range(0, Game.NB_PLATE_SQUARES):
                self.plate[y].append({})
                compare = 0 if y % 2 == 0 else 1
                self.plate[y][x]["queen"] = False
                if x % 2 == compare:
                    self.plate[y][x]["square"] = Square.WHITE
                    self.plate[y][x]["piece"] = Square.EMPTY
                    self.plate[y][x]["player"] = 0
                elif x < Game.NB_LINE_OCCUPED:
                    self.plate[y][x]["square"] = Square.BLACK
                    self.plate[y][x]["piece"] = Square.WHITE
                    self.plate[y][x]["player"] = 2
                elif x > Game.NB_PLATE_SQUARES - 1 - Game.NB_LINE_OCCUPED:
                    self.plate[y][x]["square"] = Square.BLACK
                    self.plate[y][x]["piece"] = Square.BLACK
                    self.plate[y][x]["player"] = 1
                else:
                    self.plate[y][x]["square"] = Square.BLACK
                    self.plate[y][x]["piece"] = Square.EMPTY
                    self.plate[y][x]["player"] = 0

    # Toggle Highlight Possibilities
    #   Enable or disable show of possibilities
    def toggleHighlightPossibilities(self):
        self.highlightPossibilities = False if self.highlightPossibilities else True

    # Draw Plate
    #   Draw the plate on the image from the double array
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
                if self.plate[y][x]["queen"] == True:
                    posX = x * self.squareDimension + self.MARGIN_CROWN
                    posY = y * self.squareDimension + self.MARGIN_CROWN
                    width = self.squareDimension - 2 * self.MARGIN_CROWN
                    self.drawPieceFromFile(posX, posY, width, "./icons/crown")
        self.update()

    # Draw Square
    #   Draw a square on the image
    def drawSquare(self, x, y, color, possibility):
        painter = QPainter(self.image)
        color = Qt.darkGray if possibility and self.highlightPossibilities else QColor(color)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(x * self.squareDimension, y * self.squareDimension, self.squareDimension - 1,
                         self.squareDimension - 1)

    # Draw Piece
    #   Draw a piece on the image
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

    # Draw Piece From File
    #   Draw a piece from a file on the image
    def drawPieceFromFile(self, posX, posY, width, path):
        piece = QPixmap(path)
        painter = QPainter(self.image)
        painter.drawPixmap(posX, posY, width, width, piece)

    # Paint Event (override method)
    #   Called on window focus or resize
    #   Draw the image on widget
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    # Mouse Press Event (override method)
    #   Called when user press a button on mouse
    #   Move a piece or select one
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.game.hasWon():
            if not self.isAnimationRunning and not self.game.isTurnAI():
                x, y = self.getSelectedSquare(event)
                pos = QPoint(x, y)
                # Case cliquée + Clique sur une possibilité
                if self.pieceSelected.x() != -1 and self.pieceSelected.y() != -1\
                        and self.game.getPointInPossibilities(self.squarePossibilities, pos) is not None:
                    possibility = self.game.getPointInPossibilities(self.squarePossibilities, pos)
                    self.startAnimation(possibility, self.pieceSelected)
                    self.pieceSelected = QPoint(-1, -1)
                    self.squarePossibilities = []
                # Clique sur une case du plateau
                else:
                    self.pieceSelected = QPoint(-1, -1)
                    self.squarePossibilities = []
                    player = 1 if self.game.isTurnJ1() else 2
                    if self.plate[y][x]["piece"] != Square.EMPTY and self.plate[y][x]["player"] == player:
                        if not self.game.isGameRunning():
                            self.game.launchGame()
                        self.pieceSelected = pos
                        self.squarePossibilities = self.game.getPossibility(pos)
                self.game.setPlate(self.plate)
                self.drawPlate()
                self.update()

    # Start Animation
    #   Start a piece's move (and/or eat)
    def startAnimation(self, possibility, fromPiece):
        self.isAnimationRunning = True
        self.currentAnimationIndex = 0
        self.currentAnimationPossibility = possibility
        self.currentAnimationOldPos = fromPiece
        QTimer.singleShot(self.TIMER_AI_TURN_MS if self.game.isTurnAI() else 10, self.doAnimation)

    # Do Animation
    #   Move and/or eat a piece
    def doAnimation(self):
        possibility = self.currentAnimationPossibility
        i = self.currentAnimationIndex
        if i < len(possibility.getPieceMoves()):
            self.game.movePiece(self.currentAnimationOldPos, possibility.getPieceMoves()[i], self.plate, True)
            self.currentAnimationOldPos = possibility.getPieceMoves()[i]
            if i < possibility.getNbPiecesEat():
                self.game.eatPiece(possibility.getPosPiecesEat()[i], self.plate)
            self.currentAnimationIndex += 1
            self.game.setPlate(self.plate)
            self.drawPlate()
            self.update()
            if self.currentAnimationIndex >= len(possibility.getPieceMoves()):
                self.game.removePieces(possibility.getNbPiecesEat())
                self.isAnimationRunning = False
                self.currentAnimationPossibility = None
                self.currentAnimationIndex = 0
                if not self.checkWin():
                    self.game.toggleTurn()
            else:
                QTimer.singleShot(500, self.doAnimation)

    # Get Selected Square
    #   Convert mouse coordinates to a specific cell
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

    # Check Win
    #   Display a message if someone won
    def checkWin(self):
        if self.checkLoose():
            self.game.stopGame(True)
            player = "Black" if self.game.isTurnJ1() else "White"
            if not self.game.isAi():
                QMessageBox.about(self, "Win !", "Player " + player + " won !")
            elif not self.game.isTurnJ1():
                QMessageBox.about(self, "Loose !", "You loose ... AI won !")
            else:
                QMessageBox.about(self, "Win !", "You win against the AI !")
            return True
        return False

    # Check Loose
    #   Check if a player loose
    def checkLoose(self):
        player = 2 if self.game.isTurnJ1() else 1
        for y in range(0, self.game.NB_PLATE_SQUARES):
            for x in range(0, self.game.NB_PLATE_SQUARES):
                if self.plate[y][x]["player"] == player:
                    return False
        return True

    # Get Game
    #   Return the Game class
    def getGame(self):
        return self.game