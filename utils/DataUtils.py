# coding=utf-8
from pydash import objects


def getValidMethod(obj):
    '''
    获取请求方法的有效方法类型
    :param obj: 请求对象
    :return: 返回有效的请求方法类型名称 或者 None
    '''
    methods = ['get', 'post', 'put', 'delete', 'patch']

    valids = []

    for method in methods:
        if objects.get(obj, method) != None:
            valids.append(method)
    return valids


def getSelectIndexs(items):
    paramsIndex = []
    for index in range(0, len(items), 3):
        paramsIndex.append(items[index].row())
    return paramsIndex


def getSelectFilter(indexs, datas):
    buff = []

    for dtIndex in range(len(datas)):
        for index in indexs:
            if (index == dtIndex):
                buff.append(datas[dtIndex])
    return buff


def convertSelectFilter(filters):
    # 获取对应的  Title、keyName、type即可
    buffer = []
    for item in filters:
        buffer.append({
            'key': objects.get(item, 'name'),
            'title': objects.get(item, 'description'),
            'type': objects.get(item, 'type'),
        })

    return buffer


def isLikeDate(keyName: str):
    keyDict = ['date', 'time']
    lowerKeyName = keyName.lower()

    for key in keyDict:
        if key in lowerKeyName:
            return True

    return False
