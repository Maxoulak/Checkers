import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

from CheckersContainerWidget import CheckersContainerWidget

class CheckersWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.checkersContainerWidget = CheckersContainerWidget(self.size())
        self.checkersPlateWidget = self.checkersContainerWidget.getCheckersPlateWidget()
        self.setCentralWidget(self.checkersContainerWidget)

        self.initMenus()

    def initUI(self):
        self.setWindowTitle("Draughts")
        self.setGeometry(80, 80, 1100, 800)
        self.setWindowIcon(QIcon("./icons/checkers.png"))

        self.show()

    def initMenus(self):
        mainMenu = self.menuBar()
        gameMenu = mainMenu.addMenu(" Game")
        viewMenu = mainMenu.addMenu(" View")
        helpMenu = mainMenu.addMenu(" ?")

        restartAction = QAction(QIcon("./icons/restart.png"), "Restart", self)
        restartAction.setShortcut("Ctrl+R")
        gameMenu.addAction(restartAction)
        restartAction.triggered.connect(self.checkersContainerWidget.restartGame)

        IAAction = QAction("Activate AI", self, checkable=True)
        IAAction.setChecked(False)
        gameMenu.addAction(IAAction)
        IAAction.triggered.connect(self.checkersPlateWidget.toggleAI)

        highlightPossibilitiesAction = QAction("Highlight Possibilities", self, checkable=True)
        highlightPossibilitiesAction.setChecked(True)
        viewMenu.addAction(highlightPossibilitiesAction)
        highlightPossibilitiesAction.triggered.connect(self.checkersPlateWidget.toggleHighlightPossibilities)

        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        #aboutAction.triggered.connect(self.about)

        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        #helpAction.triggered.connect(self.helpFct)

# Main Function
if __name__ == "__main__":
    try:
        sys.setrecursionlimit(10000)
        app = QApplication(sys.argv)
        window = CheckersWindow()
        window.show()
        app.exec()
    except Exception as e:
        print(e)
