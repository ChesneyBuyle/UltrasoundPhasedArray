#  ____  ____      _    __  __  ____ ___
# |  _ \|  _ \    / \  |  \/  |/ ___/ _ \
# | | | | |_) |  / _ \ | |\/| | |  | | | |
# | |_| |  _ <  / ___ \| |  | | |__| |_| |
# |____/|_| \_\/_/   \_\_|  |_|\____\___/
#                           research group
#                             dramco.be/
#
#  KU Leuven - Technology Campus Gent,
#  Gebroeders De Smetstraat 1,
#  B-9000 Gent, Belgium
#
#         File: controller.py
#      Created: 09-07-2021
#       Author: Chesney Buyle
#      Version: 1.0
#
#  Description: controller commands to NUCLEO board

import struct
import serial

# Virtual COM Port (VCP) of the NUCLEO board
ser = serial.Serial('COM6', 115200, timeout=1)


def disable_all_speaker_elements():
    # Sleep command = command 1
    payload_list = [6, 0, 0, 0, 0]

    # Send payload to VCP
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]
    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def disable_all_speaker_elements_software():
    # Sleep command = command 1
    payload_list = [8, 0, 0, 0, 0]

    # Send payload to VCP
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]
    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def enable_all_speaker_elements():
    # Sleep command = command 1
    payload_list = [7, 0, 0, 0, 0]

    # Send payload to VCP
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]
    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def enable_all_speaker_elements_software():
    # Sleep command = command 1
    payload_list = [9, 0, 0, 0, 0]

    # Send payload to VCP
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]
    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def disable_specific_speaker_element(dev):
    # Sleep command = command 1
    payload_list = [1, dev, 0, 0, 0]

    # Send payload to VCP
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]
    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def enable_specific_speaker_element(dev):
    # Enable command = command 1
    payload_list = [5, dev, 0, 0, 0]

    # Send payload to VCP
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]
    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def change_speaker_settings(dev, freq, phase, amp):
    # Change speaker settings = command 0
    payload_list = [0, dev, freq, phase, amp]
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]

    ser.write(payload)
    if ser.inWaiting():
        pass
        # print(ser.readline())


def change_speaker_vga(dev, amp):
    # Change speaker settings = command 0
    payload_list = [2, dev, 0, 0, amp]
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]

    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def change_speaker_frequency(dev, freq):
    # Change speaker settings = command 0
    payload_list = [3, dev, freq, 0, 0]
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]

    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())


def change_speaker_phase(dev, phase):
    # Change speaker settings = command 0
    payload_list = [4, dev, 0, phase, 0]
    payload = struct.pack(">BBHHH", *payload_list)  # big endian, [uchar, ushort, ushort, ushort]

    ser.write(payload)
    if ser.inWaiting():
        print(ser.readline())