#!/usr/bin/python
"""
@original code: Manuel F Martinez <manpaz@bashlinux.com>
@author: Kaltashkin Eugene <zhecka@gmail.com>
@license: BSD
"""

import usb.core
import usb.util
import serial
import socket
import pprint

from escpos import *
from constants import *
from exceptions import *

class Usb(Escpos):
    """ Define USB printer """

    def __init__(self, idVendor, idProduct, interface=0, in_ep=0x82, out_ep=0x01):
        """
        @param idVendor  : Vendor ID
        @param idProduct : Product ID
        @param interface : USB device interface
        @param in_ep     : Input end point
        @param out_ep    : Output end point
        """
        self.idVendor  = idVendor
        self.idProduct = idProduct
        self.interface = interface
        self.in_ep     = in_ep
        self.out_ep    = out_ep
        self.open()


    def open(self):
        """ Search device on USB tree and set is as escpos device """
        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self.device is None:
            print "Cable isn't plugged in"

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print "Could not detatch kernel driver: %s" % str(e)

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            print "Could not set configuration: %s" % str(e)


    def _raw1(self, msg):
        """ Print any command sent in raw format """
        self.device.write(self.out_ep, msg, self.interface)

    def _raw(self, *args):
        """ Print any command sent in raw format """
        self.device.write(self.out_ep, "".join(args), self.interface)

    def expand_bit_by_bit(self,byte,hash):
        byte = ord(byte)
        ret = []
        for i in range (0,7):
            bit = byte & 1
            if hash[i][bit] != '':
                ret.append(hash[i][bit])
            byte >>= 1
        return ret                

    def _read_status(self):
        try:
            model = MODELS[self._stread('\x1d\x49\x01')]
        except KeyError:
            print "Sorry. No supported model found"
            print "Library supports only %s" % ", ".join(GETSTATUS.keys())
        else:
            print "Printer model ID: %s" % model
            print "Rom version ID: %s" % self._stread('\x1d\x49\x03')
            print "Paper available: %s" % self._stread('\x1d\xe1')
            print "Cuts performed: %s" % self._stread('\x1d\xe2')
            print "Paper printed length: %s" % self._stread('\x1d\xe3')
            print "Number of retracting: %s" % self._stread('\x1d\xe4')
            print "Number of powerups: %s\n" % self._stread('\x1d\xe5')

            print "Supported features:"
            type_id = self._stread('\x1d\x49\x02')
            print "\n".join(self.expand_bit_by_bit(type_id,TYPEID))
        
            tmp = self._stread('\x10\x04\x01')
            print "Printer status: %s" % ', '.join(self.expand_bit_by_bit(tmp,GETSTATUS[model]['PRINTER']))
            tmp = self._stread('\x10\x04\x02')
            print "Offline status: %s" % ', '.join(self.expand_bit_by_bit(tmp,GETSTATUS[model]['OFFLINE']))
            tmp = self._stread('\x10\x04\x03')
            print "Error status: %s" % ', '.join(self.expand_bit_by_bit(tmp,GETSTATUS[model]['ERROR']))

            roll = self._stread('\x10\x04\x04')
            if IGNORE_NEAR_END:
                    roll = self.ignoreNear(roll,'ROLL')
                    GETSTATUS[model]['ROLL'][2] = RESERVED
                    GETSTATUS[model]['ROLL'][3] = RESERVED

            print "Roll status: %s" % ', '.join(self.expand_bit_by_bit(roll,GETSTATUS[model]['ROLL']))

            tmp = self._stread('\x10\x04\x11')
            print "PRINT status: %s\n" % ', '.join(self.expand_bit_by_bit(tmp,GETSTATUS[model]['PRINT']))

            print "Full status details:"
            fullstatus = self._stread('\x10\x04\x14')
            print self._sthread('\x10\x04\x14')
            if ord(fullstatus[0]) != 16 and ord(fullstatus[1]) != 15:
                raise Exception
            else:
                paperstatus = fullstatus[2]
                userstatus = fullstatus[3]
                recoverablestatus = fullstatus[4]
                unrecoverablestatus = fullstatus[5]
                if IGNORE_NEAR_END:
                    paperstatus = self.ignoreNear(paperstatus,'PAPER')
                    GETSTATUS[model]['PAPER'][2] = RESERVED
                    GETSTATUS[model]['PAPER'][6] = RESERVED
                                        
                print "Paper status: %s" % ', '.join(self.expand_bit_by_bit(paperstatus,GETSTATUS[model]['PAPER']))
                print "User status: %s" % ', '.join(self.expand_bit_by_bit(userstatus,GETSTATUS[model]['USER']))
                print "Recoverable status: %s" % ', '.join(self.expand_bit_by_bit(recoverablestatus,GETSTATUS[model]['RECOVER']))
                print "Unrecoverable status: %s" % ', '.join(self.expand_bit_by_bit(unrecoverablestatus,GETSTATUS[model]['UNRECOVER']))
                                        
    def	ignoreNear(self,strvalue,mask):
        """ Bitwise mask between chr and bit """
        return chr(ord(strvalue)&IGNORE_NEAR_END_MASK[mask])
         
    def _stread(self,buf):
        """ read data from device and put it to string """
        self.device.write(self.out_ep, buf, self.interface)
        ret = self.device.read(self.in_ep, 100, self.interface)#, 100)
        sret = ''.join([chr(x) for x in ret])
        return sret

    def _sthread(self,buf):
        """ read data from device and put it to hex string"""
        self.device.write(self.out_ep, buf, self.interface)
        ret = self.device.read(self.in_ep, 100, self.interface)#, 100)
        sret = ','.join([hex(x) for x in ret])
        return sret
        
    def __del__(self):
        """ Release USB interface """
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None



