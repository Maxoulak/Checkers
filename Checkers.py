import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication

from Square import Square

# Plate starts with WHITE square

class Checkers(QMainWindow):
    PLATE_WIDTH = 8
    PLATE_HEIGHT = 8

    def __init__(self):
        super().__init__()

        self.plate = []
        self.platePiece = []
        self.initPlate()
        self.showPlate(True)
        print("")
        self.showPlate(False)

        self.initUI()

    def showPlate(self, piece):
        for row in self.plate:
            for square in row:
                if piece:
                    sys.stdout.write(str(square["piece"].value))
                else:
                    sys.stdout.write(str(square["square"].value))
            sys.stdout.write("\n")
        sys.stdout.flush()

    def initPlate(self):
        for i in range(0, self.PLATE_HEIGHT):
            self.plate.append([])
            for j in range(0, self.PLATE_WIDTH):
                self.plate[i].append({})
                if i % 2 == 0:
                    compare = 0
                else:
                    compare = 1
                if j % 2 == compare:
                    self.plate[i][j]["square"] = Square.WHITE
                    self.plate[i][j]["piece"] = Square.EMPTY
                elif j < 3:
                    self.plate[i][j]["square"] = Square.BLACK
                    self.plate[i][j]["piece"] = Square.WHITE
                elif j > 4:
                    self.plate[i][j]["square"] = Square.BLACK
                    self.plate[i][j]["piece"] = Square.BLACK
                else:
                    self.plate[i][j]["square"] = Square.BLACK
                    self.plate[i][j]["piece"] = Square.EMPTY



    def initUI(self):
        self.setWindowTitle("Checkers")
        self.setGeometry(80, 80, 1000, 1000)
        self.setWindowIcon(QIcon("./icons/checkers.png"))

        self.show()

# Main Function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Checkers()
    window.show()
    app.exec()
