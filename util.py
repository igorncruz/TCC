import datetime, time


def getFormattedDatetimeWithMillisec(timestamp=''):
    if (timestamp == ''):
        timestamp = time.time()

    return datetime.datetime.fromtimestamp(timestamp).strftime(
        '%Y-%m-%d %H:%M:%S.%f')[:-3]


def getFormattedDateTimeFromSeconds(toSeconds, fromTimestamp=''):
    if (fromTimestamp == ''):
        fromTimestamp = time.time()

    toSeconds = toSeconds + fromTimestamp
    return datetime.datetime.fromtimestamp(toSeconds).strftime(
        '%Y-%m-%d %H:%M:%S')


def nowStr():
    return str(datetime.datetime.now())


def addSecs(tms, secs):
    fulldate = datetime.datetime.fromtimestamp(tms)
    # datetime.timedelta(0, self.__maxTimeInSecBetweenPackages)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate


def main():
    a = addSecs(time.time(), 300)
    b = addSecs(a.timestamp(), 300)
    print(a)
    print(b)


if __name__ == '__main__':
    main()