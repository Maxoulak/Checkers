from PyQt5.QtWidgets import QWidget, QHBoxLayout

from CheckersPlateWidget import CheckersPlateWidget

class CheckersContainerWidget(QWidget):
    def __init__(self, size):
        super().__init__()

        self.checkersPlateWidget = CheckersPlateWidget(size)

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.checkersPlateWidget)
        self.setLayout(self.mainLayout)

    def getCheckersPlateWidget(self):
        return self.checkersPlateWidget
