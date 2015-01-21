# -*- coding: utf8 -*-

from htmltoposml import *
from htmltoposml.constants import *
from htmltoposml.htmltopos import *
from htmltoposml.printer import *

from struct import *
from HTMLParser import HTMLParser

import sys

class UsbPOS(Usb,HTMLtoPOS):
        def __init__(self, **kwargs):
                HTMLtoPOS.__init__(self)
                Usb.__init__(self, **kwargs)

class FilePOS(File,HTMLtoPOS):
        def __init__(self, **kwargs):
                HTMLtoPOS.__init__(self)
                File.__init__(self, **kwargs)

#Custom=UsbPOS(idVendor=0x0dd4,idProduct=0x015d,interface=0,in_ep=0x81,out_ep=0x02)
Custom=FilePOS(devfile="test.file")

welcome_text = u"""
<posml>
<text size=0x11 align=center>Welcome to HTMLtoPosML library</text></center><BR>
<tab>You can use two ways for print data pages to printer.
1. Make page in PosML format and put it to this internal parser
2. Make page step by step in source code of your programm

<text lmargin=80><center><b>What is PosML</b></center>
PosML is modified markup language which inherits tags and properties from \
the same HTML tags, but has some different methods for text formatting

<center>Tags</center>
Text format standalone tags:
        Use closing tag for deactivate mode
        B - bold
        I - italic
        U - underline
        U2 - double underline
        NEG - negative
        ROTATE - Rotate text to 90 degrees
        UPDOWN - Rotate text to 180 degrees
        TAB - Add whitespace
        CENTER - align text to center
        BR - line feed and carriage return
Text format tags with multiple attributes:
        TEXT - Group of text formatting attributes
                SIZE=0x00 # hex value
                # Set size for text
                # Bits 0 to 3 - select character size height
                # Bits 4 to 7 - select character size width
                # Consult constants.py file for example
                CPI=n # decimal value
                # Set Char Per Inch(CPI) mode
                # 0 - Font A = 11 cpi, Font B = 15 cpi
                # 1 - Font A = 15 cpi, Font B = 20 cpi
                # 2 - Font A = 20 cpi, Font A = 15 cpi
                ALIGN=str # string
                # Set text align (LEFT,RIGHT,CENTER)
                # Notice! Align command insert LineFeed symbol before text!
                HT=n # decimal value
                # Set horisontal tab sequence positions
                # Make a table for each next tab element to n position.
                # 0 - reset to default
                PD=n # decimal value
                # Set print density from 0 to 8 (default:6)
                LS=str or n # str or decimal value
                # Set linespacing
                # 1/6 - 1/6 inch
                # 1/8 - 1/8 inch
                # 1 <= n <= 255 (default:64 = 1/6 inch)
                LMARGIN=n # decimal value
                # Set left margin
                # 1 <= n <= 862
        FONT - change font for text
                FACE=str # A or B
                # set internal font for print text
                SIZE=0x00 # hex value
                # see TEXT SIZE command
        BARCODE - print specified type of barcode
                TYPE=str  # barcode type
                # UPC-A, UPC-E, EAN13, EAN8, CODE39, ITF, CODABAR, CODE93, CODE32
                # CODE128FSA - CODE128 font set A
                # CODE128FSB - CODE128 font set B
                # CODE128FSC - CODE128 font set C
                TEXT=str  # barcode text for encoding
                ALIGN=str # barcode text position(ABOVE,BELOW,BOTH,OFF) 
                FONT=str  # A or B (font for barcode text)
                HEIGHT=n  # height of barcode. default: 162
                WIDTH=n   # width of barcode (2-6). default: 3
</posml>
"""

if len(sys.argv) == 1:
        Custom._read_status()
        Custom.feed(welcome_text)
        print welcome_text
else:
        pass
