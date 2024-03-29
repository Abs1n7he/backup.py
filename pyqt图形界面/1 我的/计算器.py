import sys
import re
import os
import json
import time
import requests
import urllib
import urllib3
urllib3.disable_warnings()
from PyQt5.QtGui import QIcon,QTextCharFormat
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,pyqtSlot, QMetaObject

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("计算器")
        self.setFixedSize(300, 350)  # 固定窗口大小

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout()
        central_widget.setLayout(main_layout)

        # 添加文本框
        self.screen = QLineEdit()
        self.screen.setFixedHeight(40)
        self.screen.setAlignment(Qt.AlignRight)
        self.screen.setReadOnly(True)
        main_layout.addWidget(self.screen, 0, 0, 1, 4)

        # 添加按钮
        button_1 = QPushButton("1", clicked=lambda: self.button_click("1"))
        button_2 = QPushButton("2", clicked=lambda: self.button_click("2"))
        button_3 = QPushButton("3", clicked=lambda: self.button_click("3"))
        button_4 = QPushButton("4", clicked=lambda: self.button_click("4"))
        button_5 = QPushButton("5", clicked=lambda: self.button_click("5"))
        button_6 = QPushButton("6", clicked=lambda: self.button_click("6"))
        button_7 = QPushButton("7", clicked=lambda: self.button_click("7"))
        button_8 = QPushButton("8", clicked=lambda: self.button_click("8"))
        button_9 = QPushButton("9", clicked=lambda: self.button_click("9"))
        button_0 = QPushButton("0", clicked=lambda: self.button_click("0"))
        button_add = QPushButton("+", clicked=self.button_add)
        button_subtract = QPushButton("-", clicked=self.button_subtract)
        button_multiply = QPushButton("*", clicked=self.button_multiply)
        button_divide = QPushButton("/", clicked=self.button_divide)
        button_clear = QPushButton("清除", clicked=self.button_clear)
        button_equal = QPushButton("=", clicked=self.button_equal)

        main_layout.addWidget(button_7, 1, 0)
        main_layout.addWidget(button_8, 1, 1)
        main_layout.addWidget(button_9, 1, 2)
        main_layout.addWidget(button_divide, 1, 3)

        main_layout.addWidget(button_4, 2, 0)
        main_layout.addWidget(button_5, 2, 1)
        main_layout.addWidget(button_6, 2, 2)
        main_layout.addWidget(button_multiply, 2, 3)

        main_layout.addWidget(button_1, 3, 0)
        main_layout.addWidget(button_2, 3, 1)
        main_layout.addWidget(button_3, 3, 2)
        main_layout.addWidget(button_subtract, 3, 3)

        main_layout.addWidget(button_0, 4, 0)
        main_layout.addWidget(button_clear, 4, 1, 1, 2)
        main_layout.addWidget(button_add, 4, 3)

        main_layout.addWidget(button_equal, 5, 0, 1, 4)

        # 初始化变量
        self.first_num = None
        self.operation = None
        self.show()

    def button_click(self, number):
        current = self.screen.text()
        self.screen.setText(current + number)

    def button_clear(self):
        self.screen.clear()
        self.first_num = None
        self.operation = None

    def button_add(self):
        self.first_num = float(self.screen.text())
        self.screen.clear()
        self.operation = "add"

    def button_subtract(self):
        self.first_num = float(self.screen.text())
        self.screen.clear()
        self.operation = "subtract"

    def button_multiply(self):#+
        self.first_num = float(self.screen.text())
        self.screen.clear()
        self.operation = "multiply"

    def button_divide(self):
        self.first_num = float(self.screen.text())
        self.screen.clear()
        self.operation = "divide"

    def button_equal(self): #=
        second_num = float(self.screen.text())
        self.screen.clear()

        if self.operation == "add":
            result = self.first_num + second_num
        elif self.operation == "subtract":
            result = self.first_num - second_num
        elif self.operation == "multiply":
            result = self.first_num * second_num
        elif self.operation == "divide":
            if second_num == 0:
                result = "除数不能为 0"
            else:
                result = self.first_num / second_num

        self.screen.setText(str(result))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Calculator()
    sys.exit(app.exec_())