# encoding=utf-8

import ctypes
import sys
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QTableView, QMainWindow, QMessageBox, \
    QApplication, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from pydash import arrays
from utils import BuildTools, FileTools, DataUtils, UiUtils, HttpTools
from pydash import objects

try:
    ctypes.windll.LoadLibrary('Qt5Core.dll')
except:
    pass

from ui.main import Ui_MainWindow


class MainApp(QMainWindow, Ui_MainWindow):
    data = {}
    listData = []
    filteredData = []
    fields = []
    currentItem = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        UiUtils.initTable(self.tableWidget)
        UiUtils.initParamsTable(self.tableWidget_2)
        UiUtils.initContentTable(self.tableWidget_3)
        self.setFixedSize(self.width(), self.height())  # 禁用最大化、最小化、拉伸

    @pyqtSlot()  # 这个注解在QtCore中
    def on_downloadPushButton_clicked(self):
        url = self.lineEdit.text()
        self.data = HttpTools.http_get(url)
        tags = BuildTools.buildTop(self.data)
        tags = BuildTools.buildChild(self.data, tags)
        self.listData = BuildTools.buildListData(tags)
        self.filteredData = self.listData
        UiUtils.renderApiTableItem(self.tableWidget, self.filteredData)
        # QMessageBox.information(self, '信息', '恭喜您，成功了')

    @pyqtSlot(object)
    def updateTable(self, data):
        print('pyqtSlot - cb', data)

    @pyqtSlot(str)
    def on_searchLineEdit_textChanged(self, str):
        self.filteredData = BuildTools.filter(self.listData, str)
        UiUtils.renderApiTableItem(self.tableWidget, self.filteredData)

    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemClicked(self, item: QTableWidgetItem):
        self.currentItem = self.filteredData[item.row()]
        self.fields = BuildTools.buildFields(self.currentItem, self.data)

        UiUtils.renderParamsTableItem(self.tableWidget_2, objects.get(self.currentItem, 'parameters', []))
        UiUtils.renderContentTableItem(self.tableWidget_3, self.fields)

    @pyqtSlot()
    def on_selectPushButton_clicked(self):
        paramsItems = self.tableWidget_2.selectedIndexes()
        paramsIndexs = DataUtils.getSelectIndexs(paramsItems)
        filedItems = self.tableWidget_3.selectedIndexes()
        filedIndexs = DataUtils.getSelectIndexs(filedItems)

        print(paramsIndexs)
        print(filedIndexs)

        paths = QFileDialog.getExistingDirectory()
        if paths:
            self.lineEdit_2.setText(paths)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec())

# Python  QThread使用多线程方法
