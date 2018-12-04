class ClickablePiece:

    def __init__(self, pos, queen):
        self.piecePosition = pos
        self.possibilities = []
        self.queen = queen

    def setPossibilities(self, possibilities):
        self.possibilities = possibilities

    def appendPossibilites(self, possibility):
        self.possibilities.append(possibility)

    def getPos(self):
        return self.piecePosition

    def getPossibilities(self):
        return self.possibilities

    def getNbPossibilities(self):
        return len(self.possibilities)

    def hasPossibilities(self):
        return True if len(self.possibilities) > 0 else False

    def isQueen(self):
        return self.queen