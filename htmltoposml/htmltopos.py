from constants import *
from exceptions import *
from HTMLParser import HTMLParser
from struct import pack

class HTMLtoPOS(HTMLParser):
    def __init__(self):
        self.reset()

    def handle_starttag(self, tag, attrs):
        """ Handle start tag """
        tag = tag.upper()
        if tag in STARTTAG:
            self._raw(STARTTAG[tag])
        elif tag == 'FONT':
#            print "Font Tag found ",attrs
            for pair in attrs:
                (NAME,VALUE) = (pair[0].upper(),pair[1].upper())
                if NAME == 'FACE':
                    if VALUE == 'B':
                        self._raw(TXT_FONT_B)
                    else:
                        self._raw(TXT_FONT_A)
                elif NAME == 'SIZE':
                        self._raw(TXT_SIZE_CUSTOM)
                        self._raw(chr(int(VALUE,16)))
                else:
                    print type(pair)," NAME=",NAME," VALUE=",VALUE
        elif tag == 'TEXT':
#            print 'Tag Text Found ',attrs
            for pair in attrs:
                (NAME,VALUE) = (pair[0].upper(),pair[1].upper())
                if NAME == 'SIZE':
                    self._raw(TXT_SIZE_CUSTOM)
                    self._raw(chr(int(VALUE,16)))
                elif NAME == 'CPI':
                    print "CPI ",VALUE
                    if VALUE == '0':
                        self._raw(TXT_CPI_MODE0)
                    elif VALUE == '1':
                        self._raw(TXT_CPI_MODE1)
                    elif VALUE == '2':
                        self._raw(TXT_CPI_MODE2)
                    else:
                        self._raw(TXT_CPI_MODE1)
                elif NAME == 'ALIGN':
                    self._raw(TXT_ALIGN[VALUE])
                elif NAME == 'HT':
                    print "HT FOUND! ",VALUE
                    self._raw(TXT_SET_HT)
                    if VALUE == 0:
                        self._raw(NUL)
                    else:
                        for count in range (1,9):
                            self._raw(pack('B',int(VALUE)*count))
#                            self._raw(chr(int(VALUE)*count))
                        self._raw(NUL)
                elif NAME == 'PD':
		    if VALUE == '0':
			self._raw(PD_N50)
		    elif VALUE == '1':
			self._raw(PD_N37)
		    elif VALUE == '2':
			self._raw(PD_N25)
		    elif VALUE == '3':
			self._raw(PD_N12)
		    elif VALUE == '4':
			self._raw(PD_0)
		    elif VALUE == '5':
			self._raw(PD_P12)
		    elif VALUE == '6':
			self._raw(PD_P25)
		    elif VALUE == '7':
			self._raw(PD_P37)
		    elif VALUE == '8':
			self._raw(PD_P50)
		    else:# DEFAULT: DOES NOTHING
			pass
                elif NAME == 'LS':
                    if VALUE == '1/6':
                        self._raw(TXT_16LSP)
                    elif VALUE == '1/8':
                        self._raw(TXT_18LSP)
                    else:
                        self._raw(TXT_LSP)
                        self._raw(pack('B',int(VALUE)))
                elif NAME == 'LMARGIN':
                    if VALUE != '':
                        self._raw(TXT_LMARGIN)
                        self._raw(pack('<h', int(VALUE)))
                elif NAME == 'PWIDTH':
                    if VALUE != '':
                        self._raw(TXT_PWIDTH)
                        self._raw(pack('<h', int(VALUE)))
                else:
                    pass
        elif tag == 'BARCODE':
#            self.barcodestruct = BARCODESTRUCT
            #{ 'WIDTH': 3, 'HEIGHT': 162, 'FONT': 'A', 'POS': 'ABOVE' }
            for pair in attrs:
                (NAME,VALUE) = (pair[0].upper(),pair[1].upper())
                self.barcodestruct[NAME]=VALUE
            print 'self.barcodestruct',self.barcodestruct
            self.barcodeprint()
        elif tag == 'LOGO':
            for pair in attrs:
                (NAME,VALUE) = (pair[0].upper(),pair[1].upper())
                if NAME == 'START':
                    START=pack('>h', int(VALUE))
                elif NAME == 'LENGTH':
                    LENGTH=pack('>h', int(VALUE))
                elif NAME == 'BANK':
                    BANK = int(VALUE)
            if BANK == 2:
                self._raw(P_LOGO2_PART,START,LENGTH)
            else:
                self._raw(P_LOGO1_PART,START,LENGTH)
        else:
            pass

    def handle_endtag(self, tag):
        """ Handle closing tag """
        tag = tag.upper()
        if tag in CLOSETAG:
            self._raw(CLOSETAG[tag])
        else:
            pass

    def handle_data(self, data):
        """ Put data to raw """
        self._raw(data.encode("cp866"))

    def clean(self):
        pass
