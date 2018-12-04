from PyQt5.QtCore import QPoint


class AiPlayer:

    def __init__(self, game):
        self.rate = []
        self.game = game

    def setRate(self):
        #print(self.game.getClickablePieces())
        self.rate = []
        for clickablePiece in self.game.clickablePieces:
            self.ifCanBeEat(clickablePiece)
            for pos in clickablePiece.getPossibilities():
                self.rate.append(pos)
                #print(pos.getPos())
                #print(pos.getRate())

    def play(self):
        print("Je joue!")
        self.setRate()
        tmpMove = self.rate[0]
        shuffle = True
        for move in self.rate:
            #print("je passe")
            #print(move)
            if move.getRate() > tmpMove.getRate():
                shuffle = False
                tmpMove = move
        #print("ok")
        try:
            #self.game.movePiece(tmpMove.getSrc(), tmpMove.getPos(), self.game.plate, True)
            self.game.container.checkersPlateWidget.startAnimation(tmpMove, tmpMove.getSrc())
        except Exception as e:
            print(e)


    def ifCanBeEat(self, clickablePiece):
        pointX = clickablePiece.piecePosition.x()
        pointY = clickablePiece.piecePosition.y()
        if self.checkDiagBotTop(pointY, pointX):
            if self.game.plate[pointY + 1][pointX - 1]["player"] == 1:
                self.ratePiece(clickablePiece, 30)
        if self.checkDiagTopBot(pointY, pointX):
            if self.game.plate[pointY + 1][pointX + 1]["player"] == 1:
                self.ratePiece(clickablePiece, 30)

    def ratePiece(self, clickablePiece, value):
        for pos in clickablePiece.getPossibilities():
            pos.setRate(pos.getRate() + value)

    def checkDiagTopBot(self, pointY, pointX):
        rightBot = QPoint(pointY + 1, pointX + 1)
        leftTop = QPoint(pointY - 1, pointX - 1)
        if self.game.isValidSquare(rightBot) and self.game.isValidSquare(leftTop):
            return True
        return False

    def checkDiagBotTop(self, pointY, pointX):
        rightTop = QPoint(pointY + 1, pointX - 1)
        leftBot = QPoint(pointY - 1, pointX + 1)
        if self.game.isValidSquare(rightTop) and self.game.isValidSquare(leftBot):
            return True
        return False