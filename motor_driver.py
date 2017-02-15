#!/usr/bin/python3
'''
export PYTHONPATH=/home/pi/bt_sync/

'''
import os
import RPi.GPIO as GPIO
from time import sleep

#os.environ["SDL_VIDEODRIVER"] = "dummy"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

print('start')

L293_1A = 18
L293_2A = 23
L293_3A = 24
L293_4A = 25

'''
LEFT_FWD
LEFT_REV
RIGHT_FWD
RIGHT_REV

12    black    yellow    LEFT_REV
GD    white    green     GD
16    brown    RED       
20    green
21    red

21    red    yellow    LEFT_REV
20    green    green    LEFT_FWD
16    brown    red    RIGHT_FWD
GD    white    green    GD
12    black    red    RIGHT_REV

'''
LEFT_REV = 21
LEFT_FWD = 20
RIGHT_FWD = 16
RIGHT_REV = 12
ROVER_OUTS = [LEFT_FWD, LEFT_REV, RIGHT_FWD, RIGHT_REV]


def fwd(sec):
    if sec is None:
        sec = 3
    GPIO.output(RIGHT_FWD, 1)
    GPIO.output(LEFT_FWD, 1)
    # sleep(sec)
    # stop()
    #GPIO.output(RIGHT_FWD, 0)
    #GPIO.output(LEFT_FWD, 0)


def left(sec):
    if sec is None:
        sec = .7
    # Right weels go forward to turn left...
    GPIO.output(RIGHT_FWD, 1)
    #GPIO.output(LEFT_REV, 1)
    # sleep(sec)
    # stop()


def right(sec):
    if sec is None:
        sec = .7

    #GPIO.output(RIGHT_FWD, 1)
    GPIO.output(LEFT_FWD, 1)
    # sleep(sec)
    # stop()


def rev(sec):
    if sec is None:
        sec = 1
    GPIO.output(RIGHT_REV, 1)
    GPIO.output(LEFT_REV, 1)
    # sleep(sec)
    # stop()


def stop():
    # Turn all off
    for o in ROVER_OUTS:
        GPIO.output(o, 0)
# ROVER_OUTS=[L293_1A,L293_2A,L293_3A,L293_4A]

if __name__ == '__main__':

    for o in ROVER_OUTS:
        GPIO.setup(o, GPIO.OUT)
    stop()

    while True:
        try:

            print('Input?')
            i = input().split()
            print('i:', i)
            c = i[0]
            if len(i) > 1:
                t = float(i[1])
            else:
                t = None

            print('c:', c, 't:', t)
            if c in ['f','Up']:
                fwd(t)
            elif c in ['l', 's']:
                left(t)
            elif c == 'r':
                right(t)
            elif c == 'b':
                rev(t)
            elif c == 'e':
                break
            else:
                stop()

            # d=input()
            stop()
        except KeyboardInterrupt:
            stop()
            print('KI')
        except Exception as e:
            # Turn all off
            stop()
            break
            #print('Caught exception', e)
            pass
        finally:
            # stop()
            pass
    stop()

    GPIO.cleanup()
    print('exit')
