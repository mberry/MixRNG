
from os import urandom
from time import sleep
import serial


def hwrng(numbytes, port):
    """Extracts random bits from OneRNG, check serial settings if using different hwrng"""
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=5,
        rtscts=True)

    #Wait for handshake, Request To Send True
    sleep(1)
    ser.setRTS(1)

    # Entropy feed starts/stops on input of cmdO/cmdo.
    ser.write(bytes('cmdO'.encode('ascii')))
    sleep(0.1)
    hwrng = ser.read(numbytes)
    sleep(0.1)
    ser.write(bytes('cmdo'.encode('ascii')))
    ser.setRTS(0)
    ser.close()
    return hwrng



def xorbytes(a, b):
    """Converts a&b from bytes to int then xor and returns as bytes"""
    a = int.from_bytes(a, byteorder='big')
    b = int.from_bytes(b, byteorder='big')
    xor = a ^ b
    return xor.to_bytes((xor.bit_length() + 7) // 8, byteorder='big')


def rngmix(numbytes, port='COM4'):
    """Returns xor of inbuilt CSRNG and hardware CSRNG"""
    hw = hwrng(numbytes, port)
    ib = urandom(numbytes)
    return xorbytes(hw, ib)


# Test output:
# print('hwrng: ', hwrng(100, 'COM4'))
# print('xor: ', rngmix(100))
