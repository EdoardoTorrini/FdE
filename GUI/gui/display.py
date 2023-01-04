from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget
from PyQt6.QtGui import QIcon, QCloseEvent

import pyautogui

from setting import Risks
from read_data import ReadSerial
from widget import MyWidget


class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()

        # configurazione della dialog
        self.setWindowTitle("Parking Sensor")
        self.setWindowIcon(QIcon("img/parking.png"))

        # imposto dimensioni della dialog e la rendo non ridimensionabile
        nWidth, nHeight = pyautogui.size()
        self.setGeometry(int((nWidth / 2) - (630 / 2)), int((nHeight / 2) - (565 / 2)), 266, 256)
        self.setFixedSize(self.size())

        # colori
        self.cWhite = "img/white.png"
        self.cYellow = "img/yellow.png"
        self.cRed = "img/red.png"

        # immagine della macchina
        self.wMainWid = None
        self.initGui(self.cWhite, self.cWhite, self.cWhite)

        self.OLD_STATE = Risks.Outs.value

        self.cRead = ReadSerial(self, "SMT32", "COM5", 115200, 1, 8, bEnLog=True)
        self.cRead.start()

    #   Widget init
    def initGui(self, pLow, pMid, pHigh):

        self.wMainWid = MyWidget(self, pLow, pMid, pHigh)
        t_1 = QGridLayout()
        t_1.addWidget(self.wMainWid, 0, 0)

        wWidget = QWidget()
        wWidget.setLayout(t_1)
        self.setCentralWidget(self.wMainWid)

    def changeColor(self, nVal):

        if self.OLD_STATE != nVal:
            match nVal:
                case Risks.Low.value:
                    self.OLD_STATE = Risks.Low.value
                    self.wMainWid.modifyPixmap(self.cWhite, self.cWhite, self.cYellow)
                case Risks.Medium.value:
                    self.OLD_STATE = Risks.Medium.value
                    self.wMainWid.modifyPixmap(self.cWhite, self.cYellow, self.cRed)
                case Risks.High.value:
                    self.OLD_STATE = Risks.High.value
                    self.wMainWid.modifyPixmap(self.cYellow, self.cRed, self.cRed)
                case Risks.Outs.value:
                    self.OLD_STATE = Risks.Outs.value
                    self.wMainWid.modifyPixmap(self.cWhite, self.cWhite, self.cWhite)
                case _:
                    self.wMainWid.modifyPixmap(self.cWhite, self.cWhite, self.cWhite)
                    print("Match not found")

    def closeEvent(self, a0: QCloseEvent) -> None:

        self.cRead.bStopThread = True




