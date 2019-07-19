import sys
from urllib import request


class A:
    def Hello(self):
        print('Hello')


def sayHello(name):
    '''
    sayHello
    :param name:名字
    :return:
    '''
    print('Hello,' + name)


def main():
    responseData = request.urlopen('http://192.168.2.11/djc-gateway/platform/time')
    print(responseData.read().decode('utf-8'))


if __name__ == '__main__':
    main()
