


import sys
from PyQt5.QtWidgets import *


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def NewWindows(self):
        self.new_window = QWidget()
        self.new_window.show()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.button=QPushButton('push',self, clicked=lambda: self.NewWindows())
        layout.addWidget(self.button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ex = Example()
    Ex.show()
    sys.exit(app.exec_())