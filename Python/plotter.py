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
#         File: plotter.py
#      Created: 09-07-2021
#       Author: Chesney Buyle
#      Version: 1.0
#
#  Description: Phased Array Measurements
#      Plot beam pattern results

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
from numpy import inf

# Single speaker beam pattern (at 0.25m)
array_configuration = "1x1"
freq = "25kHz"
dist = "0_25m"
beam_angle = "0"
version = "anechoic_single_speaker_v0"
datetime = "20210713-112641"

# uncalibrated beam pattern anechoic chamber
# array_configuration = "1x10"
# freq = "25kHz"
# dist = "0_75m"
# beam_angle = "0"
# version = "anechoic_uncalibrated_v0"
# datetime = "20210713-124206"

# calibrated beam pattern anechoic chamber
# array_configuration = "1x10"
# freq = "25kHz"
# dist = "0_75m"
# beam_angle = "0"
# version = "anechoic_v0"
# datetime = "20210713-163803"

# beam steering to 30
# array_configuration = "1x10"
# freq = "25kHz"
# dist = "0_75m"
# beam_angle = "30"
# version = "anechoic_v0"
# datetime = "20210713-170330"

# beam steering to 50
# array_configuration = "1x10"
# freq = "25kHz"
# dist = "0_75m"
# beam_angle = "50"
# version = "anechoic_v0"
# datetime = "20210713-175114"

# beam steering to 70
# array_configuration = "1x10"
# freq = "25kHz"
# dist = "0_75m"
# beam_angle = "70"
# version = "anechoic_v0"
# datetime = "20210713-181854"


plt_frequencies = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

min_angle = -180
max_angle = 180
angle_step = 1
num_angle_points = int(np.abs(max_angle - min_angle) / angle_step + 1)

color1 = None
color2 = None
color3 = None
color4 = None
color5 = None
color6 = None
color7 = None
color8 = None
color9 = None
color10 = None

# Files measurement data
# Amplitude calibration files
f_name_uncalibrated_speaker_sweep = "uncal_speaker_sweep_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_min = "uncal_speaker_sweep_min_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_max = "uncal_speaker_sweep_max_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_std = "uncal_speaker_sweep_std_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_info = "uncal_speaker_sweep_info_" + version + ".txt"

f_name_calibrated_speaker_sweep = "cal_speaker_sweep_" + version + ".txt"
f_name_calibrated_speaker_sweep_min = "cal_speaker_sweep_min_" + version + ".txt"
f_name_calibrated_speaker_sweep_max = "cal_speaker_sweep_max_" + version + ".txt"
f_name_calibrated_speaker_sweep_std = "cal_speaker_sweep_std_" + version + ".txt"
f_name_calibrated_speaker_sweep_info = "cal_speaker_sweep_info_" + version + ".txt"

# Beam pattern files
f_name_beam_pattern = "beampattern_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist) + \
                      "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + str(datetime) + ".txt"

f_name_beam_pattern_info = "beampattern_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist) + \
                           "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + str(datetime) + "info.txt"
# Files simulation data
f_name_beam_pattern_sim_custom = "Matlab simulation/resp_" + str(array_configuration) + "_config_" + str(freq) + "_beamangle_" + \
                                 str(beam_angle) + "_sim_custom.txt"
f_name_beam_pattern_sim_omni = "Matlab simulation/resp_" + str(array_configuration) + "_config_" + str(freq) + "_beamangle_" + \
                                 str(beam_angle) + "_sim_omni.txt"
# Files plot
# Amplitude calibration files
fname_uncalibrated_response_plt = "f_name_uncalibrated_" + version + ".pdf"
fname_calibrated_response_plt = "f_name_calibrated_" + version + ".pdf"
filename_plot_rms_vs_angle = "beampattern_rms_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist)\
                                + "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + str(datetime) + ".pdf"
filename_plot_rms_dB_vs_angle = "beampattern_db_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist)\
                                + "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + str(datetime) + ".pdf"
filename_plot_rms_dB_vs_angle_simandmeas = "beampattern_db_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist)\
                                + "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + str(datetime) + "simandmeas.pdf"
filename_plot_rms_dB_vs_angle_uncalibrated_and_calibrated = "beampattern_db_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist)\
                                + "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + str(datetime) + "(un)calibrated.pdf"


