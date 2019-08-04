import sys
import os
import math
from pydash import objects, arrays
from utils import FileTools, TplEnum, DataUtils, PrettierTools

runPath = sys.path[0]

tplRoot = runPath + os.sep + 'tpl' + os.sep

tplPaths = {
    'formTpl': tplRoot + 'FilterForm.tsx',
    'inputTpl': tplRoot + 'Input.tsx',
    'optionTpl': tplRoot + 'Option.tsx',
    'selectTpl': tplRoot + 'Select.tsx',
    'timeRange': tplRoot + 'TimeRange.tsx',
    'content': tplRoot + 'Content.tsx',
    'content-item': tplRoot + 'ContentItem.tsx',
    'manage': tplRoot + 'Manage.tsx',
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

    # 转换成字符组
    strList = arrays.mapcat(filters, lambda item: item['key'])

    # 获取相似indexsGroup
    indexs = DataUtils.enumSimilarityGroup(strList)

    # 遍历group，查看是不是时间字段，如果是则将indexGroup存下来 [[1,2],[4,5]]
    tempList = []
    for index in range(len(indexs)):
        key = strList[indexs[index][0]].lower()
        if 'time' in key or 'date' in key:
            tempList.append(indexs[index])

    tarList = DataUtils.convertTimeGroup(filters, tempList)

    # 将groupIndex每组最后一个元素记下 [2,5]
    # tempList = arrays.mapcat(tempList, lambda item: item[1])

    # 构建新的list
    # tarList = []
    # for index in range(len(filters)):
    #     if not index in tempList:
    #         tarList.append(filters[index])

    for item in tarList:
        # 输入类型
        if item['type'] == 'string':
            paramsStr = paramsStr + generateInput(item)
        # 时间类型
        elif item['type'] in ['integer', 'long', 'number'] and DataUtils.isLikeDate(item['key']):
            paramsStr = paramsStr + generateDate(item)
        # select 类型
        elif DataUtils.isSelectType(item):
            paramsStr = paramsStr + generateSelect(item)
        # 未知类型，均按照input进行渲染
        else:
            paramsStr = paramsStr + generateInput(item)

    return paramsStr


def generateInput(item):
    tpl = FileTools.readFile(tplPaths['inputTpl'])
    tpl = tpl.replace(TplEnum.REPLACE_TITLE, objects.get(item, 'title', 'UNDEFINED'))
    tpl = tpl.replace(TplEnum.REPLACE_KEY_NAME, objects.get(item, 'key', 'UNDEFINED'))
    tpl = tpl.replace(TplEnum.REPLACE_HINT, '请输入' + objects.get(item, 'title', 'UNDEFINED'))
    return tpl


def generateDate(item):
    tpl = FileTools.readFile(tplPaths['timeRange'])
    tpl = tpl.replace(TplEnum.REPLACE_TITLE, objects.get(item, 'title', ''))
    tpl = tpl.replace(TplEnum.REPLACE_KEY_NAME, objects.get(item, 'key', ''))
    tpl = tpl.replace(TplEnum.REPLACE_HINT, '请输入' + objects.get(item, 'title', ''))
    return tpl


def generateSelect(item):
    tpl = FileTools.readFile(tplPaths['selectTpl'])
    tpl = tpl.replace(TplEnum.REPLACE_TITLE, objects.get(item, 'title', 'UNDEFINED'))
    tpl = tpl.replace(TplEnum.REPLACE_KEY_NAME, objects.get(item, 'key', 'UNDEFINED'))
    tpl = tpl.replace(TplEnum.REPLACE_HINT, '请输入' + objects.get(item, 'title', 'UNDEFINED'))
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


def generateManage(path: str):
    fileName = path + os.sep + 'Manage.tsx'

    contentTpl = FileTools.readFile(tplPaths['manage'])

    # contentTpl = contentTpl.replace(TplEnum.REPLACE_CONTENT_ITEMS, filtersContent)

    FileTools.writeFile(fileName, contentTpl)

    contentTpl = PrettierTools.format(fileName)

    FileTools.writeFile(fileName, contentTpl)
