# Rate : int between 1 and 100
class Possibility:
    def __init__(self, piece, nbPiecesEat, posPiecesEat, pieceMoves, src):
        self.piecePosition = piece
        self.nbPiecesEat = nbPiecesEat
        self.rate = 0
        self.posPiecesEat = posPiecesEat
        self.pieceMoves = pieceMoves
        self.pieceGonnaBeQueen = False
        self.src = src

    # DEBUG PURPOSE
    def __str__(self):
        return str(self.piecePosition.x()) + " " + str(self.piecePosition.y())

    def setRate(self, rate):
        self.rate = rate

    def setPiecePosition(self, pos):
        self.piecePosition = pos

    def addNbPiecesEat(self):
        self.nbPiecesEat += 1

    def gonnaBeQueen(self):
        self.pieceGonnaBeQueen = True

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

    def isGonnaBeQueen(self):
        return self.pieceGonnaBeQueen

    def getSrc(self):
        return self.src
