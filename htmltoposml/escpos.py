#!/usr/bin/python
"""
@author: Kaltashkin Eugene <zhecka@gmail.com>
@original code: Manuel F Martinez <manpaz@bashlinux.com>
@license: BSD
"""

import time

from constants import *
from exceptions import *
from struct import pack

try:
    import Image
except ImportError:
    from PIL import Image

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

    def barcodeprint(self):#, *codestruct):
        """ Print Barcode """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        #
        # Height
        if self.barcodestruct['HEIGHT'] >=2 or self.barcodestruct['HEIGHT'] <=6:
            self._raw(BARCODE_HEIGHT,self.num(self.barcodestruct['HEIGHT']))
        else:
            self._raw(BARCODE_HEIGHT,self.num(3))
        # Width
        if self.barcodestruct['WIDTH'] >= 1 or self.barcodestruct['WIDTH'] <=255:
            self._raw(BARCODE_WIDTH,self.num(self.barcodestruct['WIDTH']))
        else:
            self._raw(BARCODE_WIDTH,self.num(162))
        # Font
        if self.barcodestruct['FONT'].upper() == "B":
            self._raw(BARCODE_FONT_B)
        else: # DEFAULT FONT: A
            self._raw(BARCODE_FONT_A)
        # Position
        if self.barcodestruct['POS'].upper() == "OFF":
            self._raw(BARCODE_TXT_OFF)
        elif self.barcodestruct['POS'].upper() == "BOTH":
            self._raw(BARCODE_TXT_BTH)
        elif self.barcodestruct['POS'].upper() == "ABOVE":
            self._raw(BARCODE_TXT_ABV)
        else:  # DEFAULT POSITION: BELOW 
            self._raw(BARCODE_TXT_BLW)
        # Type 
        barcodelen=len(self.barcodestruct['TEXT'])
        if self.barcodestruct['CODE'].upper() == "UPC-A":
            self.barcodecheck(self.barcodestruct['TEXT'],'numberals')
            if barcodelen >= 11 and barcodelen <= 12:
                self._raw(BARCODE_UPC_A)
            else:
                raise BarcodeLenError('11-12')
        elif self.barcodestruct['CODE'].upper() == "UPC-E":
            self.barcodecheck(self.barcodestruct['TEXT'],'numberals')
            if barcodelen >= 11 and barcodelen <= 12:
                self._raw(BARCODE_UPC_E)
            else:
                raise BarcodeLenError('11-12')
        elif self.barcodestruct['CODE'].upper() == "EAN13":
            self.barcodecheck(self.barcodestruct['TEXT'],'numberals')
            if barcodelen >= 12 and barcodelen <= 13:
                self._raw(BARCODE_EAN13)
            else:
                raise BarcodeLenError('12-13')
        elif self.barcodestruct['CODE'].upper() == "EAN8":
            self.barcodecheck(self.barcodestruct['TEXT'],'numberals')
            if barcodelen >= 7 and barcodelen <= 8:
                self._raw(BARCODE_EAN8)
            else:
                raise BarcodeLenError('7-8')
        elif self.barcodestruct['CODE'].upper() == "CODE39":
            self.barcodecheck(self.barcodestruct['TEXT'],'code39')
            if barcodelen >= 1:
                self._raw(BARCODE_CODE39)
            else:
                raise BarcodeLenError('1+')
        elif self.barcodestruct['CODE'].upper() == "ITF":
            self.barcodecheck(self.barcodestruct['TEXT'],'numberals')
            if not barcodelen & 1 :
                self._raw(BARCODE_ITF)
            else:
                raise BarcodeLenError('even')
        elif self.barcodestruct['CODE'].upper() == "CODABAR":
            self.barcodecheck(self.barcodestruct['TEXT'],'codabar')
            if barcodelen >= 1:
                self._raw(BARCODE_CODABAR)
            else:
                raise BarcodeLenError('1+')
        elif self.barcodestruct['CODE'].upper() == "CODE93":
            self.barcodecheck(self.barcodestruct['TEXT'],'latin1')
            if barcodelen >= 1 and barcodelen <= 255:
                self._raw(BARCODE_CODE93)
            else:
                raise BarcodeLenError('from 1 to 255')
        elif self.barcodestruct['CODE'].upper() == "CODE32":
            self.barcodecheck(self.barcodestruct['TEXT'],'numberals')
            if barcodelen >= 8 and barcodelen <= 9:
                self._raw(BARCODE_CODE32)
            else:
                raise BarcodeLenError('8-9')
        elif self.barcodestruct['CODE'].upper() == "CODE128FSA":
            self.barcodecheck(self.barcodestruct['TEXT'],'latin1')
            if barcodelen >= 1 and barcodelen <= 255:
                self._raw(BARCODE_CODE128FSA)
            else:
                raise BarcodeLenError('from 2 to 255')
        elif self.barcodestruct['CODE'].upper() == "CODE128FSB":
            self.barcodecheck(self.barcodestruct['TEXT'],'latin1')
            if barcodelen >= 1 and barcodelen <= 255:
                self._raw(BARCODE_CODE128FSB)
            else:
                raise BarcodeLenError('from 2 to 255')
        elif self.barcodestruct['CODE'].upper() == "CODE128FSC":
            self.barcodecheck(self.barcodestruct['TEXT'],'latin1')
            if barcodelen >= 1 and barcodelen <= 255:
                self._raw(BARCODE_CODE128FSC)
            else:
                raise BarcodeLenError('from 2 to 255')
        else:
            raise BarcodeTypeError()
        # Print Code
        if self.barcodestruct['TEXT'] != '':
            self._raw(self.barcodestruct['TEXT'],NUL)
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

    def set(self, density=6, tabpos=8, ptype='rel', pos=0, lmargin=0, pwidth=576):
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
        # Set position
        if ptype == 'abs':
            """ absolute position """
            self._raw(TXT_SET_APOS,pack('<h',int(pos)))
        else:
            """ absolute position """
            self._raw(TXT_SET_RPOS,pack('<h',int(pos)))
        # Set left margin
        self._raw(TXT_LMARGIN,pack('<h', int(lmargin)))
         #self.num(lmarginL),self.num(lmarginH))
        self._raw(TXT_PWIDTH,pack('<h', int(pwidth)))
        

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
        
    def printlogo(self,logo=1,start=0,length=240): #xH=0,xL=0,yH=0,yL=0):
        """ print logo from flash bank """
        START=pack('>h', int(start))
        LENGTH=pack('>h', int(length))
        if logo == 1:
            self._raw(P_LOGO1_PART,START,LENGTH)
            #self.num(xH),self.num(xL),self.num(yH),self.num(yL))
        elif logo == 2:
            self._raw(P_LOGO2_PART,START,LENGTH)
            #self.num(xH),self.num(xL),self.num(yH),self.num(yL))
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

    def _check_image_size(self, size):
        """ Check and fix the size of the image to 32 bits """
        if size % 32 == 0:
            return (0, 0)
        else:
            image_border = 32 - (size % 32)
            if (image_border % 2) == 0:
                return (image_border / 2, image_border / 2)
            else:
                return (image_border / 2, (image_border / 2) + 1)


    def _print_image(self, line, size):
        """ Print formatted image """
        i = 0
        cont = 0
        buffer = ""
       
