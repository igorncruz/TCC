import datetime, time

def getFormattedDatetimeWithMillisec(timestamp = ''):
    if (timestamp == ''):
        timestamp = time.time()

    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def getFormattedDateTimeFromSeconds(toSeconds, fromTimestamp=''):
	if (fromTimestamp == ''):
		fromTimestamp = time.time()

	toSeconds = toSeconds + fromTimestamp
	return datetime.datetime.fromtimestamp(toSeconds).strftime('%Y-%m-%d %H:%M:%S')


def main():
    a = getFormattedDateTimeFromSeconds(60)
    print(a)

if __name__ == '__main__':
    main()