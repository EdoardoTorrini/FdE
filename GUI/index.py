
from PyQt6.QtWidgets import QApplication
from display import MyWindow
import sys

app = QApplication(sys.argv)

try:

    window = MyWindow()
    window.show()

    app.exec()

except KeyboardInterrupt:
    print("Interruzione Programma")

except Exception as sVal:
    print(sVal)
