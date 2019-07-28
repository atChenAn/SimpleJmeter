import ctypes
import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from pydash import arrays
from utils import BuildTools, FileTools

try:
    ctypes.windll.LoadLibrary('Qt5Core.dll')
except:
    pass

from ui.main import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        tableTitle = ['request type', 'path', 'description']

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(tableTitle)

    @pyqtSlot()  # 这个注解在QtCore中
    def on_pushButton_clicked(self):
        QMessageBox.information(self, '信息', '恭喜您，成功了')


def renderTableItem(table, tags):
    model = QStandardItemModel(3, 10)

    for index in range(len(tags)):
        model.setItem(index, 0, QStandardItem(tags[index]['name']))

    table.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()

    reader = FileTools.FileReader('./swagger.json')
    data = reader.read()

    tags = BuildTools.buildTop(data)
    tags = BuildTools.buildChild(data, tags)

    win.tableWidget.setRowCount(len(tags))

    renderTableItem(win.tableWidget, tags)

    arrays.mapcat(tags, lambda item: print(item))

    sys.exit(app.exec())
