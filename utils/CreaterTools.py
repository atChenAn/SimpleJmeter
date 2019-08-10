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


def generateManage(path: str, filters, apiItem):
    fileName = path + os.sep + 'Manage.tsx'

    contentTpl = FileTools.readFile(tplPaths['manage'])

    # 寻找filter中时间组索引
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

    keyMaps = []
    # 生成相似的索引组与实际formkey关联结构
    # 建立formKey与filterKey的对应关系
    keyMaps = DataUtils.buildMaps(tempList, filters)

    # 循环构建替换代码
    timeTpl = ''
    for formKey in keyMaps:
        tempKey = keyMaps[formKey][0].lower()
        if 'to' in tempKey or 'end' in tempKey:
            timeTpl += 'filterDump.' + keyMaps[formKey][
                1] + '= getValue(filterDump,\'' + formKey + '.startTime\',undefined);'
            timeTpl += 'filterDump.' + keyMaps[formKey][0] + '= getValue(filterDump,\'' + formKey + '.endTime\',undefined);'
        else:
            timeTpl += 'filterDump.' + keyMaps[formKey][
                0] + '= getValue(filterDump,\'' + formKey + '.startTime\',undefined);'
            timeTpl += 'filterDump.' + keyMaps[formKey][1] + '= getValue(filterDump,\'' + formKey + '.endTime\',undefined);'

        timeTpl += 'delete filterDump.' + formKey + ';'

    print(timeTpl)

    # filter.contractStartDate = filter.signDate && filter.signDate.startTime;
    #   filter.contractEndDate = filter.signDate && filter.signDate.endTime;

    # 执行替换

    # 寻找分页参数

    # 执行替换

    # # Manage 筛选条件部分替换
    # REPLACE_MANAGE_FILTER = '##REPLACE_MANAGE_FILTER##'
    # # Manage api导出名称
    # REPLACE_MANAGE_API = '##REPLACE_MANAGE_API##'
    # # Manage api 方法名称
    # REPLACE_MANAGE_API_METHOD = '##REPLACE_MANAGE_API_METHOD##'
    # # 分页参数 - 页 no
    # MANAGE_PAGE_NO = '##MANAGE_PAGE_NO##'
    # # 分页参数 - 页 size
    # MANAGE_PAGE_SIZE = '##MANAGE_PAGE_SIZE##'

    contentTpl = DataUtils.replaceManageTpl(contentTpl, filter, apiItem, timeTpl)

    FileTools.writeFile(fileName, contentTpl)

    contentTpl = PrettierTools.format(fileName)

    FileTools.writeFile(fileName, contentTpl)
