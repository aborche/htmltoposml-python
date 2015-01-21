#!/usr/bin/python
"""
@author: Kaltashkin Eugene <zhecka@gmail.com>
@original code: Manuel F Martinez <manpaz@bashlinux.com>
@license: BSD
"""

import time

from constants import *
from exceptions import *

class Escpos:
    """ ESC/POS Printer object """
    device    = None

    def charcode(self,code):
        """ Set Character Code Table """
        if code.upper() == "PC437":
            self._raw(CHARCODE_PC437)
        elif code.upper() == "PC850":
            self._raw(CHARCODE_PC850)
        elif code.upper() == "PC860":
            self._raw(CHARCODE_PC860)
        elif code.upper() == "PC863":
            self._raw(CHARCODE_PC863)
        elif code.upper() == "PC865":
            self._raw(CHARCODE_PC865)
        elif code.upper() == "PC858":
            self._raw(CHARCODE_PC858)
        elif code.upper() == "SPACE":
            self._raw(CHARCODE_SPACE)
        else:
            raise CharCode_error()

    def barcode(self, code, bc, width='3', height='162', pos='OFF', font='A'):
        # "1234567","CODE128FSA",162,3,"BELOW","A"
        """ Print Barcode """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        # Height
        if height >=2 or height <=6:
            self._raw(BARCODE_HEIGHT,self.num(height))
        else:
            raise BarcodeSizeError()
        # Width
        if width >= 1 or width <=255:
            self._raw(BARCODE_WIDTH,self.num(width))
