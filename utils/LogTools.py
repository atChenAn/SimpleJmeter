import sys
from utils import TimeTools


class SysLogs:
    LogLevel = {
        'ERROR': 0,
        'WARN': 1,
        'INFO': 2,
        'DEBUG': 3,
    }

    logLevel = 3  # 0 错误 1 警告 2 信息 3 开发
    logPath = sys.path[0] + '\\log\\' + TimeTools.getNowTimeStr(TimeTools.DateFormat.DATE_DATE) + '.log'

    def __init__(self, level=3, logPath=None):
        self.setLevel(level)
        if (logPath):
            self.setLogPath(logPath)

    def setLevel(self, level):
        if level < 0 or level > 3:
            raise Exception('日至等级设置错误：请设置[0-3]区间内的整数，包含边界')
        self.logLevel = level

    def setLogPath(self, path):
        self.logPath = path

    def info(self, msg):
        self.__writeFile(self.LogLevel['INFO'], msg)

    def debug(self, msg):
        self.__writeFile(self.LogLevel['DEBUG'], msg)

    def warn(self, msg):
        self.__writeFile(self.LogLevel['WARN'], msg)

    def error(self, msg):
        self.__writeFile(self.LogLevel['ERROR'], msg)

    def __writeFile(self, level, content):
        levelStrs = ['ERROR', 'WARN', 'INFO', 'DEBUG']
        if level > self.logLevel:
            return

        timeStr = levelStrs[level] + ' ' + TimeTools.getNowTimeStr() + ' ' + content
        # 打开文件流写出log
        try:
            print(self.logPath)
            fileObj = open(r'E:\\SimpleJmeter\\utils\\log\\2019-07-26.log', 'w+')
            # fileObj.write(timeStr)
            # fileObj.flush()
            # fileObj.close()
        except:
            print('日志写出失败：文件IO操作发生异常')


if __name__ == '__main__':
    syslog = SysLogs()
    syslog.debug('这是一条debug信息')
    # syslog.info('这是一条info信息')
    # syslog.warn('这是一条warn信息')
    # syslog.error('这是一条error信息')