#        self._raw(S_RASTER_2W)
        self._raw(S_RASTER_N)
        buffer = "%02X%02X%02X%02X" % (((size[0]/size[1])/8), 0, size[1], 0)
        self._raw(buffer.decode('hex'))
        buffer = ""

        while i < len(line):
            hex_string = int(line[i:i+8],2)
            buffer += "%02X" % hex_string
            i += 8
            cont += 1
            if cont % 4 == 0:
                self._raw(buffer.decode("hex"))
                buffer = ""
                cont = 0


    def _convert_image(self, im):
        """ Parse image and prepare it to a printable format """
        pixels   = []
        pix_line = ""
        im_left  = ""
        im_right = ""
        switch   = 0
        img_size = [ 0, 0 ]


        if im.size[0] > 512:
            print  ("WARNING: Image is wider than 512 and could be truncated at print time ")
        if im.size[1] > 255:
            raise ImageSizeError()

        im_border = self._check_image_size(im.size[0])
        for i in range(im_border[0]):
            im_left += "0"
        for i in range(im_border[1]):
            im_right += "0"

        for y in range(im.size[1]):
            img_size[1] += 1
            pix_line += im_left
            img_size[0] += im_border[0]
            for x in range(im.size[0]):
                img_size[0] += 1
                RGB = im.getpixel((x, y))
                im_color = (RGB[0] + RGB[1] + RGB[2])
                im_pattern = "1X0"
                pattern_len = len(im_pattern)
                switch = (switch - 1 ) * (-1)
                for x in range(pattern_len):
                    if im_color <= (255 * 3 / pattern_len * (x+1)):
                        if im_pattern[x] == "X":
                            pix_line += "%d" % switch
                        else:
                            pix_line += im_pattern[x]
                        break
                    elif im_color > (255 * 3 / pattern_len * pattern_len) and im_color <= (255 * 3):
                        pix_line += im_pattern[-1]
                        break 
            pix_line += im_right
            img_size[0] += im_border[1]

        self._print_image(pix_line, img_size)


    def image(self,path_img):
        """ Open image file """
        im_open = Image.open(path_img)
        im = im_open.convert("RGB")
        # Convert the RGB image in printable image
        self._convert_image(im)


#    def qr(self,text):
#        """ Print QR Code for the provided string """
#        qr_code = qrcode.QRCode(version=4, box_size=4, border=1)
#        qr_code.add_data(text)
#        qr_code.make(fit=True)
#        qr_img = qr_code.make_image()
#        im = qr_img._img.convert("RGB")
        # Convert the RGB image in printable image
#        self._convert_image(im)
