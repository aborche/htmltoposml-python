#!/usr/bin/python
# -*- coding: utf8 -*-

from htmltoposml import *
from htmltoposml.constants import *
from htmltoposml.htmltopos import *
from htmltoposml.printer import *
from struct import *
from HTMLParser import HTMLParser
from cgi import parse_qs, escape, test
import sys,pprint,locale

def application(env, start_response):

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

  testq=query.get('test',[''])[0]

  print testq
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
