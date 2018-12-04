from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QGridLayout, QPushButton

from CheckersPlateWidget import CheckersPlateWidget

class CheckersContainerWidget(QWidget):
    def __init__(self, size):
        super().__init__()

        self.checkersPlateWidget = CheckersPlateWidget(size, self)
        self.NB_PIECE_PER_PLAYER = self.checkersPlateWidget.getGame().NB_PIECE_PER_PLAYER

        self.initUI()

    def initUI(self):
        self.player1RemainingPieces = QLabel(str(self.NB_PIECE_PER_PLAYER))
        self.player2RemainingPieces = QLabel(str(self.NB_PIECE_PER_PLAYER))
        self.player1EatPieces = QLabel("0")
        self.player2EatPieces = QLabel("0")
        self.player1Timer = QLabel("00:00")
        self.player2Timer = QLabel("00:00")
        self.playerTurn = QLabel("Player 1's turn")

        self.mainLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.createPlayerGroupBox(1, self.player1RemainingPieces,
                                                         self.player1EatPieces, self.player1Timer))
        self.vLayout.addWidget(self.createPlayerGroupBox(2, self.player2RemainingPieces,
                                                         self.player2EatPieces, self.player2Timer))
        self.vLayout.addWidget(self.createToolsGroupBox())

        self.mainLayout.addWidget(self.checkersPlateWidget)
        self.mainLayout.addLayout(self.vLayout)
        self.setLayout(self.mainLayout)

    def restartGame(self):
        self.checkersPlateWidget.getGame().stopGame()
        self.player1RemainingPieces.setText(str(self.NB_PIECE_PER_PLAYER))
        self.player2RemainingPieces.setText(str(self.NB_PIECE_PER_PLAYER))
        self.player1EatPieces.setText("0")
        self.player2EatPieces.setText("0")
        self.player1Timer.setText("00:00")
        self.player2Timer.setText("00:00")
        self.playerTurn.setText("Player 1's turn")
        self.checkersPlateWidget.restartGame()

    def updateUI(self):
        game = self.checkersPlateWidget.getGame()
        self.player1RemainingPieces.setText(str(game.getNbPiecesPlayer1()))
        self.player2RemainingPieces.setText(str(game.getNbPiecesPlayer2()))
        self.player1EatPieces.setText(str(self.NB_PIECE_PER_PLAYER - game.getNbPiecesPlayer2()))
        self.player2EatPieces.setText(str(self.NB_PIECE_PER_PLAYER - game.getNbPiecesPlayer1()))

    def updateTimerUI(self):
        self.player1Timer.setText("%02d:%02d" % (self.checkersPlateWidget.getGame().getTimeMinJ1(),
                                                 self.checkersPlateWidget.getGame().getTimeSecJ1()))
        self.player2Timer.setText("%02d:%02d" % (self.checkersPlateWidget.getGame().getTimeMinJ2(),
                                                 self.checkersPlateWidget.getGame().getTimeSecJ2()))

    def createPlayerGroupBox(self, player, playerRemainingPieces, playerEatPieces, playerTimer):
        title = "Player 1 (Black)"
        if player == 2:
            title = "Player 2 (White)"
        groupBox = QGroupBox(title)
        groupBox.setFixedSize(300, 200)
        layout = QGridLayout()
        layout.addWidget(QLabel("Remaining:"), 0, 0)
        layout.addWidget(playerRemainingPieces, 0, 1)
        layout.addWidget(QLabel("Jumps:"), 1, 0)
        layout.addWidget(playerEatPieces, 1, 1)
        layout.addWidget(QLabel("Time:"), 2, 0)
        layout.addWidget(playerTimer, 2, 1)
        groupBox.setLayout(layout)
        return groupBox

    def createToolsGroupBox(self):
        groupBox = QGroupBox("Game Tools")
        groupBox.setFixedSize(300, 200)
        layout = QGridLayout()
        restartBtn = QPushButton("Restart")
        layout.addWidget(restartBtn, 0, 0, 1, 2)
        groupBox.setLayout(layout)
        return groupBox

    def getCheckersPlateWidget(self):
        return self.checkersPlateWidget