def show_speaker_response_uncalibrated():
    global f_name_uncalibrated_speaker_sweep
    global plt_frequencies
    global fname_uncalibrated_response_plt
    global color1, color2, color3, color4, color5, color6, color7, color8, color9, color10

    # Response data from amplitude calibration measurement
    data = np.loadtxt(f_name_uncalibrated_speaker_sweep, ndmin=2)

    # Plot uncalibrated plot
    plt.clf()
    f = plt.figure()


    a = plt.plot(plt_frequencies, 20 * np.log10(data[0, :]), linewidth=1, label='Speaker 1')
    b = plt.plot(plt_frequencies, 20 * np.log10(data[1, :]), linewidth=1, label='Speaker 2')
    c = plt.plot(plt_frequencies, 20 * np.log10(data[2, :]), linewidth=1, label='Speaker 3')
    d = plt.plot(plt_frequencies, 20 * np.log10(data[3, :]), linewidth=1, label='Speaker 4')
    e = plt.plot(plt_frequencies, 20 * np.log10(data[4, :]), linewidth=1, label='Speaker 5')
    f = plt.plot(plt_frequencies, 20 * np.log10(data[5, :]), linewidth=1, label='Speaker 6')
    g = plt.plot(plt_frequencies, 20 * np.log10(data[6, :]), linewidth=1, label='Speaker 7')
    h = plt.plot(plt_frequencies, 20 * np.log10(data[7, :]), linewidth=1, label='Speaker 8')
    i = plt.plot(plt_frequencies, 20 * np.log10(data[8, :]), linewidth=1, label='Speaker 9')
    j = plt.plot(plt_frequencies, 20 * np.log10(data[9, :]), linewidth=1, label='Speaker 10')
    color1 = a[-1].get_color()
    color2 = b[-1].get_color()
    color3 = c[-1].get_color()
    color4 = d[-1].get_color()
    color5 = e[-1].get_color()
    color6 = f[-1].get_color()
    color7 = g[-1].get_color()
    color8 = h[-1].get_color()
    color9 = i[-1].get_color()
    color10 = j[-1].get_color()
    plt.plot(plt_frequencies, 20 * np.log10(data[0, :]), linewidth=0.5, marker='o', markersize=3, color=color1)
    plt.plot(plt_frequencies, 20 * np.log10(data[1, :]), linewidth=0.5, marker='o', markersize=3, color=color2)
    plt.plot(plt_frequencies, 20 * np.log10(data[2, :]), linewidth=0.5, marker='o', markersize=3, color=color3)
    plt.plot(plt_frequencies, 20 * np.log10(data[3, :]), linewidth=0.5, marker='o', markersize=3, color=color4)
    plt.plot(plt_frequencies, 20 * np.log10(data[4, :]), linewidth=0.5, marker='o', markersize=3, color=color5)
    plt.plot(plt_frequencies, 20 * np.log10(data[5, :]), linewidth=0.5, marker='o', markersize=3, color=color6)
    plt.plot(plt_frequencies, 20 * np.log10(data[6, :]), linewidth=0.5, marker='o', markersize=3, color=color7)
    plt.plot(plt_frequencies, 20 * np.log10(data[7, :]), linewidth=0.5, marker='o', markersize=3, color=color8)
    plt.plot(plt_frequencies, 20 * np.log10(data[8, :]), linewidth=0.5, marker='o', markersize=3, color=color9)
    plt.plot(plt_frequencies, 20 * np.log10(data[9, :]), linewidth=0.5, marker='o', markersize=3, color=color10)
    plt.grid(b=True, which='major')
    plt.grid(b=True, which='minor', alpha=0.2)
    plt.minorticks_on()
    # plt.title("Uncalibrated speaker response (" + str(db_rms_deviation) + " dB deviation)")
    plt.xlabel("Frequency [kHz]")
    plt.ylabel("Response [dBV]")
    leg = plt.legend(prop = {'size': 8})
    for line in leg.get_lines():
        line.set_linewidth(2)
    plt.savefig(fname_uncalibrated_response_plt, bbox_inches='tight')
    plt.show()