#            self._raw("".join([BARCODE_WIDTH,self.num(width)]))
        else:
            raise BarcodeSizeError()
        # Font
        if font.upper() == "B":
            self._raw(BARCODE_FONT_B)
        else: # DEFAULT FONT: A
            self._raw(BARCODE_FONT_A)
        # Position
        if pos.upper() == "OFF":
            self._raw(BARCODE_TXT_OFF)
        elif pos.upper() == "BOTH":
            self._raw(BARCODE_TXT_BTH)
        elif pos.upper() == "ABOVE":
            self._raw(BARCODE_TXT_ABV)
        else:  # DEFAULT POSITION: BELOW 
            self._raw(BARCODE_TXT_BLW)
        # Type 
        if bc.upper() == "UPC-A":
            self.barcodecheck(code,'numberals')
            if len(code) >= 11 and len(code) <= 12:
                self._raw(BARCODE_UPC_A)
            else:
                raise BarcodeLenError('11-12')
        elif bc.upper() == "UPC-E":
            self.barcodecheck(code,'numberals')
            if len(code) >= 11 and len(code) <= 12:
                self._raw(BARCODE_UPC_E)
            else:
                raise BarcodeLenError('11-12')
        elif bc.upper() == "EAN13":
            self.barcodecheck(code,'numberals')
            if len(code) >= 12 and len(code) <= 13:
                self._raw(BARCODE_EAN13)
            else:
                raise BarcodeLenError('12-13')
        elif bc.upper() == "EAN8":
            self.barcodecheck(code,'numberals')
            if len(code) >= 7 and len(code) <= 8:
                self._raw(BARCODE_EAN8)
            else:
                raise BarcodeLenError('7-8')
        elif bc.upper() == "CODE39":
            self.barcodecheck(code,'code39')
            if len(code) >= 1:
                self._raw(BARCODE_CODE39)
            else:
                raise BarcodeLenError('1+')
        elif bc.upper() == "ITF":
            self.barcodecheck(code,'numberals')
            if not len(code) & 1 :
                self._raw(BARCODE_ITF)
            else:
                raise BarcodeLenError('even')
        elif bc.upper() == "CODABAR":
            self.barcodecheck(code,'codabar')
            if len(code) >= 1:
                self._raw(BARCODE_CODABAR)
            else:
                raise BarcodeLenError('1+')
        elif bc.upper() == "CODE93":
            self.barcodecheck(code,'latin1')
            if len(code) >= 1 and len(code) <= 255:
                self._raw(BARCODE_CODE93)
            else:
                raise BarcodeLenError('from 1 to 255')
        elif bc.upper() == "CODE32":
            self.barcodecheck(code,'numberals')
            if len(code) >= 8 and len(code) <= 9:
                self._raw(BARCODE_CODE32)
            else:
                raise BarcodeLenError('8-9')
        elif bc.upper() == "CODE128FSA":
            self.barcodecheck(code,'latin1')
            if len(code) >= 1 and len(code) <= 255:
                self._raw(BARCODE_CODE128FSA)
            else:
                raise BarcodeLenError('from 2 to 255')
        elif bc.upper() == "CODE128FSB":
            self.barcodecheck(code,'latin1')
            if len(code) >= 1 and len(code) <= 255:
                self._raw(BARCODE_CODE128FSB)
            else:
                raise BarcodeLenError('from 2 to 255')
        elif bc.upper() == "CODE128FSC":
            self.barcodecheck(code,'latin1')
            if len(code) >= 1 and len(code) <= 255:
                self._raw(BARCODE_CODE128FSC)
            else:
                raise BarcodeLenError('from 2 to 255')
        else:
            raise BarcodeTypeError()
        # Print Code
        if code:
            self._raw(code,NUL)
        else:
            raise exception.BarcodeCodeError()

    def barcodecheck(self,code,range):
        """ Check code content for Barcodes """
        if range == 'numberals':
            for i in code:
              if i not in BARCODE_FILTER_NUMBER:
                raise NameError("Invalid symbol \'"+i+"\' in barcode "+code+" type 'NUMBER'")
        elif range == 'code39':
            for i in code:
              if i not in BARCODE_FILTER_CODE39:
                raise NameError("Invalid symbol \'"+i+"\' in barcode "+code+" type 'CODE39'")
        elif range == 'codabar':
            for i in code:
              if i not in BARCODE_FILTER_CODABAR:
                raise NameError("Invalid symbol \'"+i+"\' in barcode "+code+" with type 'CODABAR'")
        elif range == 'latin1':
            for i in code:
                if ord(i) < 1 or ord(i) > 127:
                    raise NameError("Invalid symbol \'"+i+"\' in barcode "+code+" with type 'LATIN1'")
                else:
                    pass
        else:
            raise BarcodeRangeError()

    def text(self, txt):
        """ Print alpha-numeric text """
        if txt:
            self._raw(txt)
        else:
            raise TextError()

    def num(self, num):
        """ Print num to chr """
        try:
            return chr(int(num))
        except ValueError:
            return num

    def txtattr(self, cpi='undef', font='undef', bold='undef', underl='undef', underl2='undef', italic='undef', align='undef', size='undef', set='undef', neg='undef', updown='undef', rotate='undef'):
        """ Set text attributes """
        if set.upper() == "RESET":
            # Resetting all text attributes
            self._raw(CTL_LF)
            self._raw(TXT_FONT_A)
            self._raw(TXT_ALIGN_LT)
            self._raw(TXT_CPI_MODE1)
            self._raw(TXT_DEFAULT)
            self._raw(TXT_SIZE_DEFAULT)
            self._raw(TXT_NEG_OFF)
            self._raw(TXT_UPDOWN_OFF)
            self._raw(TXT_ROTATE_OFF)
        else:
            # change defined attributes
            # Align
            if align.upper() == "CENTER":
                self._raw(TXT_ALIGN_CT)
            elif align.upper() == "RIGHT":
                self._raw(TXT_ALIGN_RT)
            elif align.upper() == "LEFT":
                self._raw(TXT_ALIGN_LT)
            # Change font
            if font.upper() != "UNDEF":
                if font.upper() == "A":
                    self._raw(TXT_FONT_A)
                elif font.upper() == "B":
                    self._raw(TXT_FONT_B)
                else:
                    self._raw(TXT_FONT_A)
            # change bold
            if bold.upper() != "UNDEF":
                # off, on
                if bold.upper() == "ON":
                    self._raw(TXT_BOLD_ON)
                else:
                    self._raw(TXT_BOLD_OFF)
            # change underline
            if underl.upper() != "UNDEF":
                # off,single,double
                if underl.upper() == "SINGLE":
                    self._raw(TXT_UNDERL_ON)
                elif underl.upper() == "DOUBLE":
                    self._raw(TXT_UNDERL2_ON)
                else:
                    self._raw(TXT_UNDERL_OFF)
            # change italic
            if italic.upper() != "UNDEF":
                # off, on
                if bold.upper() == "ON":
                    self._raw(TXT_ITALIC_ON)
                else:
                    self._raw(TXT_ITALIC_OFF)
            # change size
            if size.upper() != "UNDEF":
                try:
                    size = int(size,16)
                    self._raw(TXT_SIZE_CUSTOM,self.num(size))
                except ValueError:
                    self._raw(TXT_SIZE_DEFAULT)
                    pass
            # change cpi
            if cpi.upper() != "UNDEF":
                # 0,1,2
                if cpi == '0':
                    self._raw(TXT_CPI_MODE0)
                elif cpi == '1':
                    self._raw(TXT_CPI_MODE1)
                elif cpi == '2':
                    self._raw(TXT_CPI_MODE2)
                else:
                    self._raw(TXT_CPI_MODE1)
            # change negative mode
            if neg.upper() != "UNDEF":
                # off, on
                if neg.upper() == 'ON':
                    self._raw(TXT_NEG_ON)
                else:
                    self._raw(TXT_NEG_OFF)
            # change upside-down mode
            if updown.upper() != "UNDEF":
                # off, on
                if updown.upper() == 'ON':
                    self._raw(TXT_UPDOWN_ON)
                else:
                    self._raw(TXT_UPDOWN_OFF)
            # change rotate mode
            if rotate.upper() != "UNDEF":
                # off, on
                if rotate.upper() == 'ON':
                    self._raw(TXT_ROTATE_ON)
                else:
                    self._raw(TXT_ROTATE_OFF)

    def set(self, density=6, tabpos=8, ptype='rel', posL=0, posH=0, lmarginL=0, lmarginH=0, pwidthH=2, pwidthL=64):
        """ Set text properties """
        # Density
        if density == 0:
            self._raw(PD_N50)
        elif density == 1:
            self._raw(PD_N37)
        elif density == 2:
            self._raw(PD_N25)
        elif density == 3:
            self._raw(PD_N12)
        elif density == 4:
            self._raw(PD_0)
        elif density == 5:
            self._raw(PD_P12)
        elif density == 6:
            self._raw(PD_P25)
        elif density == 7:
            self._raw(PD_P37)
        elif density == 8:
            self._raw(PD_P50)
        else:# DEFAULT: DOES NOTHING
            pass
        # Set tab's position
        if int(tabpos) < 1 or int(tabpos) > 16:
            raise TabError()
        else:
            self._raw(TXT_SET_HT)
            for count in range (1,16):
                self._raw(self.num(int(tabpos)*count))
            self._raw(NUL)
        # Set relative position
        if ptype == 'abs':
            """ absolute position """
            posL = int(posL) & 255
            posH = int(posL) & 255
            print "absolute "+str(posL)+" "+str(posH)
            self._raw(TXT_SET_APOS,self.num(posL),self.num(posH))
        else:
            posL = int(posL) & 255
            posH = int(posH) & 255
            print "relative "+str(posL)+" "+str(posH)
            self._raw(TXT_SET_RPOS,self.num(posL),self.num(posH))
        # Set left margin
        self._raw(TXT_LMARGIN,self.num(lmarginL),self.num(lmarginH))
        self._raw(TXT_PWIDTH,self.num(pwidthL),self.num(pwidthH))
        

    def cut(self, mode='', feed=5):
        """ Cutter control """
        if mode.upper() == "FULL":
