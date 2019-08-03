# encoding=utf-8

import ctypes
import os
import sys
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QTableView, QMainWindow, QMessageBox, \
    QApplication, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5 import QtCore
from pydash import arrays
from utils import BuildTools, FileTools, DataUtils, UiUtils, HttpTools, LogTools, CreaterTools
from pydash import objects
import configparser
import base64

try:
    ctypes.windll.LoadLibrary('Qt5Core.dll')
except:
    pass

from ui.main import Ui_MainWindow

configPath = sys.path[0] + os.sep + 'ui-cache.ini'


class MainApp(QMainWindow, Ui_MainWindow):
    data = {}  # 原始 JSON数据
    listData = []  # 全部Api列表数据
    filteredData = []  # 筛选之后的Api 列表数据
    currentItem = None  # 当前选中的Api项目
    fields = []  # Content list数据
    params = []  # 参数列表数据

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        UiUtils.initTable(self.tableWidget)
        UiUtils.initParamsTable(self.tableWidget_2)
        UiUtils.initContentTable(self.tableWidget_3)
        self.setFixedSize(self.width(), self.height())  # 禁用最大化、最小化、拉伸

        config = configparser.ConfigParser()
        config.read(configPath, encoding='utf-8')
        try:
            if config.has_option('UI', 'url'):
                T = config.get('UI', 'url')
                self.lineEdit.setText(base64.b64decode(T).decode('utf-8'))
            if config.has_option('UI', 'savepath'):
                T = config.get('UI', 'savepath')
                self.lineEdit_2.setText(base64.b64decode(T).decode('utf-8'))
        except:
            print('未读取到配置')

    @pyqtSlot()  # 这个注解在QtCore中
    def on_downloadPushButton_clicked(self):
        url = self.lineEdit.text()
        self.data = HttpTools.http_get(url)
        tags = BuildTools.buildTop(self.data)
        tags = BuildTools.buildChild(self.data, tags)
        self.listData = BuildTools.buildListData(tags)
        self.filteredData = self.listData
        UiUtils.renderApiTableItem(self.tableWidget, self.filteredData)

        config = configparser.ConfigParser()
        config.read(configPath, encoding='utf-8')
        if not config.has_section('UI'):
            config.add_section('UI')
        try:
            config.write(open(configPath, 'w'))
        except Exception as e:
            print(e)
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
        self.params = objects.get(self.currentItem, 'parameters', [])

        UiUtils.renderParamsTableItem(self.tableWidget_2, objects.get(self.currentItem, 'parameters', []))
        UiUtils.renderContentTableItem(self.tableWidget_3, self.fields)

    @pyqtSlot()
    def on_selectPushButton_clicked(self):
        paths = QFileDialog.getExistingDirectory()
        if paths:
            self.lineEdit_2.setText(paths)

            config = configparser.ConfigParser()
            config.read(configPath, encoding='utf-8')
            if not config.has_section('UI'):
                config.add_section('UI')
            try:
                config.set('UI', 'savepath', base64.b64encode(paths.encode('utf-8')).decode('utf-8'))
                config.write(open(configPath, 'w'))
            except Exception as e:
                print(e)

    @pyqtSlot()
    def on_runPushButton_clicked(self):

        # 生成查询参数部分的Form表单TSX
        paramsItems = self.tableWidget_2.selectedIndexes()
        paramsIndexs = DataUtils.getSelectIndexs(paramsItems)
        filteredData = DataUtils.getSelectFilter(paramsIndexs, self.params)
        filteredData = DataUtils.convertSelectFilter(filteredData)
        CreaterTools.generateFilterForm(filteredData, self.lineEdit_2.text())

        # 生成TableContent的TSX
        # filedItems = self.tableWidget_3.selectedIndexes()
        # filedIndexs = DataUtils.getSelectIndexs(filedItems)

        QMessageBox.information(self, '成功', '生成完毕！')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec())

# Python  QThread使用多线程方法