class Serial(Escpos):
    """ Define Serial printer """

    def __init__(self, devfile="/dev/ttyS0", baudrate=9600, bytesize=8, timeout=1):
        """
        @param devfile  : Device file under dev filesystem
        @param baudrate : Baud rate for serial transmission
        @param bytesize : Serial buffer size
        @param timeout  : Read/Write timeout
        """
        self.devfile  = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout  = timeout
        self.open()


    def open(self):
        """ Setup serial port and set is as escpos device """
        self.device = serial.Serial(port=self.devfile, baudrate=self.baudrate, bytesize=self.bytesize, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=self.timeout, dsrdtr=True)

        if self.device is not None:
            print "Serial printer enabled"
        else:
            print "Unable to open serial printer on: %s" % self.devfile


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg)


    def __del__(self):
        """ Close Serial interface """
        if self.device is not None:
            self.device.close()



class Network(Escpos):
    """ Define Network printer """

    def __init__(self,host,port=9100):
        """
        @param host : Printer's hostname or IP address
        @param port : Port to write to
        """
        self.host = host
        self.port = port
        self.open()


    def open(self):
        """ Open TCP socket and set it as escpos device """
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.connect((self.host, self.port))

        if self.device is None:
            print "Could not open socket for %s" % self.host


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.send(msg)


    def __del__(self):
        """ Close TCP connection """
        self.device.close()



class File(Escpos):
    """ Define Generic file printer """

    def __init__(self, devfile="/dev/usb/lp0"):
        """
        @param devfile : Device file under dev filesystem
        """
        self.devfile = devfile
        self.open()

    def _read_status(self):
        pass


    def open(self):
        """ Open system file """
        self.device = open(self.devfile, "wb")

        if self.device is None:
            print "Could not open the specified file %s" % self.devfile


    def _raw1(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg);

    def _raw(self, *args):
        """ Print any command sent in raw format """
        self.device.write("".join(args))


    def __del__(self):
        """ Close system file """
        self.device.close()
