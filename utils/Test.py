import difflib
# import jieba
import Levenshtein

str1 = "我的骨骼雪白 也长不出青稞"
str2 = "雪的日子 我只想到雪中去si"

# 1. difflib
seq = difflib.SequenceMatcher(None, str1, str2)
ratio = seq.ratio()

# difflib 去掉列表中不需要比较的字符
seq = difflib.SequenceMatcher(lambda x: x in ' 我的雪', str1, str2)
ratio = seq.ratio()

# 2. hamming距离，str1和str2长度必须一致，描述两个等长字串之间对应位置上不同字符的个数
# sim = Levenshtein.hamming(str1, str2)
# print 'hamming similarity: ', sim


# 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
sim = Levenshtein.distance('changeDateFrom', 'signDateTo')


# # 4.计算莱文斯坦比
# sim = Levenshtein.ratio(str1, str2)
# print('Levenshtein.ratio similarity: ', sim)
#
# # 5.计算jaro距离
# sim = Levenshtein.jaro(str1, str2)
# print('Levenshtein.jaro similarity: ', sim)
#
# # 6. Jaro–Winkler距离
# sim = Levenshtein.jaro_winkler(str1, str2)
# print('Levenshtein.jaro_winkler similarity: ', sim)

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


keys1 = ['payNo', 'projectName', 'budgetId', 'budgetName', 'payDateFrom', 'payDateTo', 'providerId', 'providerName']

groups = enumSimilarityGroup(keys1)

print(groups)


def getNumofCommonSubstr(str1, str2):
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
    return str1[p - maxNum:p], maxNum


if __name__ == '__main__':
    s1 = 'projectName'
    s2 = 'projectId'
    res = getNumofCommonSubstr(s1, s2)
    print(res)
