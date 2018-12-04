
class AiPlayer:

    def __init__(self, game):
        self.rate = []
        self.game = game

    def setRate(self):
        print(self.game.getClickablePieces())
        for clickablePiece in self.game.clickablePieces:
            print(clickablePiece.piecePosition)
            for pos in clickablePiece.getPossibilities():
                self.rate.append(pos.getPos(), )
                print(pos.getPos())
    def play(self):
        print("Je joue!")
        self.setRate()
        return