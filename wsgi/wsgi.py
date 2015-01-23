#!/usr/bin/python
# -*- coding: utf8 -*-

from htmltoposml import *
from htmltoposml.constants import *
from htmltoposml.htmltopos import *
from htmltoposml.printer import *
from struct import *
from HTMLParser import HTMLParser
from cgi import parse_qs, escape, test
import sys,pprint,locale,re

# remove annoying characters
chars = {
	'\xc2\x82' : ',',        # High code comma
	'\xc2\x84' : ',,',       # High code double comma
	'\xc2\x85' : '...',      # Tripple dot
	'\xc2\x88' : '^',        # High carat
	'\xc2\x91' : '\x27',     # Forward single quote
	'\xc2\x92' : '\x27',     # Reverse single quote
	'\xc2\x93' : '\x22',     # Forward double quote
	'\xc2\x94' : '\x22',     # Reverse double quote
	'\xc2\x95' : ' ',
	'\xc2\x96' : '-',        # High hyphen
	'\xc2\x97' : '--',       # Double hyphen
	'\xc2\x99' : ' ',
	'\xc2\xa0' : ' ',
	'\xc2\xa6' : '|',        # Split vertical bar
	'\xc2\xab' : '<<',       # Double less than
	'\xc2\xbb' : '>>',       # Double greater than
	'\xc2\xbc' : '1/4',      # one quarter
	'\xc2\xbd' : '1/2',      # one half
	'\xc2\xbe' : '3/4',      # three quarters
	'\xca\xbf' : '\x27',     # c-single quote
	'\xcc\xa8' : '',         # modifier - under curve
	'\xcc\xb1' : ''          # modifier - under line
}

def replace_chars(match):
    char = match.group(0)
    return chars[char]

#return re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, text)


def application(env, start_response):
  pprint.pprint(env)
  start_response('200 OK', [('Content-Type','text/html, charset=utf-8')])
  if env['REQUEST_METHOD'] == 'GET':
    query = parse_qs(env['QUERY_STRING'])
  else:
    try:
      request_body_size = int(env.get('CONTENT_LENGTH', 0))
    except (ValueError):
      request_body_size = 0
    request_body = env['wsgi.input'].read(request_body_size)
    query = parse_qs(request_body)

  testq=re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, query.get('test',[''])[0])
  print type(testq)," ",testq.decode('utf-8')

  Custom.hw('INIT')
  Custom.cut('TOTAL')
  Custom.paper('OUT')
  Custom.feed(testq.decode('utf-8'))
  Custom.cut('TOTAL')
  Custom.paper('OUT')
  Custom.control('FF')
#  Custom._read_status()
  return [htmlhead+testq+htmlend]# .encode('utf8')]

class UsbPOS(Usb,HTMLtoPOS):
        def __init__(self, **kwargs):
                HTMLtoPOS.__init__(self)
                Usb.__init__(self, **kwargs)
                self.barcodestruct=BARCODESTRUCT

class FilePOS(File,HTMLtoPOS):
        def __init__(self, **kwargs):
                HTMLtoPOS.__init__(self)
                File.__init__(self, **kwargs)
                self.barcodestruct=BARCODESTRUCT

locale.setlocale(locale.LC_ALL, ('RU','UTF8'))

Custom=UsbPOS(idVendor=0x0dd4,idProduct=0x015d,interface=0,in_ep=0x81,out_ep=0x02)
#Custom=FilePOS(devfile="test.file")




htmlhead="""<HTML><HEAD>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8;">
  </HEAD>
  <BODY>
"""
htmlend="""
  </FORM>
  </BODY>
  </HTML>
"""
