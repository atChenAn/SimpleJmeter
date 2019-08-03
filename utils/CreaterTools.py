import sys
import os
import math
from pydash import objects
from utils import FileTools, TplEnum, DataUtils, PrettierTools

runPath = sys.path[0]

tplPaths = {
    'formTpl': runPath + os.sep + 'tpl' + os.sep + 'FilterForm.tsx',
    'inputTpl': runPath + os.sep + 'tpl' + os.sep + 'Input.tsx',
    'optionTpl': runPath + os.sep + 'tpl' + os.sep + 'Option.tsx',
    'selectTpl': runPath + os.sep + 'tpl' + os.sep + 'Select.tsx',
    'timeRange': runPath + os.sep + 'tpl' + os.sep + 'TimeRange.tsx',
    'content': runPath + os.sep + 'tpl' + os.sep + 'Content.tsx',
    'content-item': runPath + os.sep + 'tpl' + os.sep + 'ContentItem.tsx',
}


def generateFilterForm(filters: list, path: str):
    fileName = path + os.sep + 'FilterForm.tsx'

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
        elif item['type'] in ['integer', 'long', 'number'] and DataUtils.isLikeDate(item['key']):
            paramsStr = paramsStr + generateDate(item)
        elif item['type'] in ['integer', 'long', 'number']:
            paramsStr = paramsStr + generateInput(item)

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


def generateContent(fields: list, path: str):
    fileName = path + os.sep + 'Content.tsx'

    contentTpl = FileTools.readFile(tplPaths['content'])

    filtersContent = generateContentItem(fields)

    contentTpl = contentTpl.replace(TplEnum.REPLACE_CONTENT_ITEMS, filtersContent)

    FileTools.writeFile(fileName, contentTpl)

    contentTpl = PrettierTools.format(fileName)

    FileTools.writeFile(fileName, contentTpl)


def generateContentItem(fields: list):
    itemStr = ''
    width = math.floor(100 / fields.__len__())
    itemTpl = FileTools.readFile(tplPaths['content-item'])

    for field in fields:
        T = itemTpl.replace(TplEnum.REPLACE_ITEM_TITLE, objects.get(field, 'title'))
        T = T.replace(TplEnum.REPLACE_ITEM_KEY, objects.get(field, 'key'))
        T = T.replace(TplEnum.REPLACE_ITEM_WIDTH, str(width) + "%")
        itemStr = itemStr + T

    return itemStr
