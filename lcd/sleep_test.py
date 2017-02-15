#!/usr/bin/python3
import time as ttime
from time import time, sleep, clock, localtime
import sys
print('Start', time())

num_micro=10
if len(sys.argv)>1:
    num_micro=float(sys.argv[1])
print('num_micro', num_micro)
sleep_time=num_micro * (10 ** -6)


start_time=time()
sleep(sleep_time)
stop_time=time()

delta=(stop_time-start_time) * (10 ** 6)

print('delta', delta)
error=abs(num_micro-delta)
print('error', error)
print('Done', time())

