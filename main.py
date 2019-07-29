# encoding=utf-8

import ctypes
import sys
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QTableView, QMainWindow, QMessageBox, \
    QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from pydash import arrays
from utils import BuildTools, FileTools, DataUtils, UiUtils, HttpTools

try:
    ctypes.windll.LoadLibrary('Qt5Core.dll')
except:
    pass

from ui.main import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    listData = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        UiUtils.initTable(self.tableWidget)
        self.setFixedSize(self.width(), self.height())  # 禁用最大化、最小化、拉伸

    @pyqtSlot()  # 这个注解在QtCore中
    def on_downloadPushButton_clicked(self):
        url = self.lineEdit.text()
        self.http_thred = HttpTools.Http(url)
        self.http_thred.run()
        # reader = FileTools.FileReader('./swagger.json')
        # data = reader.read()
        # tags = BuildTools.buildTop(data)
        # tags = BuildTools.buildChild(data, tags)
        # self.listData = BuildTools.buildListData(tags)
        # UiUtils.renderTableItem(self.tableWidget, self.listData)
        # QMessageBox.information(self, '信息', '恭喜您，成功了')

    @pyqtSlot(object)
    def updateTable(self, data):

    @pyqtSlot(str)
    def on_searchLineEdit_textChanged(self, str):
        filterData = BuildTools.filter(self.listData, str)
        UiUtils.renderTableItem(self.tableWidget, filterData)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec())
