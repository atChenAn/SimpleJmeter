import sys
import os
from utils import FileTools, TplEnum, DataUtils, PrettierTools

runPath = sys.path[0]

tplPaths = {
    'formTpl': runPath + os.sep + 'tpl' + os.sep + 'FilterForm.tsx',
    'inputTpl': runPath + os.sep + 'tpl' + os.sep + 'Input.tsx',
    'optionTpl': runPath + os.sep + 'tpl' + os.sep + 'Option.tsx',
    'selectTpl': runPath + os.sep + 'tpl' + os.sep + 'Select.tsx',
    'timeRange': runPath + os.sep + 'tpl' + os.sep + 'TimeRange.tsx',
}


def generateFilterForm(filters: list, path: str):
    fileName = path + os.altsep + 'FilterForm.tsx'

    filterFormTpl = FileTools.readFile(tplPaths['formTpl'])

    filtersContent = generateParams(filters)

    filterFormTpl = filterFormTpl.replace(TplEnum.REPLACE_FORM_CONTENT, filtersContent)

    FileTools.writeFile(fileName, filterFormTpl)

    filterFormTpl = PrettierTools.format(fileName)

    FileTools.writeFile(fileName, filterFormTpl)


def generateParams(filters: list):
    paramsStr = ''

    for item in filters:
        if item['type'] == 'string':
            paramsStr = paramsStr + generateInput(item)
        if item['type'] in ['integer', 'long', 'number'] and DataUtils.isLikeDate(item['key']):
            paramsStr = paramsStr + generateDate(item)

    return paramsStr


def generateInput(item):
    tpl = FileTools.readFile(tplPaths['inputTpl'])
    tpl = tpl.replace(TplEnum.REPLACE_TITLE, item['title'])
    tpl = tpl.replace(TplEnum.REPLACE_KEY_NAME, item['key'])
    tpl = tpl.replace(TplEnum.REPLACE_HINT, '请输入' + item['title'])
    return tpl


def generateDate(item):
    tpl = FileTools.readFile(tplPaths['timeRange'])
    tpl = tpl.replace(TplEnum.REPLACE_TITLE, item['title'])
    tpl = tpl.replace(TplEnum.REPLACE_KEY_NAME, item['key'])
    tpl = tpl.replace(TplEnum.REPLACE_HINT, '请输入' + item['title'])
    return tpl
