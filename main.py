# import ctypes
# import sys
# from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
# from PyQt5.QtCore import *
# from PyQt5 import QtCore
#
# try:
#     ctypes.windll.LoadLibrary('Qt5Core.dll')
# except:
#     pass
#
#
#
#
# from ui.main import Ui_MainWindow
#
#
# class Main(QMainWindow, Ui_MainWindow):
#
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#     @pyqtSlot()  # 这个注解在QtCore中
#     def on_pushButton_clicked(self):
#         QMessageBox.information(self, '信息', '恭喜您，成功了')
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = Main()
#     win.show()
#
#     sys.exit(app.exec())
#
#

from utils import BuildTools

if __name__ == '__main__':


