#!/usr/bin/env python
# encoding: utf-8
import sys
import serial
import argparse


commands = {
        'BBIO1': b'\x00',    # Enter reset binary mode
        'SPI1':  b'\x01',    # Enter binary SPI mode
        'I2C1':  b'\x02',    # Enter binary I2C mode
        'ART1':  b'\x03',    # Enter binary UART mode
        '1W01':  b'\x04',    # Enter binary 1-Wire mode
        'RAW1':  b'\x05',    # Enter binary raw-wire mode
        'RESET': b'\x0F',    # Reset Bus Pirate
        'STEST': b'\x10',    # Bus Pirate self-tests
}


def arg_auto_int(x):
    return int(x, 0)


class FatalError(RuntimeError):
    def __init__(self, message):
        RuntimeError.__init__(self, message)


def main():
    parser = argparse.ArgumentParser(description = 'Bus Pirate binary interface demo', prog = 'binaryModeDemo')


    parser.add_argument(
            '--port', '-p',
            help = 'Serial port device',
            default = '/dev/ttyUSB0')


    parser.add_argument(
            '--baud', '-b',
            help = 'Serial port baud rate',
            type = arg_auto_int,
            default = 115200)


    args = parser.parse_args()


    print('\nTrying port: ', args.port, ' at baudrate: ', args.baud)


    try:
        port = serial.Serial(args.port, args.baud, timeout=0.1)
    except Exception as e:
        print('I/O error({0}): {1}'.format(e.errno, e.strerror))
        print('Port cannot be opened')
    else:
        print('Ready!')
        print('Entering binary mode...\n')


        count = 0
        done = False
        while count < 20 and not done:
            count += 1
            port.write(commands.get('BBIO1'))
            got = port.read(5)  # Read up to 5 bytes
            print(got)
            if got == b'BBIO1':
                done = True
        if not done:
            port.close()
            raise FatalError('Buspirate failed to enter binary mode')


        # Now that the Buspirate is in binary mode, choose a BP mode
        port.write(commands.get('RESET'))
        while True:
            got = port.readline()
            if not got:
                break
            print(got),




        port.close()




if __name__ == '__main__':
    try:
        main()
    except FatalError as e:
        print('\nA fatal error occurred: %s',e)
        sys.exit(2)