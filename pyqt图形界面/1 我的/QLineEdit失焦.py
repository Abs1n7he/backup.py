import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.editingFinished.connect(lambda: self.setColor(self.lineEdit))
        layout.addWidget(self.lineEdit)


        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.editingFinished.connect(lambda: self.setColor(self.lineEdit2))
        layout.addWidget(self.lineEdit2)



    def setColor(self,lineEdit):
        print(lineEdit.text())
        #eval(lineEdit+".setText("+lineEdit+".text().replace('1','2'))")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())