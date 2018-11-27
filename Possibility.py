# Rate : int between 1 and 100
class Possibility:
    def __init__(self, piece, nbPiecesEat, posPiecesEat, pieceMoves):
        self.piecePosition = piece
        self.nbPiecesEat = nbPiecesEat
        self.rate = 0
        self.posPiecesEat = posPiecesEat
        self.pieceMoves = pieceMoves

    def setRate(self, rate):
        self.rate = rate

    def setNbPieceEat(self, nbPieceEat):
        self.nbPiecesEat = nbPieceEat

    def getRate(self):
        return self.rate

    def getNbPiecesEat(self):
        return self.nbPiecesEat

    def getPos(self):
        return self.piecePosition

    def getPosPiecesEat(self):
        return self.posPiecesEat

    def getPieceMoves(self):
        return self.pieceMoves