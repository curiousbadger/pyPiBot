#!/usr/bin/python3
'''
Created on Jul 20, 2016

@author: charper
export PYTHONPATH=/home/pi/bt_sync/
'''
import socket
import threading
LISTEN_PORT = 6889


def readData():
    while True:
        data = s.recv(1024)
        if data:
            print('Received: ' + data.decode('utf-8'))


def sendData():
    while True:
        print('Input?')
        intxt = input()
        s.send(intxt.encode('utf-8'))


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.0.0.9', LISTEN_PORT))

    t1 = threading.Thread(target=readData)
    t1.start()
    t2 = threading.Thread(target=sendData)
    t2.start()
