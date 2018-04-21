import datetime, time

def getFormattedDatetimeWithMillisec(timestamp = ''):
	if (timestamp == ''):
		timestamp = time.time()

	return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def main():
	a = getFormattedDatetimeWithMillisec()
	print(a)

if __name__ == '__main__':
    main()