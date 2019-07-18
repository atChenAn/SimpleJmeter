import sys


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
    sayHello('Jack')

    buff = []

    buff.append('Hello')
    buff.append('Jack')

    tempObj = A();

    buff.append(tempObj)

    print(buff.__len__())

    buff.remove(tempObj)

    print(buff.__len__())


if __name__ == '__main__':
    main()
