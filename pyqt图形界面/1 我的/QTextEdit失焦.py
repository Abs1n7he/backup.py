import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit
class CustomTextEdit(QTextEdit): # 失焦
    def __init__(self, parent=None):
        super(CustomTextEdit, self).__init__(parent)

    def setColor(self):                     # 手动执行
        if self.objectName() == '666':
            x=self.toPlainText().replace('1','2')
            self.setText(x)
            print(x)

    def focusOutEvent(self, event):         # 失焦后执行
        # 在这里编写失焦时想要执行的代码
        super(CustomTextEdit, self).focusOutEvent(event)
        self.setColor()

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.textEdit = CustomTextEdit(self)    # 失焦后执行
        self.textEdit.setObjectName('666')
        self.textEdit.setText('123')
        self.textEdit.setColor()                # 手动执行
        layout.addWidget(self.textEdit)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())