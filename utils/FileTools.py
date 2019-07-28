import os
import pydash
from utils import LogTools

sysLog = LogTools.SysLogs()


class FileReader:
    file = None

    def __init__(self, fileName):
        try:
            self.file = open(fileName)
        except Exception:
            print('IO异常')

    def moveToBegin(self):
        if not pydash.predicates.is_none(self.file):
            self.file.seek(0)

    def read(self, len=None):

        if not pydash.predicates.is_none(self.file):
            if pydash.predicates.is_none(len):
                return self.file.read()
            return self.file.read(len)

    def close(self):
        if not pydash.predicates.is_none(self.file):
            self.file.close()


def readFile(path):
    if os.path.exists(path) and os.path.isfile(path):
        fileReader = FileReader(path)
        return fileReader.read()
    else:
        sysLog.info('读取文件失败：文件不存在或者path指定的路径是文件夹')


if __name__ == '__main__':
    reader = FileReader('./log/2019-07-28.log')
    print(reader.read())
    reader.close()
