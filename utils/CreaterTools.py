import sys
import os
from utils import FileTools, TplEnum

runPath = sys.path[0]

tplPaths = {
    'formTpl': runPath + os.sep + 'tpl' + os.sep + 'FilterForm.tsx',
    'inputTpl': runPath + os.sep + 'tpl' + os.sep + 'Input.tsx',
    'optionTpl': runPath + os.sep + 'tpl' + os.sep + 'Option.tsx',
    'selectTpl': runPath + os.sep + 'tpl' + os.sep + 'Select.tsx',
    'timeRange': runPath + os.sep + 'tpl' + os.sep + 'TimeRange.tsx',
}


def generateFilterForm(filters: list, path: str):
    fileName = path + os.sep + 'FilterForm.tsx'

    filterFormTpl = FileTools.readFile(tplPaths['formTpl'])

    filtersContent = generateParams(filters)

    filterFormTpl = filterFormTpl.replace(TplEnum.REPLACE_FORM_CONTENT, filtersContent)

    print(fileName)
    print(filterFormTpl)

    FileTools.writeFile(fileName, filterFormTpl)


def generateParams(filters: list):
    paramsStr = ''

    for item in filters:
        if item['type'] == 'string':
            paramsStr = paramsStr + generateInput(item)

    return paramsStr


def generateInput(item):
    tpl = FileTools.readFile(tplPaths['inputTpl'])
    tpl = tpl.replace(TplEnum.REPLACE_TITLE, item['keyName'])
    tpl = tpl.replace(TplEnum.REPLACE_KEY_NAME, item['title'])
    tpl = tpl.replace(TplEnum.REPLACE_HINT, '请输入' + item['keyName'])
    return tpl
