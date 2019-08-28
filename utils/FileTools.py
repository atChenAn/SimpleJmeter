import os
import pydash
from utils import LogTools

sysLog = LogTools.SysLogs()


class FileReader:
    file = None

    def __init__(self, fileName, model=None):
        try:
            self.file = open(fileName, model or 'r', encoding='UTF-8')
        except Exception as e:
            print('IO异常')
            sysLog.info('IO异常：' + e.__str__())

    def moveToBegin(self):
        if not pydash.predicates.is_none(self.file):
            self.file.seek(0)

    def read(self, len=None):
        try:
            if not pydash.predicates.is_none(self.file):
                if pydash.predicates.is_none(len):
                    return self.file.read()
                return self.file.read(len)
        except Exception as e:
            sysLog.info('IO异常：' + e.__str__())

    def write(self, data):
        try:
            if not pydash.predicates.is_none(self.file):
                self.file.write(data)
        except Exception as e:
            sysLog.info('IO异常：' + e.__str__())

    def close(self):
        if not pydash.predicates.is_none(self.file):
            self.file.flush()
            self.file.close()


def readFile(path):
    if os.path.exists(path) and os.path.isfile(path):
        fileReader = FileReader(path)
        data = fileReader.read()
        fileReader.close()
        return data
    else:
        sysLog.info('读取文件失败：文件不存在或者path指定的路径是文件夹：' + path)


def writeFile(path, data):
    try:
        fileReader = FileReader(path, 'w')
        fileReader.write(data)
        fileReader.close()
    except Exception as e:
        sysLog.info('文件写出失败：' + e)


if __name__ == '__main__':
    reader = FileReader('./log/2019-07-28.log')
    print(reader.read())
    reader.close()
