from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox, QGridLayout, QPushButton

from CheckersPlateWidget import CheckersPlateWidget

# Checkers Widget Container Class
#   Includes the Plate and init the right pannel
#   Included by the Main Window
class CheckersContainerWidget(QWidget):
    # Init
    #   Init class variables and the plate
    def __init__(self, size):
        super().__init__()

        self.checkersPlateWidget = CheckersPlateWidget(size, self)
        self.game = self.checkersPlateWidget.getGame()

        self.initUI()

    # Init UI Method
    #   Add the Plate to the layout
    #   Create and Add the Right Panel to the layout
    def initUI(self):
        self.player1RemainingPieces = QLabel(str(self.game.NB_PIECE_PER_PLAYER))
        self.player2RemainingPieces = QLabel(str(self.game.NB_PIECE_PER_PLAYER))
        self.player1EatPieces = QLabel("0")
        self.player2EatPieces = QLabel("0")
        self.player1Timer = QLabel("%02d:%02d" % (self.game.NB_MIN_PER_PLAYER, self.game.NB_SEC_PER_PLAYER))
        self.player2Timer = QLabel("%02d:%02d" % (self.game.NB_MIN_PER_PLAYER, self.game.NB_SEC_PER_PLAYER))
        self.playerTurn = QLabel("Player 1's turn")

        self.mainLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()
        self.groupBoxPlayer1 = self.createPlayerGroupBox(1, self.player1RemainingPieces, self.player1EatPieces, self.player1Timer)
        self.groupBoxPlayer2 = self.createPlayerGroupBox(2, self.player2RemainingPieces, self.player2EatPieces, self.player2Timer)
        self.vLayout.addWidget(self.groupBoxPlayer1)
        self.vLayout.addWidget(self.groupBoxPlayer2)
        self.vLayout.addWidget(self.createToolsGroupBox())

        self.mainLayout.addWidget(self.checkersPlateWidget)
        self.mainLayout.addLayout(self.vLayout)
        self.setLayout(self.mainLayout)

    # Toogle AI
    #   Enable or disable AI
    #   Change the name of the player on the right pannel
    def toggleAI(self):
        self.checkersPlateWidget.toggleAI()
        if self.checkersPlateWidget.game.isAi():
            self.groupBoxPlayer2.setTitle("AI (White)")
        else:
            self.groupBoxPlayer2.setTitle("Player 2 (White)")

    # Restart Game
    #   Restart the game and init back the right pannel
    def restartGame(self):
        self.game.stopGame(False)
        self.player1RemainingPieces.setText(str(self.game.NB_PIECE_PER_PLAYER))
        self.player2RemainingPieces.setText(str(self.game.NB_PIECE_PER_PLAYER))
        self.player1EatPieces.setText("0")
        self.player2EatPieces.setText("0")
        self.player1Timer.setText("%02d:%02d" % (self.game.NB_MIN_PER_PLAYER, self.game.NB_SEC_PER_PLAYER))
        self.player2Timer.setText("%02d:%02d" % (self.game.NB_MIN_PER_PLAYER, self.game.NB_SEC_PER_PLAYER))
        self.playerTurn.setText("Player 1's turn")
        self.checkersPlateWidget.restartGame()

    # Update UI
    #   Update the game information on the right pannel
    def updateUI(self):
        self.player1RemainingPieces.setText(str(self.game.getNbPiecesPlayer1()))
        self.player2RemainingPieces.setText(str(self.game.getNbPiecesPlayer2()))
        self.player1EatPieces.setText(str(self.game.NB_PIECE_PER_PLAYER - self.game.getNbPiecesPlayer2()))
        self.player2EatPieces.setText(str(self.game.NB_PIECE_PER_PLAYER - self.game.getNbPiecesPlayer1()))

    # Update Timer UI
    #   Update the timers on the right pannel
    def updateTimerUI(self):
        self.player1Timer.setText("%02d:%02d" % (self.game.getTimeMinJ1(),
                                                 self.game.getTimeSecJ1()))
        self.player2Timer.setText("%02d:%02d" % (self.game.getTimeMinJ2(),
                                                 self.game.getTimeSecJ2()))

    # Create Player GroupBox
    #   Create the QGroupBox for a player (for the right pannel)
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

    # Create Tools GroupBox
    #   Create the QGroupBox of game's tools (for the right pannel)
    def createToolsGroupBox(self):
        groupBox = QGroupBox("Game Tools")
        groupBox.setFixedSize(300, 200)
        layout = QGridLayout()
        restartBtn = QPushButton("Restart")
        restartBtn.clicked.connect(self.restartGame)
        layout.addWidget(restartBtn, 0, 0, 1, 2)
        groupBox.setLayout(layout)
        return groupBox

    # Get Checkers Plate Widget
    #   Return the Plate
    def getCheckersPlateWidget(self):
        return self.checkersPlateWidget
