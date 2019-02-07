import signal
import time


def timeout_handler(num, stack):
    print("Received SIGALRM")
    raise Exception("FUBAR")


def long_function():
    print("LEEEEROYYY JENKINSSSSS!!!")
    time.sleep(60)


signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)

try:
    print("Before: %s" % time.strftime("%M:%S"))
    long_function()
except Exception as ex:
    # if "FUBAR" in ex:
    #     print("Gotcha!")
    # else:
    #     print("We're gonna need a bigger boat!")
    print(ex)
finally:
    signal.alarm(0)
    print("After: %s" % time.strftime("%M:%S"))