def show_speaker_response_calibrated():
    global f_name_calibrated_speaker_sweep
    global color1, color2, color3, color4, color5, color6, color7, color8, color9, color10
    global fname_calibrated_response_plt

    # Plot calibrated response results
    data_cal = np.loadtxt(f_name_calibrated_speaker_sweep, ndmin=2)

    plt.clf()
    f = plt.figure()
    # a = plt.plot(frequencies, 20 * np.log10(data[0, :]), linestyle='dashed', label='Speaker 0x03', alpha=0.3)
    # b = plt.plot(frequencies, 20 * np.log10(data[1, :]), linestyle='dashed', label='Speaker 0x01', alpha=0.3)
    # c = plt.plot(frequencies, 20 * np.log10(data[2, :]), linestyle='dashed', label='Speaker 0x0B', alpha=0.3)
    # d = plt.plot(frequencies, 20 * np.log10(data[3, :]), linestyle='dashed', label='Speaker 0x09', alpha=0.3)
    # e = plt.plot(frequencies, 20 * np.log10(data[4, :]), linestyle='dashed', label='Speaker 0x07', alpha=0.3)
    # f = plt.plot(frequencies, 20 * np.log10(data[5, :]), linestyle='dashed', label='Speaker 0x05', alpha=0.3)
    # g = plt.plot(frequencies, 20 * np.log10(data[6, :]), linestyle='dashed', label='Speaker 0x0F', alpha=0.3)
    # h = plt.plot(frequencies, 20 * np.log10(data[7, :]), linestyle='dashed', label='Speaker 0x0D', alpha=0.3)
    # i = plt.plot(frequencies, 20 * np.log10(data[8, :]), linestyle='dashed', label='Speaker 0x02', alpha=0.3)
    # j = plt.plot(frequencies, 20 * np.log10(data[9, :]), linestyle='dashed', label='Speaker 0x00', alpha=0.3)

    # a = plt.plot(frequencies, 20 * np.log10(data[0, :]), linestyle='dashed', label='Speaker 1', alpha=0.3)
    # b = plt.plot(frequencies, 20 * np.log10(data[1, :]), linestyle='dashed', label='Speaker 2', alpha=0.3)
    # c = plt.plot(frequencies, 20 * np.log10(data[2, :]), linestyle='dashed', label='Speaker 3', alpha=0.3)
    # d = plt.plot(frequencies, 20 * np.log10(data[3, :]), linestyle='dashed', label='Speaker 4', alpha=0.3)
    # e = plt.plot(frequencies, 20 * np.log10(data[4, :]), linestyle='dashed', label='Speaker 5', alpha=0.3)
    # f = plt.plot(frequencies, 20 * np.log10(data[5, :]), linestyle='dashed', label='Speaker 6', alpha=0.3)
    # g = plt.plot(frequencies, 20 * np.log10(data[6, :]), linestyle='dashed', label='Speaker 7', alpha=0.3)
    # h = plt.plot(frequencies, 20 * np.log10(data[7, :]), linestyle='dashed', label='Speaker 8', alpha=0.3)
    # i = plt.plot(frequencies, 20 * np.log10(data[8, :]), linestyle='dashed', label='Speaker 9', alpha=0.3)
    # j = plt.plot(frequencies, 20 * np.log10(data[9, :]), linestyle='dashed', label='Speaker 10', alpha=0.3)

    # color1 = a[-1].get_color()
    # color2 = b[-1].get_color()
    # color3 = c[-1].get_color()
    # color4 = d[-1].get_color()
    # color5 = e[-1].get_color()
    # color6 = f[-1].get_color()
    # color7 = g[-1].get_color()
    # color8 = h[-1].get_color()
    # color9 = i[-1].get_color()
    # color10 = j[-1].get_color()
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[0, :]), linewidth=0.5, label='Speaker 1', color=color1)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[1, :]), linewidth=0.5, label='Speaker 2', color=color2)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[2, :]), linewidth=0.5, label='Speaker 3', color=color3)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[3, :]), linewidth=0.5, label='Speaker 4', color=color4)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[4, :]), linewidth=0.5, label='Speaker 5', color=color5)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[5, :]), linewidth=0.5, label='Speaker 6', color=color6)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[6, :]), linewidth=0.5, label='Speaker 7', color=color7)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[7, :]), linewidth=0.5, label='Speaker 8', color=color8)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[8, :]), linewidth=0.5, label='Speaker 9', color=color9)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[9, :]), linewidth=0.5, label='Speaker 10', color=color10)

    plt.plot(plt_frequencies, 20 * np.log10(data_cal[0, :]), marker='o', markersize=3, color=color1)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[1, :]), marker='o', markersize=3, color=color2)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[2, :]), marker='o', markersize=3, color=color3)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[3, :]), marker='o', markersize=3, color=color4)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[4, :]), marker='o', markersize=3, color=color5)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[5, :]), marker='o', markersize=3, color=color6)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[6, :]), marker='o', markersize=3, color=color7)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[7, :]), marker='o', markersize=3, color=color8)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[8, :]), marker='o', markersize=3, color=color9)
    plt.plot(plt_frequencies, 20 * np.log10(data_cal[9, :]), marker='o', markersize=3, color=color10)

    plt.grid(b=True, which='major')
    plt.grid(b=True, which='minor', alpha=0.2)
    plt.minorticks_on()
    # plt.title("Calibrated speaker response (" + str(db_rms_deviation) + " dB deviation)")
    plt.xlabel("Frequency [kHz]")
    plt.ylabel("Response [dBV]")
    leg = plt.legend(prop = {'size': 8})
    for line in leg.get_lines():
        line.set_linewidth(2)
    plt.savefig(fname_calibrated_response_plt, bbox_inches='tight')
    plt.show()


    # # plot data avg, min, max and std (microphone rms measurements)
    # data_avg = np.loadtxt(f_name_uncalibrated_speaker_sweep, ndmin=2)
    # data_min = np.loadtxt(f_name_uncalibrated_speaker_sweep_min, ndmin=2)
    # data_max = np.loadtxt(f_name_uncalibrated_speaker_sweep_max, ndmin=2)
    # data_std = np.loadtxt(f_name_uncalibrated_speaker_sweep_std, ndmin=2)
    # plt.clf()
    # f = plt.figure()
    # plt.errorbar(frequencies, data_avg[2, :], data_std[2, :], fmt='ok', lw=3)
    # plt.errorbar(frequencies, data_avg[2, :], [data_avg[2, :] - data_min[2, :], data_max[2, :] - data_avg[2, :]],
    #              fmt='.k', ecolor='gray', lw=1)
    # plt.show()


