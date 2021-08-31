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
#         File: daq.py
#      Created: 09-07-2021
#       Author: Chesney Buyle
#      Version: 1.0
#
#  Description: measurement of microphone signal

import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import (
    TerminalConfiguration, AcquisitionType, Edge)

# DAQ settings
sample_rate = 400000  # Samples/s
num_samples = 4095  # max support by DAQ = 4095
num_sample_loops = 10

microphone_data = 0
avg_rms_microphone_data = 0
max_rms_microphone_data = 0
min_rms_microphone_data = 0
std_rms_microphone_data = 0


def sample_microphone():
    global microphone_data

    # Measure microphone signal through NI DAQ
    with nidaqmx.Task() as task:
        # Set task settings
        task.ai_channels.add_ai_voltage_chan("Dev3/ai1", max_val=5, min_val=0,
                                             terminal_config=TerminalConfiguration.RSE)
        task.timing.cfg_samp_clk_timing(rate=sample_rate, active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE,
                                        samps_per_chan=num_samples)

        while not task.is_task_done():
            pass

        # Read data from the NI DAQ
        microphone_data = task.read(num_samples)
        microphone_data = np.array(microphone_data)

    return microphone_data


def calculate_microphone_params(print_avg_rms):
    global microphone_data
    global num_sample_loops
    global avg_rms_microphone_data
    global max_rms_microphone_data
    global min_rms_microphone_data
    global std_rms_microphone_data

    # The microphone signal is sampled 'num_sample_loops' times to calculate an average RMS value
    rms_buffer = np.zeros(num_sample_loops)
    mic_signal = None

    for i in range(0, num_sample_loops):
        # Sample microphone signal (4095 samples)
        mic_signal = sample_microphone()

        # Calculate mean
        mean_microphone_data = np.mean(microphone_data)
        ac_microphone_data = microphone_data - mean_microphone_data

        # Calculate RMS value of the microphone signal
        rms_buffer[i] = np.sqrt(np.mean(ac_microphone_data ** 2))

        # if i >= 0:
        #     plot_microphone_signal()

    avg_rms_microphone_data = np.mean(rms_buffer)
    max_rms_microphone_data = np.max(rms_buffer)
    min_rms_microphone_data = np.min(rms_buffer)
    std_rms_microphone_data = np.std(rms_buffer)

    if print_avg_rms:
        print("AVG RMS: " + str(avg_rms_microphone_data))

    return [avg_rms_microphone_data, min_rms_microphone_data, max_rms_microphone_data, std_rms_microphone_data,
            mic_signal]


def plot_microphone_signal():
    global microphone_data

    # Plot a part of the measured microphone signal
    plt.clf()
    plt.plot(microphone_data)
    plt.show()
