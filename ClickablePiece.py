# Clickable Piece Class
#   Represent a piece which can be selected and move by the user (or AI)
class ClickablePiece:
    # Init Method
    #   Init Class variables
    def __init__(self, pos, queen):
        self.piecePosition = pos
        self.possibilities = []
        self.queen = queen

    # Set Possibilities
    #   Setter for possibilities
    def setPossibilities(self, possibilities):
        self.possibilities = possibilities

    # Append Possibilities
    #   Add a possibility to current possibilities
    def appendPossibilites(self, possibility):
        self.possibilities.append(possibility)

    # Get Pos
    #   Return piece's position
    def getPos(self):
        return self.piecePosition

    # Get Possibilitites
    #   Return the current possibilities
    def getPossibilities(self):
        return self.possibilities

    # Get Nb Possibilities
    #   Return the number of current possibilities
    def getNbPossibilities(self):
        return len(self.possibilities)

    # Has Possibilities
    #   Return true if there is at least one possibility in the current possibilities
    def hasPossibilities(self):
        return True if len(self.possibilities) > 0 else False

    # Is Queen
    #   Return true if the piece is a queen, false otherwise
    def isQueen(self):
        return self.queen