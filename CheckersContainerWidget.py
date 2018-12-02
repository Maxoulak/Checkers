from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from CheckersPlateWidget import CheckersPlateWidget

class CheckersContainerWidget(QWidget):
    def __init__(self, size):
        super().__init__()

        self.checkersPlateWidget = CheckersPlateWidget(size)

        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.checkersPlateWidget)
        self.mainLayout.addLayout(self.vLayout)
        self.setLayout(self.mainLayout)

    def getCheckersPlateWidget(self):
        return self.checkersPlateWidget
