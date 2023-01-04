from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QPixmap


class MyWidget(QWidget):

    def __init__(self, cFather,
                 pLow="img/white.png", pMid="img/white.png", pHigh="img/white.png"):

        super(MyWidget, self).__init__()

        self.cFather = cFather
        self.white = None
        self.white_mid = None
        self.white_high = None

        self.initGui(pLow, pMid, pHigh)

        # imposto la grandezza del widget
        self.setGeometry(0, 0, 500, 256)
        self.setFixedSize(self.size())

    def initGui(self, pLow, pMid, pHigh):

        t_1 = QGridLayout()

        pic = QLabel()
        pic.setPixmap(QPixmap("img/car.png"))
        t_1.addWidget(pic, 0, 0)

        # prima banda
        self.white = QLabel()
        self.white.setPixmap(QPixmap(pLow))
        t_1.addWidget(self.white, 1, 0)

        # seconda banda
        self.white_mid = QLabel()
        self.white_mid.setPixmap(QPixmap(pMid))
        t_1.addWidget(self.white_mid, 2, 0)

        # terza banda
        self.white_high = QLabel()
        self.white_high.setPixmap(QPixmap(pHigh))
        t_1.addWidget(self.white_high, 3, 0)

        self.setLayout(t_1)

    def modifyPixmap(self, pLow, pMid, pHigh):

        self.white.setPixmap(QPixmap(pLow))
        self.white_mid.setPixmap(QPixmap(pMid))
        self.white_high.setPixmap(QPixmap(pHigh))