def show_beam_pattern_measurement_data(show_gofigure):
    global f_name_beam_pattern
    global filename_plot_rms_dB_vs_angle

    # Load beam pattern measurement data and ensure a continuous plot [0 - 360°]
    measurement_data = np.loadtxt(f_name_beam_pattern)
    measurement_data = np.append(measurement_data, measurement_data[0])

    # Normalize measurement data
    max_measurement_data = np.max(measurement_data)
    norm_measurement_data = measurement_data / max_measurement_data
    db_measurement_data = 20 * np.log10(norm_measurement_data)

    # Construct theta array
    theta_degrees = np.linspace(min_angle, max_angle, num_angle_points, endpoint=True)
    theta = np.deg2rad(theta_degrees)

    # Plotting
    plt.clf()
    f = plt.figure()
    plt.polar(theta, db_measurement_data, label='Measured', linewidth=1)
    ax = plt.gca()
    ax.set_rlabel_position(0)
    ax.set_rticks([-25, -20, -15, -10, -5, 0])
    plt.ylim((-30, 0))
    plt.ylabel('Response [dB]', loc='bottom', rotation=0)
    plt.legend(loc=(0.92, 0.92))
    plt.show()
    f.savefig(filename_plot_rms_dB_vs_angle, bbox_inches='tight')

    if show_gofigure:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=db_measurement_data, theta=np.linspace(min_angle, max_angle,
                                                                               num_angle_points, endpoint=True),
                                      mode='lines',
                                      connectgaps=False))
        fig.update_layout(
            title='Beam pattern'
        )
        fig.show()


