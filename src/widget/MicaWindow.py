from win32mica import ApplyMica, MicaTheme, MicaStyle
from PyQt5 import QtWidgets, QtCore
import sys


class MicaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 300, 200)
        ApplyMica(self.winId(), MicaTheme.LIGHT, MicaStyle.ALT)
        self.setContentsMargins(0, 0, 0, 0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MicaWindow()
    window.show()
    sys.exit(app.exec_())
