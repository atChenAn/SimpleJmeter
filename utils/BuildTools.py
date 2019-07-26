import pydash


def buildTop(data):
    '''
    构建swagger顶层目录结构
    :param data: swagger原始返回的信息
    :return:返回顶层元组信息
    '''
    tags = pydash.objects.get(data, 'tags', [])
    tops = pydash.arrays.mapcat(tags, lambda item: item)
    tops = pydash.arrays.compact(tops)

    return tops;
