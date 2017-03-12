#!/usr/bin/env python
import serial
from os import urandom
from time import sleep


def hwrng(numbytes, port='COM4'):
    """Extracts bits from OneRNG, check serial settings and start/stop command if using different hardware"""
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=5,
        rtscts=True)

    # Wait for handshake, Request To Send True
    sleep(0.5)
    ser.setRTS(1)

    # Entropy feed start/stops on input of cmdO/cmdo for the OneRNG.
    ser.write(bytes('cmdO'.encode('ascii'))) # Start
    sleep(0.1)
    hwrng = ser.read(numbytes)
    sleep(0.1)
    ser.write(bytes('cmdo'.encode('ascii'))) # Stop
    ser.setRTS(0)
    ser.close()
    return hwrng


def xorbytes(a, b):
    """ bytes >> int >> xor >> int >> bytes """
    a = int.from_bytes(a, byteorder='big')
    b = int.from_bytes(b, byteorder='big')
    xor = a ^ b
    return xor.to_bytes((xor.bit_length() + 7) // 8, byteorder='big')


def mixrng(numbytes, port='COM4'):
    """Returns bitwise xor of an inbuilt and hardware CSRNG"""
    ib = urandom(numbytes)
    hw = hwrng(numbytes, port)
    return xorbytes(ib, hw)

