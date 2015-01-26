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
                ALIGNLF=str # string
                # ON = add LF before!!! align text(Default is ON)
                # OFF = turn off LF before align text
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
                PWIDTH=n # decimal value
                # Set print width
                # 1 <= n <= 862
        FONT - change font for text
                FACE=str # A or B
                # set internal font for print text
                SIZE=0x00 # hex value
                # see TEXT SIZE command

Special functions:
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
        LOGO - print logo from internal flash
                BANK=n # logo bank number
                START=n # start line in logo bitmap
                LENGTH=n # number of lines which need to be printed
</posml>
"""
object_method= u"""
Custom.hw()
        'INIT': Init printer
        'SELECT': Select printer

Custom.control()
        'LF': Print data, feed one line
        'FF': Print data, cuts the paper and presents the ticket
        'CR': When autofeed is "CR enabled", this command functions in the same way as 'LF',
              otherwise it is disregarded
        'HT': Horisontal tabulation
        'VT': Vertical tabulation for 4 lines

Custom.paper()
        'EJECT': Eject ticket
        'OUT': Final ticket cut and eject

Custom.cut()
        'FULL': Full cut paper
        'FEED': Partial cut paper and feed 5 lines
        '': Paper total cut

Custom.txtattr()
        # ex. Custom.txtattr(align="left", font="B", italic="on")
        # attribute values must be included to " or '
        set="reset": Reset all text settings
        align="left|right|center": Text align
        cpi="0|1|2": Set char per inch
        size='xy': set font size(hex)
        font="A|B": Set text font
        bold="on|off": Bold text
        underl="single|double|off": Underline
        italic="on|off": Italic
        neg="on|off": Negative
        updown="on|off": Rotate 180 degrees
        rotate="on|off": Rotate 90 degrees

Custom.set()
        # Custom.set(lmargin=100)
        # set some settings cpi or position
        # attribute values must be used without " or '
        density=n: from 0 to 8
        tabpos=n: set tab position array
        ptype="abs|rel": relative and absolute position
        pos=n: position value
        lmargin=n: Left margin value
        pwidth=n: Print area width

Custom.charcode()
        "PC437":
        "PC850":
        "PC860":
        "PC863":
        "PC865":
        "PC858":
        "SPACE":

Custom.barcode()
        # redefine barcode struct!
        # Custom.barcodestruct['TEXT']="TEXT"
        # Custom.barcodestruct['CODE']="BARCODETYPE"
        # Custom.barcodestruct['WIDTH']=3
        # Custom.barcodestruct['HEIGHT']=162
        # Custom.barcodestruct['FONT']='A'
        # Custom.barcodestruct['POS']='ABOVE'
        # For Reset barcodestruct
        # Custom.barcodestruct = BARCODESTRUCT
        FONT='A|B': set barcode text font
        POS="OFF|ABOVE|BELOW|BOTH": barcode text position
        WIDTH=n: barcode width(default:3)
        HEIGHT=n: barcode height(default:162)
        TEXT='barcodetext': Barcode string
        CODE="UPC-A|UPC-E|EAN13|EAN8|CODE39|ITF|CODABAR|CODE93|CODE32|CODE128FSA|CODE128FSB|CODE128FSC": barcode type

Custom.text("some text")

Custom.printlogo()
        logo=1|2: select flash logo
        start=n : start line in logo bitmap
        length=n: number of lines which need to be printed
        
Custom.image('image filename')
"""

txtdemopos = """
from htmltoposml import *
from htmltoposml.constants import *
from htmltoposml.htmltopos import *
from htmltoposml.printer import *

from struct import *
from HTMLParser import HTMLParser

import sys

class FilePOS(File,HTMLtoPOS):
        def __init__(self, **kwargs):
                HTMLtoPOS.__init__(self)
                File.__init__(self, **kwargs)
                self.barcodestruct=BARCODESTRUCT

Custom=FilePOS(devfile="test.file")

str='''<font size=0x22><center>Test Page</center></font>
<tab><b>This is a test message printed
from htmltopos python library.</b>
<LOGO BANK=1 START=0 LENGTH=240>
<BARCODE CODE='CODE128FSB' TEXT="HTMLtoPosML" POS="BOTH">
'''

Custom.hw('INIT')
Custom.cut('TOTAL')
Custom.paper('OUT')
Custom.feed(str)
Custom.text('\\n\\n\\n\\n\\n\\n')
Custom.cut('TOTAL')
Custom.paper('OUT')
Custom.control('FF')

"""
txtdemoobj = """
from htmltoposml import *
from htmltoposml.constants import *
from htmltoposml.htmltopos import *
from htmltoposml.printer import *

from struct import *
from HTMLParser import HTMLParser

import sys

class FilePOS(File,HTMLtoPOS):
        def __init__(self, **kwargs):
                HTMLtoPOS.__init__(self)
                File.__init__(self, **kwargs)
                self.barcodestruct=BARCODESTRUCT

Custom=FilePOS(devfile="test.file")

Custom.hw('INIT')
Custom.cut('TOTAL')
Custom.paper('OUT')
Custom.txtattr(align="center",size='10')
Custom.text('HTMLtoPosML demo')
Custom.control('LF')
Custom.txtattr(size='12',bold="on")
Custom.text('Bold text with custom size')
Custom.control('LF')
Custom.txtattr(size='11',bold="off",font="B",align='left')
Custom.set(lmargin=90)
Custom.text('Left margin=90, Bold off, Font B')
Custom.control('LF')
Custom.txtattr(set='reset')
Custom.text('Just simple text with default settings')
Custom.control('LF')
Custom.printlogo(logo=1,start=0,length=250)
Custom.barcodestruct['CODE']='CODE128FSA'
Custom.barcodestruct['TEXT']='CODE128FSA'
Custom.barcodeprint()
Custom.text('\\n\\n\\n\\n\\n\\n')
Custom.cut('TOTAL')
Custom.paper('OUT')
Custom.control('FF')

"""

if len(sys.argv) == 1:
        name = str(sys.argv[0])
        help = u"""
        python scrname posml - PosML command set
        python scrname object - POS Object command set
        python scrname status - Get printer status(USB,COM,NET)
        python scrname txtdemopos - Print PosML democode
        python scrname txtdemoobj - Print Object democode
        """
        print help.replace("scrname",name)
#        Custom.feed(welcome_text)
else:
        if sys.argv[1].upper() == 'POSML':
                print welcome_text
        elif sys.argv[1].upper() == 'OBJECT':
                print object_method
        elif sys.argv[1].upper() == 'STATUS':
                Custom._read_status()
        elif sys.argv[1].upper() == 'TXTDEMOPOS':
                print txtdemopos
        elif sys.argv[1].upper() == 'TXTDEMOOBJ':
                print txtdemoobj
        else:
                pass
