import random

from PyQt5.QtCore import QPoint


class AiPlayer:

    def __init__(self, game):
        self.rate = []
        self.game = game

    def resetRate(self):
        """
        Set all rates of possibilities to 0
        :return:
        """
        for clickablePiece in self.game.clickablePieces:
            for pos in clickablePiece.getPossibilities():
                pos.setRate(0)

    def setRate(self):
        print(self.game.getClickablePieces())
        self.rate = []
        self.resetRate()
        for clickablePiece in self.game.clickablePieces:
            self.ifCanBeEat(clickablePiece)
            for pos in clickablePiece.getPossibilities():
                self.rate.append(pos)
                self.confortMove(pos, clickablePiece)
                self.eatMove(pos, clickablePiece)
                self.ifCanBeEatAfterMove(clickablePiece, pos)
                print(pos.getPos())
                print(pos.getRate())

    def play(self):
        print("Je joue!")
        self.setRate()
        tmpMove = self.rate[0]
        movePossibilities = []
        movePossibilities.append(tmpMove)
        shuffle = False
        for move in self.rate:
            if move.getRate() > tmpMove.getRate():
                shuffle = False
                movePossibilities = []
                movePossibilities.append(move)
                tmpMove = move
            elif move.getRate() == tmpMove.getRate():
                shuffle = True
                movePossibilities.append(move)
        if shuffle:
            random.shuffle(movePossibilities)
        self.game.container.checkersPlateWidget.startAnimation(movePossibilities[0], movePossibilities[0].getSrc())


    def ifCanBeEat(self, clickablePiece):
        """
        Check if piece can be eat, if yes, up rate to 30
        :param clickablePiece:
        :return:
        """
        pointX = clickablePiece.piecePosition.x()
        pointY = clickablePiece.piecePosition.y()
        if self.checkDiagBotTop(pointY, pointX):
            if self.game.plate[pointY - 1][pointX + 1]["player"] == 1 and self.game.plate[pointY + 1][pointX - 1]["player"] == 0:
                self.ratePiece(clickablePiece, 50)
        if self.checkDiagTopBot(pointY, pointX):
            if self.game.plate[pointY + 1][pointX + 1]["player"] == 1 and self.game.plate[pointY - 1][pointX - 1]["player"] == 0:
                self.ratePiece(clickablePiece, 50)

    def ifCanBeEatAfterMove(self, clickablePiece, pos):
        """
        Check if piece can be eat after a move, if yes, up rate to 30
        :param clickablePiece:
        :param pos
        :return:
        """
        pointX = pos.getPos().x()
        pointY = pos.getPos().y()
        self.game.plate[clickablePiece.piecePosition.y()][clickablePiece.piecePosition.x()]["player"] = 0
        if self.checkDiagBotTop(pointY, pointX):
            if self.game.plate[pointY - 1][pointX + 1]["player"] == 1 and self.game.plate[pointY + 1][pointX - 1]["player"] == 0:
                pos.setRate(pos.getRate() - 30)
        if self.checkDiagTopBot(pointY, pointX):
            if self.game.plate[pointY + 1][pointX + 1]["player"] == 1 and self.game.plate[pointY - 1][pointX - 1]["player"] == 0:
                pos.setRate(pos.getRate() - 30)
        self.game.plate[clickablePiece.piecePosition.y()][clickablePiece.piecePosition.x()]["player"] = 2

    def ifMoveIsQueen(self, pos):
        """
        Check if next move can be a Queen, if yes up rate by 40
        :param pos:
        :return:
        """
        if pos.getPos().x() > 6:
            pos.setRate(pos.getRate() + 40)

    def ratePiece(self, clickablePiece, value):
        """
        Up rate of all possibilities of a piece by 30
        :param clickablePiece:
        :param value:
        :return:
        """
        for pos in clickablePiece.getPossibilities():
            pos.setRate(pos.getRate() + value)

    def confortMove(self, pos, clickablePiece):
        """
        Check if the move is safe with a whole or a piece
        If safe, up rate by 10
        :param pos:
        :param clickablePiece:
        :return:
        """
        self.game.plate[clickablePiece.piecePosition.y()][clickablePiece.piecePosition.x()]["player"] = 0
        if self.game.isValidSquare(QPoint(pos.getPos().y() - 1, pos.getPos().x() - 1)):
            if self.game.plate[pos.getPos().y() - 1][pos.getPos().x() - 1]["player"] == 2:
                pos.setRate(pos.getRate() + 10)
        else:
            pos.setRate(pos.getRate() + 10)
        if self.game.isValidSquare(QPoint(pos.getPos().y() + 1, pos.getPos().x() - 1)):
            if self.game.plate[pos.getPos().y() + 1][pos.getPos().x() - 1]["player"] == 2:
                pos.setRate(pos.getRate() + 10)
        else:
            pos.setRate(pos.getRate() + 10)
        self.game.plate[clickablePiece.piecePosition.y()][clickablePiece.piecePosition.x()]["player"] = 2

    def eatMove(self, pos, clickablePiece):
        """
        If piece can eat, up rate by 30 by piece eat
        :param pos:
        :param clickablePiece:
        :return:
        """
        if (pos.getPos().x() - clickablePiece.piecePosition.x()) > 1:
            pos.setRate(pos.getRate() + 30)
        if (pos.getPos().x() - clickablePiece.piecePosition.x()) > 2:
            pos.setRate(pos.getRate() + 30)

    def checkDiagTopBot(self, pointY, pointX):
        """
        Check if one square in diag left-top and right-bottom is valid
        :param pointY:
        :param pointX:
        :return:
        """
        rightBot = QPoint(pointY + 1, pointX + 1)
        leftTop = QPoint(pointY - 1, pointX - 1)
        if self.game.isValidSquare(rightBot) and self.game.isValidSquare(leftTop):
            return True
        return False

    def checkDiagBotTop(self, pointY, pointX):
        """
        Check if one square in diag left-bottom and right-top is valid
        :param pointY:
        :param pointX:
        :return:
        """
        rightTop = QPoint(pointY - 1, pointX + 1)
        leftBot = QPoint(pointY + 1, pointX - 1)
        if self.game.isValidSquare(rightTop) and self.game.isValidSquare(leftBot):
            return True
        return False