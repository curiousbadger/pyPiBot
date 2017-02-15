#!/usr/bin/python3
'''
Created on Jul 20, 2016

@author: charper
export PYTHONPATH=/home/pi/bt_sync/
'''
import socketserver
LISTEN_PORT = 6889
from robo.rover import Rover
import os
import RPi.GPIO as GPIO
from time import sleep


rov = Rover()
fwd = rov.fwd
rev = rov.rev
# left=rov.left
stop = rov.stop
lc = None


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            # print('loop')
            self.data = self.request.recv(1024)
            if not self.data:
                print('DISCONNECTED')
                break
            #print('RECEIVED: ' + str(self.data))
            # self.request.sendall(str(self.data)[::-1].encode('utf-8'))
            t = .1
            c = str(self.data, encoding='utf-8')

#             print('type(self.data)', type(self.data))
#             print('c,t', c, t)
#             print('type(c)', type(c))
            if c in ['w', 'f']:
                fwd(t)
            elif c in ['l', 'a']:
                rov.left()
            elif c in ['r', 'd']:
                rov.right()
            elif c in ['s', 'b']:
                rev(t)
            elif c == 'e':
                stop()
                raise Exception('Custom exit')
                break
            elif c == 'stop':
                stop()
            else:
                stop()


if __name__ == '__main__':

    print('Start')

    print('listening')
    server = socketserver.TCPServer(('0.0.0.0', LISTEN_PORT), MyTCPHandler)
    server.allow_reuse_address = True
    while True:
        try:
            server.serve_forever()

        except KeyboardInterrupt:
            print('KEYBOARD INTERUPT!!!')
            stop()
            GPIO.cleanup()
            server.server_close()
            server.shutdown()
            exit(0)

        except ConnectionResetError:
            stop()
            server.server_close()
            server.shutdown()

        except Exception as e:
            stop()
            GPIO.cleanup()
            server.server_close()
            server.shutdown()
            exit(0)
        finally:
            server.shutdown()
    # server.server_close()
    server.shutdown()
    GPIO.cleanup()
    # less ~/btsync/pyRPI_LCD/motor_server.py
    # python3 ~/btsync/pyRPI_LCD/motor_server.py

'''
#os.environ["SDL_VIDEODRIVER"] = "dummy"


L293_1A = 18
L293_2A = 23
L293_3A = 24
L293_4A = 25

LEFT_REV = 20
LEFT_FWD = 16
RIGHT_FWD = 21
RIGHT_REV = 12
ROVER_OUTS = [LEFT_FWD, LEFT_REV, RIGHT_FWD, RIGHT_REV]


def fwd(sec):

    if sec is None:
        sec = .1
    print('fwd:', sec)
    GPIO.output(RIGHT_FWD, 1)
    GPIO.output(LEFT_FWD, 1)
    # sleep(sec)
    # stop()
    #GPIO.output(RIGHT_FWD, 0)
    #GPIO.output(LEFT_FWD, 0)


def left(sec):
    if sec is None:
        sec = .7
    #GPIO.output(RIGHT_FWD, 1)
    GPIO.output(LEFT_FWD, 1)

    sleep(sec)
    stop()


def right(sec):
    if sec is None:
        sec = .7

    GPIO.output(RIGHT_FWD, 1)
    #GPIO.output(LEFT_REV, 1)
    sleep(sec)
    stop()


def rev(sec):
    if sec is None:
        sec = 1
    GPIO.output(RIGHT_REV, 1)
    GPIO.output(LEFT_REV, 1)
    sleep(sec)
    stop()


def stop():
    # Turn all off
    for o in ROVER_OUTS:
        GPIO.output(o, 0)
# ROVER_OUTS=[L293_1A,L293_2A,L293_3A,L293_4A]
'''
