#!/usr/bin/env python
import time
import serial
from os import urandom


def extrng(numbytes, port='COM4'):
    """Extracts bits from OneRNG, check serial settings and start/stop command if using different hardware"""
    
    # OneRNG feed starts/stops on input of cmdO/cmdo    
    start = 'cmdO'
    stop = 'cmdo'
    
    # Serial settings
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=5,
        rtscts=True)
    
    # Wait for handshake, Request To Send set True
    time.sleep(0.2)
    ser.setRTS(1)
    
    # Start
    ser.write(bytes(start.encode('ascii')))
    time.sleep(0.1)
    
    # Read
    hwrng = ser.read(numbytes)
    time.sleep(0.1)
    
    # Stop
    ser.write(bytes(stop.encode('ascii'))) 
    ser.setRTS(0)
    ser.close()
    return hwrng


def xorbytes(a, b):
    """ bytes > int > xor > int > bytes """
    a = int.from_bytes(a, byteorder='big')
    b = int.from_bytes(b, byteorder='big')
    xor = a ^ b
    return xor.to_bytes((xor.bit_length() + 7) // 8, byteorder='big')


def mixrng(numbytes, port='COM4'):
    """Returns bitwise xor of an inbuilt and hardware CSRNG"""
    internal = urandom(numbytes)
    external = extrng(numbytes, port)
    return xorbytes(internal, external)

