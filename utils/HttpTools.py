# coding=utf-8

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from urllib import request, parse


class Http(QThread):
    signal = pyqtSignal(object)  # 括号里填写信号传递的参数

    # init 初始化部分
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self.signal.emit()

    # ============================================ 拦截器相关部分的代码 ============================================ #
    # 添加拦截器
    def __addInterceptor(self, interceptor, fn):
        '''
        私有方法，添加拦截器响应函数
        :param interceptor: 将要操作的拦截器集合
        :param fn: 添加的拦截器响应函数
        :return: None
        '''
        interceptor.append(fn)
        return interceptor.__len__() - 1

    # 移除拦截器
    def __removeInterceptor(self, interceptor, index):
        '''
        移除已经存在的拦截器
        :param interceptor: 将要操作的拦截器集合
        :param index: 此参数可以为添加拦截器时返回的index或者拦截器响应函数本身
        :return: None
        '''
        try:
            if isinstance(index, int):
                if index < interceptor.__len__():
                    interceptor.remove(interceptor[index])
            else:
                interceptor.remove(index)
        except Exception:
            print('remove interceptor failed,because can not find it')

    # 添加请求拦截器
    def addRequestInterceptor(self, fn):
        '''
        添加请求拦截器，将在发起请求前进行调用
        :param fn: 拦截请求响应函数
        :return:
        '''
        return self.__addInterceptor(self.requestInterceptor, fn)

    # 移除请求拦截器
    def removeRequestInterceptor(self, index):
        '''
        移除请求拦截器
        :param index: 下标或拦截响应函数本身
        :return:
        '''
        self.__removeInterceptor(self.requestInterceptor, index)

    # 添加响应拦截器
    def addResponseInterceptor(self, fn):
        '''
        添加响应拦截器，将在响应后调用
        :param fn: 拦截响应响应函数
        :return:
        '''
        return self.__addInterceptor(self.responseInterceptor, fn)

    # 移除响应拦截器
    def removeResponseInterceptor(self, index):
        '''
        移除响应函数
        :param index: 下标或响应函数本身
        :return:
        '''
        self.__removeInterceptor(self.responseInterceptor, index)

    # ============================================ 拦截器相关部分的代码 ============================================ #

    def http_get(self, path, params={}):
        print('http_get')
        queryStr = '?%s' % parse.urlencode(params)
        # 如果没有查询条件就清空queryStr
        if queryStr == '?':
            queryStr = ''

        response = requests.get('https://' + path + queryStr)
        response.encoding = 'utf-8'
        buffer = response.text;
        print(buffer)
        return buffer;


# 请求拦截器、静态成员
Http.requestInterceptor = []
# 响应拦截器、静态成员
Http.responseInterceptor = []


def http_get(path, params={}):
    print('http_get')
    queryStr = '?%s' % parse.urlencode(params)
    # 如果没有查询条件就清空queryStr
    if queryStr == '?':
        queryStr = ''

    response = requests.get(path + queryStr)
    response.encoding = 'utf-8'
    buffer = response.text;
    print(buffer)
    return buffer;


if __name__ == '__main__':
    data = http_get('http://www.baidu.com')
    print(data)
