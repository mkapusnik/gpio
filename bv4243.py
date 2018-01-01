#!/usr/bin/env python
# -*- coding: CP1252 -*-
#BV4243 Keypad and LCD Class

from notsmb import notSMB
from time import sleep

#commands
PAD_CLEARBUF   = 1
PAD_KEYSINBUF  = 2
PAD_GETKEY     = 3
PAD_ISINBUF    = 4
PAD_SCANCODE   = 5
PAD_GETAVG     = 10
PAD_GETDELTA   = 11
PAD_RESETEEPROM= 20
PAD_SLEEP      = 21
LCD_RESET      = 30
LCD_CMD        = 31
LCD_DATA       = 32
LCD_STRING     = 33
LCD_SIGNON     = 35
LCD_BL         = 36


class BV4243:
    """
    BV4243 Keypad and LCD screen for the Arduino and Rpi, works
    on 3V3 to 5V, depending on the display fittted
    """
    # i2cAdddress is the i2c address of the devce, channel is the channel
    # number 0 for older rpi and 1 for newer
    def __init__(self,i2cAddress,i2cChan):
        self.bus = notSMB(i2cChan)
        self.adr = i2cAddress

    #***************************************************************************
    # K E Y   S E C T I O N
    #---------------------------------------------------------------------------
    # clears the key buffer
    #---------------------------------------------------------------------------
    def clrBuf(self):
        self.bus.i2c(self.adr,[PAD_CLEARBUF],0)

    #---------------------------------------------------------------------------
    # gets number of keys in buffer
    #---------------------------------------------------------------------------
    def keys(self):
        kib=self.bus.i2c(self.adr,[PAD_KEYSINBUF],1)
        return kib[0]

    #---------------------------------------------------------------------------
    # gets the key
    #---------------------------------------------------------------------------
    def key(self):
        kib=self.bus.i2c(self.adr,[PAD_GETKEY],1)
        return kib[0]

    #---------------------------------------------------------------------------
    # see if a particular key is in the buffer
    #---------------------------------------------------------------------------
    def keyInBuf(self,key):
        kib=self.bus.i2c(self.adr,[PAD_ISINBUF,key],1)
        return kib[0]

    #---------------------------------------------------------------------------
    # gets the scancode
    #---------------------------------------------------------------------------
    def scan(self):
        kib=self.bus.i2c(self.adr,[PAD_SCANCODE],1)
        return kib[0]

    #---------------------------------------------------------------------------
    # returns 8 average values as a list
    #---------------------------------------------------------------------------
    def scan(self):
        return self.bus.i2c(self.adr,[PAD_GETAVG],8)

    #---------------------------------------------------------------------------
    # returns 8 delta values as a list
    #---------------------------------------------------------------------------
    def scan(self):
        return self.bus.i2c(self.adr,[PAD_GETDELTA],8)

    #---------------------------------------------------------------------------
    # EEPROM default values reset
    #---------------------------------------------------------------------------
    def eeReset(self):
        self.bus.i2c(self.adr,[PAD_RESETEEPROM],0)

    #---------------------------------------------------------------------------
    # sleep
    #---------------------------------------------------------------------------
    def sleep(self):
        self.bus.i2c(self.adr,[PAD_SLEEP],0)



    #***************************************************************************
    # L C D   S E C T I O N
    #---------------------------------------------------------------------------
    # resets LCD display
    #---------------------------------------------------------------------------
    def lcd_reset(self):
        self.bus.i2c(self.adr,[LCD_RESET],0)
        sleep(0.7)
        
    #---------------------------------------------------------------------------
    # backlight RGB 
    #---------------------------------------------------------------------------
    def bl(self,r,g,b):
       self.bus.i2c(self.adr,[LCD_BL,r,g,b],0)
       
    # The following names match the LiquidCrystal library for the Arduino
    #---------------------------------------------------------------------------
    # clear lcd screen
    #---------------------------------------------------------------------------
    def clear(self):
        self.bus.i2c(self.adr,[LCD_CMD,1],0)

    #---------------------------------------------------------------------------
    # home cursor
    #---------------------------------------------------------------------------
    def lcd_home(self):
       self.bus.i2c(self.adr,[LCD_CMD,2],0)

    #---------------------------------------------------------------------------
    # set cursor, count starts from 1:
    # lines 1 or 2, columns 1 to 16 (for 16x2)
    #---------------------------------------------------------------------------
    def setCursor(self,col,row):
        if row > 2: row = 2
        if col > 16: col = 16
        col -= 1
        if row == 1:
            adr = 0x80+col-1
        else:
            adr = 0xc0+col-1
        self.bus.i2c(self.adr,[LCD_CMD,adr],0)
       
    #---------------------------------------------------------------------------
    # turn cursor on
    #---------------------------------------------------------------------------
    def cursor(self):
        self.bus.i2c(self.adr,[LCD_CMD,0xe],0)

    #---------------------------------------------------------------------------
    # turn cursor off
    #---------------------------------------------------------------------------
    def noCursor(self):
        self.bus.i2c(self.adr,[LCD_CMD,0xc],0)

    #---------------------------------------------------------------------------
    # large cursor
    #---------------------------------------------------------------------------
    def blink(self):
        self.bus.i2c(self.adr,[LCD_CMD,0xd],0)

    #---------------------------------------------------------------------------
    # turn cursor on
    #---------------------------------------------------------------------------
    def noBlink(self):
        self.bus.i2c(self.adr,[LCD_CMD,0xc],0)

    #---------------------------------------------------------------------------
    # turn dislay on
    #---------------------------------------------------------------------------
    def display(self):
        self.bus.i2c(self.adr,[LCD_CMD,0xc],0)

    #---------------------------------------------------------------------------
    # turn dislay off
    #---------------------------------------------------------------------------
    def noDisplay(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x8],0)

    #---------------------------------------------------------------------------
    # scroll left
    #---------------------------------------------------------------------------
    def scrollDisplayLeft(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x18],0)

    #---------------------------------------------------------------------------
    # scroll right
    #---------------------------------------------------------------------------
    def scrollDisplayRight(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x1c],0)

    #---------------------------------------------------------------------------
    # autoscroll 1 line
    #---------------------------------------------------------------------------
    def autoscroll(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x7],0)

    #---------------------------------------------------------------------------
    # autoscroll 1 line
    #---------------------------------------------------------------------------
    def noAutoscroll(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x6],0)

    #---------------------------------------------------------------------------
    # left to right
    #---------------------------------------------------------------------------
    def leftToRight(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x6],0)

    #---------------------------------------------------------------------------
    # right to left
    #---------------------------------------------------------------------------
    def rightToLeft(self):
        self.bus.i2c(self.adr,[LCD_CMD,0x4],0)

    #---------------------------------------------------------------------------
    # create custom char
    #---------------------------------------------------------------------------
    def createChar(self,location, map):
        location &= 7 # 7 locations
        self.bus.i2c(self.adr,[LCD_CMD,0x40 | location << 3],0)
        sleep(0.01)
        for c in map:
            self.bus.i2c(self.adr,[LCD_DATA,c],0)
            sleep(0.01)

    #---------------------------------------------------------------------------
    # prints a string
    #---------------------------------------------------------------------------
    def lcdPrint(self,s):
        for c in s:
            self.bus.i2c(self.adr,[LCD_DATA,ord(c)],0)
