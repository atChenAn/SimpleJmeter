# coding=utf-8
from pydash import objects
import Levenshtein


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


def getSelectIndexs(items, arrWidth=3):
    paramsIndex = []
    for index in range(0, len(items), arrWidth):
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


def convertSelectFields(fields):
    # 获取对应的  Title、keyName即可
    buffer = []
    for item in fields:
        buffer.append({
            'key': objects.get(item, 'key'),
            'title': objects.get(item, 'name.description'),
        })

    return buffer


def convertTimeGroup(filter: list, groups: list):
    tempGroups = []
    delIndex = []

    for group in groups:
        before = filter[group[0]]
        after = filter[group[1]]

        whiteList = ['date', 'time']
        isContinue = 0
        for name in whiteList:
            if name in objects.get(before, 'key', '').lower():
                isContinue = isContinue + 1
            if name in objects.get(after, 'key', '').lower():
                isContinue = isContinue + 1
        if isContinue == 1:
            continue

        # 计算组key 组title
        groupeKey = getNumofCommonSubstr(objects.get(before, 'key', ''), objects.get(after, 'key', ''))
        beforeSecondKey = objects.get(before, 'key', '').replace(groupeKey, '')
        afterSecondKey = objects.get(after, 'key', '').replace(groupeKey, '')
        # 第二次计算有没有相似的keyN内容，只要是黄波的习惯
        secondCommon = getNumofCommonSubstr(beforeSecondKey, afterSecondKey)
        # 如果发现存在相似的字符串，长度超过4的，则拼接上去
        if len(secondCommon) >= 4:
            groupeKey = groupeKey + secondCommon

        # 计算组title
        groupTitle = getNumofCommonSubstr(objects.get(before, 'title', ''), objects.get(after, 'title', ''))
        beforeSecondKey = objects.get(before, 'title', '').replace(groupTitle, '')
        afterSecondKey = objects.get(after, 'title', '').replace(groupTitle, '')
        # 二次计算title
        secondCommon = getNumofCommonSubstr(beforeSecondKey, afterSecondKey)
        if len(secondCommon) >= 2:
            groupTitle = groupTitle + secondCommon

        # 剔除无效部分
        groupTitle = groupTitle.replace('-', '')
        groupTitle = groupTitle.replace(':', '')
        # 插入项目
        tempGroups.append({'key': groupeKey, 'title': groupTitle, 'type': 'long'})
        delIndex.append(group[0])
        delIndex.append(group[1])

    # 删除索引对应的元素
    for index in range(len(filter)):
        if not index in delIndex:
            tempGroups.append(filter[index])

    return tempGroups


def isLikeDate(keyName: str):
    keyDict = ['date', 'time']
    lowerKeyName = keyName.lower()

    for key in keyDict:
        if key in lowerKeyName:
            return True

    return False


def enumSimilarityGroup(data: list, coefficient=0.6, editDistance=8):
    '''
    获取组内相似的字符串索引
    :param data: 字符串组
    :param coefficient: 相似系数 默认0.6 越高越相似
    :param editDistance: 编辑距离 默认8 越低越相似
    :return:
    '''
    groupIndex = []
    for extIndex in range(len(data) - 1):
        for innerIndex in range(extIndex + 1, len(data)):

            if Levenshtein.ratio(data[extIndex], data[innerIndex]) > coefficient:  # 莱文斯坦相似度在 0.6以上的可能为成组出现的元素
                if Levenshtein.jaro(data[extIndex], data[innerIndex]) > coefficient:  # Jaro 相似度 0.6以上
                    if Levenshtein.distance(data[extIndex], data[innerIndex]) <= editDistance:  # 编辑距离在 8 以内的
                        groupIndex.append([extIndex, innerIndex])

    return groupIndex


def getNumofCommonSubstr(str1, str2):
    '''
    获取两个字符串最长公共部分
    :param str1: 字符串1
    :param str2: 字符串2
    :return: 最长的公共部分字符串
    '''
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p]


def isSelectType(item):  # key、title、type

    types = ['integer', 'long', 'number']
    keys = ['type', 'model', 'state', 'status']
    # titles = ['类型','模式','']

    objKey = objects.get(item, 'key').lower()
    objType = objects.get(item, 'type').lower()

    for key in keys:
        if key in objKey and objType in types:
            return True
    return False


def reverse(text):
    return text[::-1]


if __name__ == '__main__':
    str1 = 'From'
    str2 = 'To'

    print(str1)
    print(str2)

    print(getNumofCommonSubstr(str1, str2))
