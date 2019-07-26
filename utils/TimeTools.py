import time


class DateFormat():
    DATE_NORMAL = '%Y-%m-%d %H:%M:%S'
    DATE_NORMAL_NO_SECOND = '%Y-%m-%d %H:%M:%S'
    DATE_TIME = '%H:%M:%S'
    DATE_DATE = '%Y-%m-%d'


def getUnix(hasMillisecond=False):
    '''
    返回本地unix时间戳
    :param hasMillisecond:是否包含毫秒 true返回毫秒级unix  默认false
    :return: unix时间戳 10位(秒) | 13位(毫秒)
    '''
    unix = time.time()
    if hasMillisecond:
        return int(unix * 1000)
    else:
        return int(unix)


def formatDate(unix, formatStr):
    '''
    格式化时间
    :param unix:unix时间戳 10 | 13位
    :param formatStr: 格式化字符串 DateFormat下预定义的和自行定义
    :return: 格式化后的日期/时间字符串
    '''
    unixTemp = unix;

    if unixTemp > 9999999999999:
        raise Exception('时间格式化失败：unix 值过大')

    if (unixTemp > 9999999999):
        unixTemp = int(unixTemp / 1000)

    timeGroup = time.localtime(unixTemp)
    timeStr = time.strftime(formatStr, timeGroup)
    return timeStr


def getNowTimeStr(format=DateFormat.DATE_NORMAL):
    '''
    获取当前时间
    :param format:格式化字符串，默认为普通格式
    :return: 当前时间字符串
    '''
    unix = getUnix();
    return formatDate(unix, format)
