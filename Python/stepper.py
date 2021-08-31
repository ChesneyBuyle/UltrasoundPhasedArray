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
#         File: stepper.py
#      Created: 11-07-2021
#       Author: Chesney Buyle
#      Version: 1.0
#
#  Description: Phased Array Measurements
#      Stepper control for beam pattern measurements

import serial
import time

# Arduino and stepper motor settings
arduino_ser = serial.Serial()
arduino_ser_port = "COM7"
arduino_baud = 9600

num_steps_one_revolution_az = 3200  # 2090
degree_per_step_az = 360 / num_steps_one_revolution_az
current_steps_from_base_az = 0


def start_arduino_serial():
    global arduino_ser

    # setup serial port to communicate with Arduino
    arduino_ser = serial.Serial(arduino_ser_port, arduino_baud, timeout=1)
    bool_serial_open = arduino_ser.is_open
    print("Check if serial is open (True = open): " + str(bool_serial_open))

    # If serial is already open, then close it again
    if bool_serial_open:
        arduino_ser.close()

    # Now open serial again to use it
    arduino_ser.open()

    if bool_serial_open:
        print("Arduino serial ready.")

    # wait until Arduino booted
    time.sleep(2)

    # Print Arduino boot text
    while arduino_ser.inWaiting():
        data = arduino_ser.readline()
        print(data)

    time.sleep(1)


def set_stepper_at_angle_relative_to_base_az(angle):
    global degree_per_step_az
    global current_steps_from_base_az
    global arduino_ser

    # Calculate the number of steps to be taken to set stepper to 'angle'
    target_num_steps_relative_to_base = round(angle/degree_per_step_az)
    num_steps_to_be_taken = target_num_steps_relative_to_base - current_steps_from_base_az

    # Write number of steps to Arduino serial
    arduino_ser.write(str.encode('rotate_az\r\n'))

    # Wait for response (OK)
    while not arduino_ser.inWaiting():
        pass

    # Print out received serial data
    while arduino_ser.inWaiting():
        print(arduino_ser.readline())

    # Send number of steps to be taken to get to angle
    arduino_ser.write(str.encode(str(num_steps_to_be_taken) + '\r\n'))

    # Wait for response (OK) = when turn is executed
    while not arduino_ser.inWaiting():
        pass

    # Print out serial data
    while arduino_ser.inWaiting():
        print(arduino_ser.readline())

    # Update current steps from base
    current_steps_from_base_az = current_steps_from_base_az + num_steps_to_be_taken

