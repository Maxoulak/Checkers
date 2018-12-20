from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

# Help Popup Class
#   Show when shortcut "Ctrl+H" is used or item menu "Help" is clicked
class HelpPopup(QWidget):
    # Init Method
    #   Init Window's title, width, height and icon
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Draughts' Help")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("./icons/paint-brush.png"))

        self.initUI()

    # Init UI Method
    #   Create the Help Message and display it in a label, which is within a layout
    def initUI(self):
        helpMsg = "Welcome to Draughts' Help !\n\n"
        helpMsg += "\"Game\" Menu\n"
        helpMsg += "\tRestart (Ctrl+R) : Restart the game\n"
        helpMsg += "\tActivate AI (Ctrl+I) : Restart the game and activate or desactivate AI\n"
        helpMsg += "\tQuit (Ctrl+Q) : Quit the application\n\n"
        helpMsg += "\"View\" Menu\n"
        helpMsg += "\tHighlight Possibilities : Highlight possible move for the player\n"
        helpMsg += "\"Help\" Menu\n"
        helpMsg += "\tAbout (Ctrl+A) : Show information about this application\n"
        helpMsg += "\tHelp (Ctrl+H) : Display this Help\n\n"
        layout = QHBoxLayout()
        layout.addWidget(QLabel(helpMsg))
        self.setLayout(layout)
        self.show()