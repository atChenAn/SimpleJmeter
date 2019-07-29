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
