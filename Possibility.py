# Possibility Class
#   Represent a possible piece move
class Possibility:
    # Init Method
    #   Init Class variables
    def __init__(self, piece, nbPiecesEat, posPiecesEat, pieceMoves, src):
        self.piecePosition = piece
        self.nbPiecesEat = nbPiecesEat
        self.rate = 0
        self.posPiecesEat = posPiecesEat
        self.pieceMoves = pieceMoves
        self.pieceGonnaBeQueen = False
        self.src = src

    # Set Rate
    #   Setter for rate
    def setRate(self, rate):
        self.rate = rate

    # Set Piece Position
    #   Setter for piece position
    def setPiecePosition(self, pos):
        self.piecePosition = pos

    # Add Nb Pieces Eat
    #   Increment by one the number of piece eat
    def addNbPiecesEat(self):
        self.nbPiecesEat += 1

    # Gonna Be Queen
    #   This possibility make the piece to be queen
    def gonnaBeQueen(self):
        self.pieceGonnaBeQueen = True

    # Get Rate
    #   Return the rate
    def getRate(self):
        return self.rate

    # Get Nb Pieces Eat
    #   Return the number of eaten pieces
    def getNbPiecesEat(self):
        return self.nbPiecesEat

    # Get Pos
    #   Return the piece position
    def getPos(self):
        return self.piecePosition

    # Get Pos Pieces Eat
    #   Return an array of eaten pieces position
    def getPosPiecesEat(self):
        return self.posPiecesEat

    # Get Piece Moves
    #   Return an array of piece move position
    def getPieceMoves(self):
        return self.pieceMoves

    # Is Gonna Be Queen
    #    Return true if the possibility will transform the piece to queen, false otherwise
    def isGonnaBeQueen(self):
        return self.pieceGonnaBeQueen

    # Get Src
    #   Return the piece's start position
    def getSrc(self):
        return self.src
