
class AiPlayer:

    def __init__(self, game):
        self.rate = []
        self.game = game

    def setRate(self):
        print(self.game.getClickablePieces())
        for clickablePiece in self.game.clickablePieces:
            self.setRateClickablePiece(clickablePiece)
            for pos in clickablePiece.getPossibilities():
                self.rate.append(pos)
                print(pos.getPos())
        self.rate = []

    def play(self):
        print("Je joue!")
        self.setRate()

    def setRateClickablePiece(self, clickablePiece):
        print(self.game.plate[clickablePiece.piecePosition.y()][clickablePiece.piecePosition.x()])
        print(clickablePiece.piecePosition.x())
        print(clickablePiece.piecePosition.y())