# Rate : int between 1 and 100
class Possibility:
    def __init__(self, piece, nbPieceEat):
        self.piecePosition = piece
        self.nbPieceEat = nbPieceEat
        self.rate = 0

    def setRate(self, rate):
        self.rate = rate

    def setNbPieceEat(self, nbPieceEat):
        self.nbPieceEat = nbPieceEat

    def getRate(self):
        return self.rate

    def getNbPieceEat(self):
        return self.nbPieceEat

    def getPiece(self):
        return self.piecePosition