import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QMessageBox

from CheckersContainerWidget import CheckersContainerWidget
from HelpPopup import HelpPopup

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

        AIAction = QAction("Activate AI", self, checkable=True)
        AIAction.setChecked(False)
        AIAction.setShortcut("Ctrl+I")
        gameMenu.addAction(AIAction)
        AIAction.triggered.connect(self.checkersPlateWidget.toggleAI)

        exitAction = QAction(QIcon("./icons/exit.png"), "Quit", self)
        exitAction.setShortcut("Ctrl+Q")
        gameMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exitFct)

        highlightPossibilitiesAction = QAction("Highlight Possibilities", self, checkable=True)
        highlightPossibilitiesAction.setChecked(True)
        viewMenu.addAction(highlightPossibilitiesAction)
        highlightPossibilitiesAction.triggered.connect(self.checkersPlateWidget.toggleHighlightPossibilities)

        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.helpFct)

    # About
    #   Display the description of the application in a dialog box
    #   Add a button to About Qt dialog box
    def about(self):
        about = QMessageBox(self)
        about.setWindowTitle("About Draughts")
        about.setText("Draughts Application V1, developed in December, 2018 by Thomas Bunel and Maxime Maisonnas, in Python, using the library Qt.")
        btn = about.addButton("About Qt", QMessageBox.ActionRole)
        btn.clicked.connect(self.aboutQt)
        about.addButton(QMessageBox.Ok)
        about.show()

    # About Qt
    #   Display a dialog box with Qt's version information
    def aboutQt(self):
        QMessageBox.aboutQt(self)

    # Help Function
    #   Show the popup widget Help
    def helpFct(self):
        self.helpPopup = HelpPopup()
        self.helpPopup.show()

    # Close Event (override)
    #   Ask user to confirm exit
    def closeEvent(self, event):
        self.exitFct()
        event.ignore()

    # Exit
    #   Called when user quit the application
    #   Show a dialog box and ask user to confirm exit
    def exitFct(self):
        choice = QMessageBox.question(self, "Exit", "Are you sure you want to exit ?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()

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
