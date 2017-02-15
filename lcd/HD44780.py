#!/usr/bin/python3

from __future__ import print_function

'''
HD44780
pins_db:      pins_db[0] -> DB0
            pins_db[1] -> DB1 etc...
3.3 driven transistor
https://www.fairchildsemi.com/datasheets/TI/TIP122.pdf
'''
import sys
import RPi.GPIO as GPIO
from time import sleep


class HD44780:

    def __init__(self, pin_rs=24, pin_e=23, pins_db=[4, 17, 21, 22], pin_rw=18):

        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pin_rw = pin_rw
        

        self.pins_db = pins_db
        self.rpins_db = list(reversed(pins_db))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.pin_rw, GPIO.OUT)

        # self.clear()
        # sleep(1)
        # self.message('init')
        self.initialize()

    def DB7(self):
        return self.pins_db[-1]

    def busy_wait(self):
        '''TODO: Probably unnecessary '''
#         if GPIO.gpio_function(self.DB7() == GPIO.OUT):
#             GPIO
        GPIO.output(self.pin_rw, True)
        GPIO.output(self.pin_e, True)
        GPIO.setup(self.pins_db[-1], GPIO.IN)
        while GPIO.input(self.pins_db[-1]) == 1:
            print('busy')
            pass
        GPIO.output(self.pin_e, False)
        GPIO.setup(self.pins_db[-1], GPIO.OUT)
        GPIO.output(self.pin_rw, False)

    def clear_display(self):
        '''Clear Display 0x01 '''
        self.nibble(0x0)
        self.pulse_E()
        self.nibble(0x1)
        self.pulse_E()

        # self.busy_wait()
        sleep(0.0152)

    def return_home(self):
        '''Return Home 0000 001X '''
        self.nibble(0x0)
        self.pulse_E()
        self.nibble(0b0010)
        self.pulse_E()
        sleep(0.0152)

    def clear(self):
        """ Blank / Reset LCD """
        '0011 0011'
        self.cmd(0x33)  # $33 8-bit mode

        '0011 0010'
        self.cmd(0x32)  # $32 8-bit mode

        '''0010 1000
                NFXX
        '''
        self.cmd(0x28)  # $28 8-bit mode
        '''
        0000 1100
             1DCB
        '''
        self.cmd(0x0C)  # $0C 8-bit mode
        '''
        0000 0110
             01ID
        '''
        self.cmd(0x06)  # $06 8-bit mode
        ''' Clear display '''
        self.cmd(0x01)  # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        sleep(0.001)
        bits = bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4, 8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i - 4], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def initialize(self):

        GPIO.output(self.pin_rs, False)
        self.nibble(0x3)
        self.pulse_E()
        sleep(0.005)
        self.nibble(0x3)
        self.pulse_E()

        self.nibble(0x3)
        self.pulse_E()
        # 2 -> 4bit, 3 -> 8bit
        self.nibble(0x2)
        self.pulse_E()

        '''
        Set lines, font high nib:
        0|0|1|0
        Low nib:
        N Number of lines|F Font Size, 0 -> 5x8|X|X
        '''
        self.nibble(0x2)
        self.pulse_E()
        self.nibble(0b1000)
        self.pulse_E()

        '''
        Entry mode set
        High command nib:
        0|0|0|0
        Low nib:
        0|1|I/D Increment->1|S Shift NO shift -> 0
        '''
        self.nibble(0)
        self.pulse_E()
        self.nibble(0b0110)
        self.pulse_E()

        '''
        X|Display ON|Cursor ON|Blink ON
        '''
        self.nibble(0)
        self.pulse_E()
        self.nibble(0b1111)
        self.pulse_E()
        sleep(0.001)

    def pulse_E(self):
        #GPIO.output(self.pin_e, False)
        GPIO.output(self.pin_e, True)
        # 1 clock cycle ~ 4 microseconds
        sleep(0.000005)
        GPIO.output(self.pin_e, False)
        sleep(0.000050)

    def nibble(self, n, char_mode=False):
        # sleep(0.001)
        #m = []
        # print(n)
        # convert to ASCII string of 0's and 1's
        bs = bin(n)[2:].zfill(4)
        b = []
        for i in bs:
            b.append(True if i == '1' else False)

        GPIO.output(self.pin_rs, char_mode)

        for pin, bit in enumerate(b):
            #print(pin, bit, self.rpins_db[pin])
            GPIO.output(self.rpins_db[pin], bit)

    def write_char(self, c):
        oc = ord(c)
        hn = (oc & 0xF0) >> 4
        ln = oc & 0x0F
        #print(c, hex(oc), bin(hn), bin(ln))
        self.nibble(hn, True)
        self.pulse_E()
        self.nibble(ln, True)
        self.pulse_E()
        sleep(0.000038)

    def message(self, text, old=False):
        """ Send string to LCD. Newline wraps to second line"""

        for char in text:
            if char == '\n':
                self.cmd(0xC0)  # next line
            else:
                if old:
                    self.cmd(ord(char), True)
                else:
                    self.write_char(char)

    def fmt_message(self, m):
        ml = [l[:20] for l in m.split('\n')]
        ml[1], ml[2] = ml[2], ml[1]
        # lcd.return_home()
        for l in ml:
            self.message(l)





if __name__ == '__main__':

    print('GPIO.getmode()', GPIO.getmode())
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, 0)

    lcd = HD44780()
    lcd.clear_display()
    # lcd.write_char('a')
    lcd.clear_display()
    lcd.fmt_message(
        "aaaaaaaaaaaaaaaaaaaa\nbbbbbbbbbbbbbbbbbbbb\ncccccccccccccccccccc\nddddddddddddddddddddd")
    sleep(1)
    lcd.clear_display()
    lcd.message('007', False)
    lcd.message('foobar', False)
    if len(sys.argv) > 1:
        lcd.message(sys.argv[1])
    lcd.return_home()
    print('foo')
    
    