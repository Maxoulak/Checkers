import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication

from CheckersContainerWidget import CheckersContainerWidget

class CheckersWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.checkersContainerWidget = CheckersContainerWidget(self.size())
        self.checkersPlateWidget = self.checkersContainerWidget.getCheckersPlateWidget()
        self.setCentralWidget(self.checkersContainerWidget)

    def initUI(self):
        self.setWindowTitle("Checkers")
        self.setGeometry(80, 80, 1100, 800)
        self.setWindowIcon(QIcon("./icons/checkers.png"))

        self.show()

# Main Function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckersWindow()
    window.show()
    app.exec()