def show_calibrated_and_uncalibrated_beam_pattern():
    array_configuration = "1x10"
    freq = "25kHz"
    dist = "0_75m"
    beam_angle = "0"
    version = "anechoic_uncalibrated_v0"
    datetime = "20210713-124206"

    f_name_beam_pattern_uncalibrated = "beampattern_" + str(array_configuration) + "_config_" + str(freq) + "_" + \
                                     str(dist) + "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + \
                                     str(datetime) + ".txt"

    # calibrated beam pattern anechoic chamber
    freq = "25kHz"
    dist = "0_75m"
    beam_angle = "0"
    version = "anechoic_v0"
    datetime = "20210713-163803"

    f_name_beam_pattern_calibrated = "beampattern_" + str(array_configuration) + "_config_" + str(freq) + "_" + \
                                     str(dist) + "_beamangle_" + str(beam_angle) + "_" + str(version) + "_" + \
                                     str(datetime) + ".txt"

    # Load beam pattern measurement data and ensure a continuous plot [0 - 360°]
    uncal_measurement_data = np.loadtxt(f_name_beam_pattern_uncalibrated)
    uncal_measurement_data = np.append(uncal_measurement_data, uncal_measurement_data[0])
    cal_measurement_data = np.loadtxt(f_name_beam_pattern_calibrated)
    cal_measurement_data = np.append(cal_measurement_data, cal_measurement_data[0])

    # Normalize measurement data
    uncal_max_measurement_data = np.max(uncal_measurement_data)
    uncal_norm_measurement_data = uncal_measurement_data / uncal_max_measurement_data
    uncal_db_measurement_data = 20 * np.log10(uncal_norm_measurement_data)

    cal_max_measurement_data = np.max(cal_measurement_data)
    cal_norm_measurement_data = cal_measurement_data / cal_max_measurement_data
    cal_db_measurement_data = 20 * np.log10(cal_norm_measurement_data)

    # Construct theta array
    theta_degrees = np.linspace(min_angle, max_angle, num_angle_points, endpoint=True)
    theta = np.deg2rad(theta_degrees)

    # Import simulated beam pattern (omni directional)
    beam_pattern_sim_omni = np.loadtxt(f_name_beam_pattern_sim_omni)
    beam_pattern_sim_omni[beam_pattern_sim_omni == -inf] = math.nan
    beam_pattern_sim_omni[beam_pattern_sim_omni < -30] = -30

    # Plotting
    plt.clf()
    f = plt.figure()
    # plt.polar(theta, uncal_db_measurement_data, label='Uncalibrated', linewidth=1)
    # plt.polar(theta, cal_db_measurement_data, label='Calibrated', linewidth=1)
    # plt.polar(theta, beam_pattern_sim_omni, label='Theoretical', linewidth=1)


    plt.polar(theta, beam_pattern_sim_omni, label='Theoretical', linewidth=1)
    plt.polar(theta, cal_db_measurement_data, label='Calibrated', linewidth=1)
    plt.polar(theta, uncal_db_measurement_data, label='Uncalibrated', linewidth=1)
    ax = plt.gca()
    ax.set_rlabel_position(0)
    ax.set_rticks([-25, -20, -15, -10, -5, 0])
    plt.ylim((-30, 0))
    plt.ylabel('Response [dB]', loc='bottom', rotation=0)
    plt.legend(loc=(0.92, 0.92))
    plt.show()
    f.savefig(filename_plot_rms_dB_vs_angle_uncalibrated_and_calibrated, bbox_inches='tight')

def show_measurement_and_simulation_data():
    global f_name_beam_pattern
    global f_name_beam_pattern_sim_custom
    global f_name_beam_pattern_sim_omni
    global filename_plot_rms_dB_vs_angle_simandmeas

    # Load beam pattern measurement data and ensure a continuous plot [0 - 360°]
    measurement_data = np.loadtxt(f_name_beam_pattern)
    measurement_data = np.append(measurement_data, measurement_data[0])

    # Normalize measurement data
    max_measurement_data = np.max(measurement_data)
    norm_measurement_data = measurement_data / max_measurement_data
    db_measurement_data = 20 * np.log10(norm_measurement_data)

    # Construct theta array
    theta_degrees = np.linspace(min_angle, max_angle, num_angle_points, endpoint=True)
    theta = np.deg2rad(theta_degrees)

    # Import simulated beam patterns
    # First simulation: based on measured single speaker beam pattern
    beam_pattern_sim_custom = np.loadtxt(f_name_beam_pattern_sim_custom)
    beam_pattern_sim_omni = np.loadtxt(f_name_beam_pattern_sim_omni)
    beam_pattern_sim_omni[beam_pattern_sim_omni == -inf] = math.nan
    beam_pattern_sim_omni[beam_pattern_sim_omni < -30] = -30

    # Plotting
    plt.clf()
    f = plt.figure()
    plt.polar(theta, db_measurement_data, label='Measured', linewidth=1)
    plt.polar(theta, beam_pattern_sim_omni, label='Simulated', linewidth=1)
    ax = plt.gca()
    ax.set_rlabel_position(0)
    ax.set_rticks([-25, -20, -15, -10, -5, 0])
    plt.ylim((-30, 0))
    plt.ylabel('Response [dB]', loc='bottom', rotation=0)
    plt.legend(loc=(0.92, 0.92))
    plt.show()
    f.savefig(filename_plot_rms_dB_vs_angle, bbox_inches='tight')

show_speaker_response_uncalibrated()
show_speaker_response_calibrated()
# show_beam_pattern_measurement_data(True)
# show_measurement_and_simulation_data()
# show_calibrated_and_uncalibrated_beam_pattern()