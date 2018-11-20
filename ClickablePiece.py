class ClickablePiece:

    def __init__(self, pos):
        self.piecePosition = pos
        self.possibilities = []

    def setPossibilities(self, possibilities):
        self.possibilities = possibilities

    def appendPossibilites(self, possibility):
        self.possibilities.append(possibility)

    def getPiecePosition(self):
        return self.piecePosition

    def getPossibilities(self):
        return self.possibilities