#            self._raw("\n\n\n\n\n\n")
            self._raw(PAPER_FULL_CUT)
        elif mode.upper() == "FEED":
            self._raw(PAPER_FEED_CUT,self.num(feed))
        else: # DEFAULT MODE: FULL CUT
#            self._raw("\n\n\n\n\n\n")
            self._raw(PAPER_TOTAL_CUT)
    
    def paper(self, mode=''):
        """ Paper control """
        if mode.upper() == "EJECT":
            self._raw(PAPER_EJECT)
        elif mode.upper() == "OUT":
            self._raw(PAPER_FINAL_EJECT)
        else:
            pass
        
    def printlogo(self,logo=1,xH=0,xL=0,yH=0,yL=0):
        """ print logo from flash bank """
        if logo == 1:
            self._raw(P_LOGO1_PART,self.num(xH),self.num(xL),self.num(yH),self.num(yL))
        elif logo == 2:
            self._raw(P_LOGO2_PART,self.num(xH),self.num(xL),self.num(yH),self.num(yL))
        else:
            pass

#    def cut(self, mode=''):
#        """ Cut paper """
#        # Fix the size between last line and cut
#        # TODO: handle this with a line feed
#        self._raw("\n\n\n\n\n\n")
#        if mode.upper() == "PART":
#            self._raw(PAPER_PART_CUT)
#        else: # DEFAULT MODE: FULL CUT
#            self._raw(PAPER_FULL_CUT)


#    def cashdraw(self, pin):
#        """ Send pulse to kick the cash drawer """
#        if pin == 2:
#            self._raw(CD_KICK_2)
#        elif pin == 5:
#            self._raw(CD_KICK_5)
#        else:
#            raise CashDrawerError()

    def hw(self, hw):
        """ Hardware operations """
        if hw.upper() == "INIT":
            self._raw(HW_INIT)
        elif hw.upper() == "SELECT":
            self._raw(HW_SELECT)
        else: # DEFAULT: DOES NOTHING
            pass


    def control(self, ctl):
        """ Feed control sequences """
        if ctl.upper() == "LF":
            self._raw(CTL_LF)
        elif ctl.upper() == "FF":
            self._raw(CTL_FF)
        elif ctl.upper() == "CR":
            self._raw(CTL_CR)
        elif ctl.upper() == "HT":
            self._raw(CTL_HT)
        elif ctl.upper() == "VT":
            self._raw(CTL_VT)
