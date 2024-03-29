import sys
from PyQt5.QtWidgets import *


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(int(app.desktop().screenGeometry(0).width() * 0.9),int(app.desktop().screenGeometry(0).height() * 0.8))
        # app.desktop().width()                     是整个屏幕的长度，包括多屏幕
        # app.desktop().screenGeometry(0).width()   第一个屏幕的长度





if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ex = Example()
    Ex.show()
    sys.exit(app.exec_())