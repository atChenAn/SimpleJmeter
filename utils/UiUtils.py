# coding=utf-8
from utils import BuildTools
from pydash import objects
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QAbstractItemView, QTableView, QMainWindow, QMessageBox, \
    QApplication, QTableWidget


def initTable(table):
    tableTitle = ['请求类型', 'path', '描述']
    table.setColumnCount(3)  # 设置列数
    table.setHorizontalHeaderLabels(tableTitle)  # 设置表头
    table.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
    table.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置单行选中
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面


def initParamsTable(table: QTableWidget):
    tableTitle = ['keyName', '名称', '必须']
    table.setColumnCount(3)  # 设置列数
    table.setHorizontalHeaderLabels(tableTitle)  # 设置表头
    # table.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
    table.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置单行选中
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面


def initContentTable(table: QTableWidget):
    tableTitle = ['keyName', '名称']
    table.setColumnCount(2)  # 设置列数
    table.setHorizontalHeaderLabels(tableTitle)  # 设置表头
    # table.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
    table.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置单行选中
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面


def renderApiTableItem(table: QTableWidget, listData):
    table.setRowCount(len(listData))
    for rowIndex in range(len(listData)):
        rowData = listData[rowIndex]

        methodTypeItem = QTableWidgetItem(objects.get(rowData, 'type', '--'))
        pathItem = QTableWidgetItem(objects.get(rowData, 'path', '--'))
        descItem = QTableWidgetItem(objects.get(rowData, 'summary', '--'))
        table.setItem(rowIndex, 0, methodTypeItem)
        table.setItem(rowIndex, 1, pathItem)
        table.setItem(rowIndex, 2, descItem)


def renderParamsTableItem(table: QTableWidget, params):
    table.setRowCount(len(params))
    for rowIndex in range(len(params)):
        rowData = params[rowIndex]

        methodTypeItem = QTableWidgetItem(objects.get(rowData, 'name', '--'))
        pathItem = QTableWidgetItem(objects.get(rowData, 'description', '--'))
        descItem = QTableWidgetItem(str(objects.get(rowData, 'required', '--')))
        table.setItem(rowIndex, 0, methodTypeItem)
        table.setItem(rowIndex, 1, pathItem)
        table.setItem(rowIndex, 2, descItem)


def renderContentTableItem(table: QTableWidget, apiItem, tags):
    fields = BuildTools.buildFields(apiItem, tags)

    table.setRowCount(len(fields))
    for rowIndex in range(len(fields)):
        rowData = fields[rowIndex]

        methodTypeItem = QTableWidgetItem(objects.get(rowData, 'key', '--'))
        pathItem = QTableWidgetItem(objects.get(rowData, 'name', '--'))
        table.setItem(rowIndex, 0, methodTypeItem)
        table.setItem(rowIndex, 1, pathItem)
